
from pathlib import Path
import joblib


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "keyword_vectorizer.joblib"

_vectorizer = None


def load_keyword_vectorizer():
    global _vectorizer

    if _vectorizer is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Keyword vectorizer not found. "
                "Run pipeline.train_keyword_extractor first."
            )

        _vectorizer = joblib.load(MODEL_PATH)

    return _vectorizer


def extract_keywords(
    title: str,
    text: str,
    top_n: int = 8
) -> list[str]:

    content = f"{title or ''} {text or ''}".strip()

    if not content or top_n <= 0:
        return []

    vectorizer = load_keyword_vectorizer()

    features = vectorizer.transform([content])

    scores = features.toarray()[0]
    words = vectorizer.get_feature_names_out()

    ranked_keywords = sorted(
        zip(words, scores),
        key=lambda item: item[1],
        reverse=True
    )

    keywords = [
        word
        for word, score in ranked_keywords
        if score > 0
    ]

    return keywords[:top_n]
