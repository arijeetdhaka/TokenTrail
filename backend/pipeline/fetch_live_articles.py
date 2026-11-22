
import json
import time
from pathlib import Path

import requests

API_URL = "https://tokentrail-api.onrender.com/articles"
PAGE_SIZE = 50

BACKEND_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BACKEND_DIR / "data" / "unclassified_articles.json"

articles = []
page = 1
total = None

while True:
    response = requests.get(
        API_URL,
        params={
            "unclassified": "true",
            "page": page,
            "page_size": PAGE_SIZE
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    if total is None:
        total = data.get("total", 0)
        print(f"Unclassified articles reported by API: {total}")

    items = data.get("items", [])

    if not items:
        break

    for article in items:
        articles.append({
            "id": article.get("id"),
            "title": article.get("title", ""),
            "summary": article.get("summary") or "",
            "url": article.get("url", ""),
            "published_at": article.get("published_at"),
            "source": (article.get("source") or {}).get("name", "")
        })

    print(
        f"Page {page}: fetched {len(items)} articles | "
        f"Total collected: {len(articles)}"
    )

    if len(articles) >= total:
        break

    page += 1
    time.sleep(0.2)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE.write_text(
    json.dumps(articles, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("\nFETCH COMPLETE")
print("Articles saved:", len(articles))
print("Output file:", OUTPUT_FILE.resolve())
