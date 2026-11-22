
from pipeline.preprocessing import clean_text
from pipeline.classification import classify_article
from pipeline.keyword_extraction import extract_keywords
from pipeline.summarization import summarize_article


def process_article(title: str, text: str) -> dict:
    """
    Process an article using all four NLP modules.
    """

    # Step 1: Clean article text
    cleaned_text = clean_text(text)

    # Step 2: Predict article categories
    categories = classify_article(title, cleaned_text)

    # Step 3: Extract important keywords
    keywords = extract_keywords(title, cleaned_text, top_n=8)

    # Step 4: Generate article summary
    summary = summarize_article(title, cleaned_text, max_sentences=3)

    # Return all NLP results
    return {
        "cleaned_text": cleaned_text,
        "categories": categories,
        "keywords": keywords,
        "summary": summary
    }
