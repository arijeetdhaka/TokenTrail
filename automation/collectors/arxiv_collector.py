
import httpx
import feedparser
import json
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

    try:
        response = httpx.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        feed = feedparser.parse(response.content)

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

    except httpx.HTTPError as error:
        print("arXiv API error:", error)

    except Exception as error:
        print("Unexpected error:", error)

    return papers

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
