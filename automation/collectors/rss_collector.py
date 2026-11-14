
import json
import time
import logging
from pathlib import Path
import httpx
import feedparser
from datetime import datetime, timezone


def collect_rss_news(feed_url, source_name):
    articles = []

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:
            response = httpx.get(
                feed_url,
                timeout=20,
                follow_redirects=True
            )

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

            return articles

        except httpx.HTTPError as error:

            logging.warning(
                f"{source_name} collection failed. "
                f"Attempt {attempt}/{max_attempts}: {error}"
            )

            if attempt < max_attempts:
                print(f"Retrying {source_name} in 5 seconds...")
                time.sleep(5)

            else:
                logging.error(
                    f"{source_name} collection failed after "
                    f"{max_attempts} attempts."
                )

        except Exception:
            logging.exception(
                f"Unexpected error while collecting {source_name}"
            )
            raise

    raise RuntimeError(
        f"RSS collection failed for {source_name} "
        f"after {max_attempts} attempts."
    )


def remove_duplicates(articles):
    unique_articles = []
    seen_urls = set()

    for article in articles:
        url = article["url"]

        if url and url not in seen_urls:
            unique_articles.append(article)
            seen_urls.add(url)

    return unique_articles


def normalize_articles(articles):
    normalized_articles = []

    for article in articles:
        normalized_article = {
            "title": article.get("title", "").strip(),
            "source": article.get("source", "").strip(),
            "url": article.get("url", "").strip(),
            "published_at": article.get("published_at", ""),
            "summary": article.get("summary", "").strip(),
            "collected_at": article.get("collected_at", "")
        }

        if normalized_article["title"] and normalized_article["url"]:
            normalized_articles.append(normalized_article)

    return normalized_articles


if __name__ == "__main__":

    rss_sources = [
        {
            "name": "OpenAI",
            "url": "https://openai.com/news/rss.xml"
        },
        {
            "name": "Google AI",
            "url": "https://blog.research.google/feeds/posts/default"
        }
    ]

    all_news = []

    for source in rss_sources:
        news = collect_rss_news(source["url"], source["name"])
        all_news.extend(news)

    print("\nArticles before removing duplicates:", len(all_news))

    all_news = remove_duplicates(all_news)

    print("Articles after removing duplicates:", len(all_news))

    all_news = normalize_articles(all_news)

    print("Valid articles after normalization:", len(all_news))
    print("\nTotal articles collected:", len(all_news))

    data_folder = Path(__file__).resolve().parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    output_file = data_folder / "raw_news.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_news, file, indent=4, ensure_ascii=False)

    print("News saved successfully at:", output_file)
