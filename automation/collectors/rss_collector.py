import json
from pathlib import Path
import httpx
import feedparser
from datetime import datetime, timezone


def collect_rss_news(feed_url, source_name):
    articles = []

    try:
        response = httpx.get(feed_url, timeout=20)
        response.raise_for_status()

        feed = feedparser.parse(response.content)

        for entry in feed.entries:
            article = {
                "title": entry.get("title", "No title"),
                "source": source_name,
                "url": entry.get("link", ""),
                "published_at": entry.get("published", ""),
                "summary": entry.get("summary", ""),
                "collected_at": datetime.now(timezone.utc).isoformat()
            }

            articles.append(article)

        print(f"Collected {len(articles)} articles from {source_name}")

    except httpx.HTTPError as error:
        print(f"Network error while collecting {source_name}: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")

    return articles


if __name__ == "__main__":

    feed_url = "https://openai.com/news/rss.xml"

    news = collect_rss_news(feed_url, "OpenAI")
    data_folder = Path(__file__).resolve().parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)
    output_file = data_folder / "raw_news.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(news, file, indent=4, ensure_ascii=False)
    print(f"News saved successfully at: {output_file}")

    print("\n========== TOKENTRAIL AI NEWS ==========\n")

    for article in news[:5]:
        print("Title:", article["title"])
        print("Source:", article["source"])
        print("URL:", article["url"])
        print("Published:", article["published_at"])
        print("-" * 60)
