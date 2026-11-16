
from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    ENGLISH_STOP_WORDS
)


# Get backend folder path
BASE_DIR = Path(__file__).resolve().parents[1]

# File paths
DATA_PATH = BASE_DIR / "data" / "tokentrail_training_data.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "keyword_vectorizer.joblib"


def train_keyword_extractor():

    # Read training dataset
    df = pd.read_csv(DATA_PATH)

    # Handle missing values
    df["title"] = df["title"].fillna("")
    df["summary"] = df["summary"].fillna("")

    # Combine title and summary
    texts = (
        df["title"] + " " +
        df["title"] + " " +
        df["summary"]
    ).str.strip()

    # Remove empty articles
    texts = texts[texts != ""]

    if texts.empty:
        raise ValueError("No article text found.")

    # Custom words to ignore
    custom_stop_words = [
        "introducing",
        "introduce",
        "new",
        "year",
        "today",
        "announced",
        "announces",
        "available",
        "worldwide",
        "support",
        "building",
        "ll"
    ]

    # Combine standard English stop words with custom words
    all_stop_words = ENGLISH_STOP_WORDS.union(custom_stop_words)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words=list(all_stop_words),
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9.-]*\b",
        ngram_range=(1, 2),
        min_df=1,
        max_features=5000
    )

    # Train vectorizer
    vectorizer.fit(texts)

    # Create models folder if needed
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Save trained vectorizer
    joblib.dump(vectorizer, MODEL_PATH)

    print("Keyword vectorizer trained successfully!")
    print("Articles used:", len(texts))
    print("Vocabulary size:", len(vectorizer.vocabulary_))
    print("Model saved at:", MODEL_PATH)


if __name__ == "__main__":
    train_keyword_extractor()
