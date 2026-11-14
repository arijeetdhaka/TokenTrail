
import json
import logging
from pathlib import Path
from datetime import datetime, timezone

from services.backend_client import (
    send_articles,
    send_explore_items
)

from collectors.rss_collector import (
    collect_rss_news,
    remove_duplicates,
    normalize_articles
)

from collectors.github_collector import (
    collect_github_repositories,
    remove_duplicate_repositories
)

from collectors.huggingface_collector import (
    collect_huggingface_models,
    remove_duplicate_models
)

from collectors.arxiv_collector import (
    collect_arxiv_papers,
    remove_duplicate_papers
)


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


logging.basicConfig(
    filename=LOG_DIR / "automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def save_data(filename, records):

    output_file = DATA_DIR / filename

    existing_records = []

    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as file:
            existing_records = json.load(file)

    unique_records = {}

    for record in existing_records:

        record_id = (
            record.get("url")
            or record.get("model_id")
            or record.get("name")
        )

        if record_id:
            unique_records[record_id] = record

    current_time = datetime.now(timezone.utc).isoformat()

    for record in records:

        record_id = (
            record.get("url")
            or record.get("model_id")
            or record.get("name")
        )

        if not record_id:
            continue

        old_record = unique_records.get(record_id)

        if old_record:
            record["first_discovered_at"] = (
                old_record.get("first_discovered_at")
                or old_record.get("collected_at")
                or current_time
            )
        else:
            record["first_discovered_at"] = current_time

        record["last_updated_at"] = current_time

        unique_records[record_id] = record

    final_records = list(unique_records.values())

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            final_records,
            file,
            indent=4,
            ensure_ascii=False
        )

    logger.info(
        "Received %s records. Total unique records: %s in %s",
        len(records),
        len(final_records),
        filename
    )

    print(
        f"Received {len(records)} records. "
        f"Total unique records: {len(final_records)} "
        f"in {filename}"
    )


def run_rss_collection():

    logger.info("RSS collection started")

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

        try:
            news = collect_rss_news(
                source["url"],
                source["name"]
            )

            for article in news:
                article["source_url"] = source["url"]

            all_news.extend(news)

        except Exception:
            logger.exception(
                "RSS collection failed for %s",
                source["name"]
            )

    all_news = remove_duplicates(all_news)
    all_news = normalize_articles(all_news)

    for article in all_news:

        if not article.get("source_url"):

            article["source_url"] = next(
                (
                    source["url"]
                    for source in rss_sources
                    if source["name"] == article.get("source")
                ),
                None
            )

    save_data("raw_news.json", all_news)

    logger.info(
        "RSS collection completed. Articles: %s",
        len(all_news)
    )

    valid_articles = [
        article for article in all_news
        if (
            article.get("title")
            and article.get("url")
            and article.get("source")
            and article.get("source_url")
        )
    ]

    try:
        result = send_articles(valid_articles)

        logger.info(
            "RSS backend upload completed: %s",
            result
        )

    except Exception:
        logger.exception(
            "RSS backend upload failed. "
            "Local data remains saved."
        )


def run_github_collection():

    logger.info("GitHub collection started")

    github_topics = [
        "machine-learning",
        "generative-ai",
        "large-language-model",
        "ai-agents",
        "deep-learning"
    ]

    all_repositories = []

    for topic in github_topics:

        try:
            repositories = collect_github_repositories(
                topic,
                limit=10
            )

            all_repositories.extend(repositories)

        except Exception:
            logger.exception(
                "GitHub collection failed for topic: %s",
                topic
            )

    all_repositories = remove_duplicate_repositories(
        all_repositories
    )

    save_data(
        "github_repositories.json",
        all_repositories
    )

    logger.info(
        "GitHub collection completed. Repositories: %s",
        len(all_repositories)
    )

    explore_items = [
        {
            "type": "repo",
            "name": repository.get("name"),
            "url": repository.get("url"),
            "description": repository.get("description")
        }
        for repository in all_repositories
        if repository.get("name") and repository.get("url")
    ]

    try:
        result = send_explore_items(explore_items)

        logger.info(
            "GitHub backend upload completed: %s",
            result
        )

    except Exception:
        logger.exception(
            "GitHub backend upload failed. "
            "Local data remains saved."
        )


def run_huggingface_collection():

    logger.info("Hugging Face collection started")

    huggingface_tasks = [
        "text-generation",
        "text-classification",
        "text-to-image",
        "image-classification",
        "sentence-similarity"
    ]

    all_models = []

    for task in huggingface_tasks:

        try:
            models = collect_huggingface_models(
                task,
                limit=10
            )

            all_models.extend(models)

        except Exception:
            logger.exception(
                "Hugging Face collection failed for task: %s",
                task
            )

    all_models = remove_duplicate_models(all_models)

    save_data(
        "huggingface_models.json",
        all_models
    )

    logger.info(
        "Hugging Face collection completed. Models: %s",
        len(all_models)
    )

    explore_items = [
        {
            "type": "model",
            "name": model.get("model_id"),
            "url": model.get("url"),
            "description": model.get("description")
        }
        for model in all_models
        if model.get("model_id") and model.get("url")
    ]

    try:
        result = send_explore_items(explore_items)

        logger.info(
            "Hugging Face backend upload completed: %s",
            result
        )

    except Exception:
        logger.exception(
            "Hugging Face backend upload failed. "
            "Local data remains saved."
        )


def run_arxiv_collection():

    logger.info("arXiv collection started")

    try:
        all_papers = collect_arxiv_papers(limit=50)

    except Exception:
        logger.exception("arXiv collection failed")
        return

    all_papers = remove_duplicate_papers(all_papers)

    save_data(
        "arxiv_papers.json",
        all_papers
    )

    logger.info(
        "arXiv collection completed. Papers: %s",
        len(all_papers)
    )

    explore_items = [
        {
            "type": "paper",
            "name": paper.get("title"),
            "url": paper.get("url"),
            "description": paper.get("abstract")
        }
        for paper in all_papers
        if paper.get("title") and paper.get("url")
    ]

    try:
        result = send_explore_items(explore_items)

        logger.info(
            "arXiv backend upload completed: %s",
            result
        )

    except Exception:
        logger.exception(
            "arXiv backend upload failed. "
            "Local data remains saved."
        )


def run_all_collectors():

    print("\n========== TOKENTRAIL AUTOMATION STARTED ==========\n")

    logger.info("All collectors started")

    collection_jobs = [
        ("RSS", run_rss_collection),
        ("GitHub", run_github_collection),
        ("Hugging Face", run_huggingface_collection),
        ("arXiv", run_arxiv_collection)
    ]

    for job_name, job_function in collection_jobs:

        try:
            job_function()

        except Exception:
            logger.exception(
                "%s collection job failed",
                job_name
            )

    print("\n========== TOKENTRAIL AUTOMATION COMPLETED ==========\n")

    logger.info("All collection jobs finished")


if __name__ == "__main__":

    try:
        run_all_collectors()

    except Exception:
        logger.exception("TokenTrail automation failed")
