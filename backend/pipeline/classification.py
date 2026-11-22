
from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "article_classifier.joblib"

_model_data = None


def load_classifier():
    """Load the trained classifier only when needed."""
    global _model_data

    if _model_data is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Trained model not found. "
                "Run pipeline.train_classifier first."
            )

        _model_data = joblib.load(MODEL_PATH)

    return _model_data



def classify_article(title: str, text: str) -> list[dict]:
    data = load_classifier()

    model = data["model"]
    vectorizer = data["vectorizer"]
    mlb = data["mlb"]

    content = f"{title or ''} {text or ''}".strip()

    if not content:
        return []

    features = vectorizer.transform([content])
    probabilities = model.predict_proba(features)[0]

    threshold = 0.5

    predicted_categories = []

    for category, probability in zip(mlb.classes_, probabilities):
        if probability >= threshold:
            predicted_categories.append({
                "category": category,
                "confidence": round(float(probability), 4)
            })

    return predicted_categories
