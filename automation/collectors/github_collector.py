
import httpx
import json
import time
import logging
from datetime import datetime, timezone
from pathlib import Path


def collect_github_repositories(topic, limit=10):

    repositories = []

    url = "https://api.github.com/search/repositories"

    params = {
        "q": f"{topic} in:name,description",
        "sort": "updated",
        "order": "desc",
        "per_page": limit
    }

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:
            response = httpx.get(
                url,
                params=params,
                timeout=20,
                headers={"Accept": "application/vnd.github+json"}
            )

            response.raise_for_status()

            data = response.json()

            for repo in data.get("items", []):

                repository = {
                    "name": repo.get("full_name", ""),
                    "description": repo.get("description") or "",
                    "url": repo.get("html_url", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "language": repo.get("language") or "",
                    "topics": repo.get("topics", []),
                    "updated_at": repo.get("updated_at", ""),
                    "collected_at": datetime.now(timezone.utc).isoformat()
                }

                repositories.append(repository)

            print(f"Collected {len(repositories)} repositories for {topic}")

            return repositories

        except httpx.HTTPError as error:

            logging.warning(
                f"GitHub collection failed for {topic}. "
                f"Attempt {attempt}/{max_attempts}: {error}"
            )

            if attempt < max_attempts:
                print(f"Retrying GitHub collection for {topic} in 5 seconds...")
                time.sleep(5)

            else:
                logging.error(
                    f"GitHub collection failed for {topic} "
                    f"after {max_attempts} attempts."
                )

        except Exception:
            logging.exception(
                f"Unexpected error while collecting GitHub topic: {topic}"
            )
            raise

    raise RuntimeError(
        f"GitHub collection failed for {topic} "
        f"after {max_attempts} attempts."
    )


def remove_duplicate_repositories(repositories):

    unique_repositories = []
    seen_names = set()

    for repo in repositories:

        name = repo["name"]

        if name and name not in seen_names:
            unique_repositories.append(repo)
            seen_names.add(name)

    return unique_repositories


if __name__ == "__main__":

    topics = [
        "machine-learning",
        "generative-ai",
        "large-language-model",
        "ai-agents",
        "deep-learning"
    ]

    all_repositories = []

    for topic in topics:

        repositories = collect_github_repositories(
            topic=topic,
            limit=10
        )

        all_repositories.extend(repositories)

    print("\nRepositories before removing duplicates:",
          len(all_repositories))

    all_repositories = remove_duplicate_repositories(all_repositories)

    print("Repositories after removing duplicates:",
          len(all_repositories))

    data_folder = Path(__file__).resolve().parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    output_file = data_folder / "github_repositories.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_repositories, file, indent=4, ensure_ascii=False)

    print("\nTotal unique repositories:", len(all_repositories))
    print("Repositories saved successfully at:", output_file)
