
import httpx
import feedparser
import json
import time
import logging
from pathlib import Path
from datetime import datetime, timezone


def collect_arxiv_papers(limit=10):

    papers = []

    url = "https://export.arxiv.org/api/query"

    params = {
        "search_query": "cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR cat:cs.CL",
        "start": 0,
        "max_results": limit,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:
            response = httpx.get(
                url,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            feed = feedparser.parse(response.content)

            if feed.bozo:
                raise ValueError("Invalid or malformed arXiv feed response")

            for entry in feed.entries:

                paper = {
                    "title": entry.get("title", "").strip(),
                    "abstract": entry.get("summary", "").strip(),
                    "authors": [
                        author.get("name", "")
                        for author in entry.get("authors", [])
                    ],
                    "url": entry.get("id", ""),
                    "published_at": entry.get("published", ""),
                    "updated_at": entry.get("updated", ""),
                    "categories": [
                        category.get("term", "")
                        for category in entry.get("tags", [])
                    ],
                    "collected_at": datetime.now(timezone.utc).isoformat()
                }

                papers.append(paper)

            print("Collected research papers:", len(papers))

            return papers

        except httpx.HTTPError as error:

            logging.warning(
                f"arXiv collection failed. "
                f"Attempt {attempt}/{max_attempts}: {error}"
            )

        except ValueError as error:

            logging.warning(
                f"arXiv response error. "
                f"Attempt {attempt}/{max_attempts}: {error}"
            )

        except Exception:
            logging.exception("Unexpected error while collecting arXiv papers")
            raise

        if attempt < max_attempts:
            print("Retrying arXiv collection in 5 seconds...")
            time.sleep(5)

    raise RuntimeError(
        f"arXiv collection failed after {max_attempts} attempts."
    )


def remove_duplicate_papers(papers):

    unique_papers = []
    seen_urls = set()

    for paper in papers:

        url = paper["url"]

        if url and url not in seen_urls:
            unique_papers.append(paper)
            seen_urls.add(url)

    return unique_papers


if __name__ == "__main__":

    papers = collect_arxiv_papers(limit=50)

    print("\nPapers before removing duplicates:", len(papers))

    papers = remove_duplicate_papers(papers)

    print("Papers after removing duplicates:", len(papers))

    print("\n========== TOKENTRAIL AI RESEARCH PAPERS ==========\n")

    for paper in papers:
        print("Title:", paper["title"])
        print("Authors:", ", ".join(paper["authors"]))
        print("Published:", paper["published_at"])
        print("Categories:", paper["categories"])
        print("URL:", paper["url"])
        print("-" * 60)

    print("Total unique papers:", len(papers))

    data_folder = Path(__file__).resolve().parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    output_file = data_folder / "arxiv_papers.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(papers, file, indent=4, ensure_ascii=False)

    print("Papers saved successfully at:", output_file)
