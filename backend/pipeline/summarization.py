import re

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    ENGLISH_STOP_WORDS
)

from sklearn.metrics.pairwise import cosine_similarity


def split_sentences(text: str) -> list[str]:
    """Split text into individual sentences."""

    if not text or not text.strip():
        return []

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def remove_acknowledgements(text: str) -> str:
    """Remove the acknowledgements section and everything after it."""

    pattern = r'\backnowledgements?\b'

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        text = text[:match.start()]

    return text.strip()

def remove_section_headings(text: str) -> str:
    """Remove section headings without deleting normal sentence words."""

    headings = [
        "Pre-training data",
        "Two-stage training",
        "Results",
        "Classification and localization",
        "Combining with LLMs",
        "Scientific applications",
        "Conclusion"
    ]

    for heading in headings:
        pattern = (
            r"(^|[.!?]\s+)"
            + re.escape(heading)
            + r"(?=\s+[A-Z])"
        )

        text = re.sub(pattern, r"\1", text)

    return text.strip()



def summarize_article(
    title: str,
    text: str,
    max_sentences: int = 3
) -> str:
    """Generate an extractive summary using TF-IDF sentence ranking."""

    if not text or not text.strip() or max_sentences <= 0:
        return ""

    # Remove acknowledgements before processing
    text = remove_acknowledgements(text)
    text = remove_section_headings(text)

    # Split article into sentences
    sentences = split_sentences(text)

    if not sentences:
        return ""

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    # Create TF-IDF sentence vectors
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:
        sentence_vectors = vectorizer.fit_transform(sentences)
    except ValueError:
        return " ".join(sentences[:max_sentences])

    # Extract important words from the title
    title_words = {
        word.lower()
        for word in re.findall(
            r"\b[a-zA-Z0-9.-]+\b",
            title or ""
        )
        if word.lower() not in ENGLISH_STOP_WORDS
    }

    scores = []

    for i, sentence in enumerate(sentences):

        # Average TF-IDF score
        vector = sentence_vectors[i]

        if vector.nnz == 0:
            tfidf_score = 0.0
        else:
            tfidf_score = float(vector.sum()) / vector.nnz

        # Title relevance
        sentence_words = {
            word.lower()
            for word in re.findall(
                r"\b[a-zA-Z0-9.-]+\b",
                sentence
            )
        }

        if title_words:
            overlap = len(title_words & sentence_words)
            title_score = overlap / len(title_words)
        else:
            title_score = 0.0

        # Give earlier sentences a stronger position score
        position_score = 1.0 / (i + 1)

        # Combine all scores
        final_score = (
            0.50 * tfidf_score
            + 0.30 * title_score
            + 0.20 * position_score
        )

        scores.append(final_score)

    # Select the highest-scoring sentences
    ranked_indices = sorted(
        range(len(sentences)),
        key=lambda i: scores[i],
        reverse=True
    )

    selected_indices = sorted(
        ranked_indices[:max_sentences]
    )

    # Return selected sentences in original order
    return " ".join(
        sentences[i]
        for i in selected_indices
    )
