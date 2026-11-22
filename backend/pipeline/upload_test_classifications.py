import json
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

API_URL = "https://tokentrail-api.onrender.com"

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")
PREDICTIONS_FILE = BACKEND_DIR / "data" / "live_nlp_predictions.json"

TEST_ARTICLE_IDS = {
    1411, 1413, 1412, 1414, 1418,
    1417, 1416, 1415, 1419, 1422
}


def main():
    # 1. Load existing NLP predictions
    predictions = json.loads(
        PREDICTIONS_FILE.read_text(encoding="utf-8")
    )

    # 2. Fetch actual category IDs from the backend
    response = requests.get(
        f"{API_URL}/categories",
        timeout=60
    )
    response.raise_for_status()

    categories = response.json()

    category_map = {
        category["name"].strip().lower(): category["id"]
        for category in categories
    }

    # 3. Prepare only positive predictions for our 10 test articles
    results = []
    skipped = []

    for prediction in predictions:
        article_id = prediction.get("article_id")

        if article_id not in TEST_ARTICLE_IDS:
            continue

        predicted_categories = prediction.get("categories", [])

        if not predicted_categories:
            skipped.append(article_id)
            continue

        category_scores = []

        for item in predicted_categories:
            category_name = item["category"].strip().lower()

            if category_name not in category_map:
                raise ValueError(
                    f"Unknown category: {item['category']}"
                )

            category_scores.append({
                "category_id": category_map[category_name],
                "confidence": float(item["confidence"])
            })

        results.append({
            "article_id": article_id,
            "categories": category_scores
        })

    if not results:
        print("No positive predictions available.")
        return

    # 4. Show exactly what will be uploaded
    print("\n===== UPLOAD PREVIEW =====")
    print("Articles to upload:", len(results))
    print("Articles skipped (no predicted category):", skipped)
    print(json.dumps({"results": results}, indent=2))

    # 5. Ask for confirmation before changing the database
    confirm = input(
        "\nType UPLOAD to send these classifications: "
    )

    if confirm != "UPLOAD":
        print("Upload cancelled. No database changes made.")
        return

    # 6. Read API key securely (input will not be displayed)
    api_key = os.getenv("INGEST_API_KEY", "").strip()

    if not api_key:
        print("INGEST_API_KEY not found in backend/.env")
        return

    # 7. Send classifications to the live backend
    upload_response = requests.post(
        f"{API_URL}/articles/classify/bulk",
        headers={"X-API-Key": api_key},
        json={"results": results},
        timeout=120
    )

    print("\nHTTP Status:", upload_response.status_code)
    print("API Response:")

    try:
        print(json.dumps(upload_response.json(), indent=2))
    except ValueError:
        print(upload_response.text)

    upload_response.raise_for_status()


if __name__ == "__main__":
    main()