
import sys
import json
from pathlib import Path
from collections import Counter

# Find the backend folder
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# File locations
INPUT_FILE = BACKEND_DIR / "data" / "unclassified_articles.json"
OUTPUT_FILE = BACKEND_DIR / "data" / "unclassified_nlp_predictions.json"

# Import NLP pipeline
from app.services.nlp import process_article


def main():
    if not INPUT_FILE.exists():
        print("ERROR: Live articles file not found:", INPUT_FILE)
        return

    articles = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    predictions = []
    errors = []
    category_counts = Counter()

    print(f"Processing {len(articles)} live articles...\n")

    for index, article in enumerate(articles, start=1):
        try:
            title = article.get("title") or ""
            summary = article.get("summary") or ""

            if not title.strip() and not summary.strip():
                errors.append({
                    "article_id": article.get("id"),
                    "error": "No title or summary"
                })
                continue

            result = process_article(title, summary)

            predictions.append({
                "article_id": article["id"],
                "title": title,
                "categories": result["categories"],
                "keywords": result["keywords"],
                "generated_summary": result["summary"]
            })

            for category in result["categories"]:
                category_counts[category["category"]] += 1

            if index % 100 == 0:
                print(f"Processed {index}/{len(articles)}")

        except Exception as error:
            errors.append({
                "article_id": article.get("id"),
                "error": str(error)
            })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(predictions, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("\n===== NLP PROCESSING COMPLETE =====")
    print("Total articles:", len(articles))
    print("Successfully processed:", len(predictions))
    print("Errors:", len(errors))

    print("\n===== CATEGORY DISTRIBUTION =====")
    for category, count in category_counts.most_common():
        print(category, ":", count)

    print("\n===== FIRST PREDICTION =====")
    if predictions:
        print(json.dumps(predictions[0], indent=2, ensure_ascii=False))

    if errors:
        print("\n===== FIRST ERRORS =====")
        print(json.dumps(errors[:5], indent=2, ensure_ascii=False))

    print("\nSaved at:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
