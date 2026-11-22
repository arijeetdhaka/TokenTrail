
import requests

API_URL = "https://tokentrail-api.onrender.com"

article_ids = [
    1411, 1413, 1412, 1414, 1418,
    1417, 1416, 1415, 1419, 1422
]

print("Checking current database classifications...\n")

for article_id in article_ids:
    try:
        response = requests.get(
            f"{API_URL}/articles/{article_id}",
            timeout=60
        )
        response.raise_for_status()

        article = response.json()

        print("Article ID:", article_id)
        print("Title:", article.get("title"))
        print("Categories:", article.get("categories"))
        print("Topics:", article.get("topics"))
        print("-" * 60)

    except Exception as error:
        print("Error for article", article_id, ":", error)
