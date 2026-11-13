
import json
import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

logger.info("TokenTrail logging system initialized")


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


def run_all_collectors():

    print("\n========== TOKENTRAIL AUTOMATION STARTED ==========\n")
    logger.info("TokenTrail automation started")

    # 1. Collect RSS News

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

    all_news = remove_duplicates(all_news)
    all_news = normalize_articles(all_news)

    print("\nTotal unique news articles:", len(all_news))
    logger.info(f"RSS collection completed. Articles: {len(all_news)}")


    # 2. Collect GitHub Repositories

    github_topics = [
        "machine-learning",
        "generative-ai",
        "large-language-model",
        "ai-agents",
        "deep-learning"
    ]

    all_repositories = []

    for topic in github_topics:
        repositories = collect_github_repositories(topic, limit=10)
        all_repositories.extend(repositories)

    all_repositories = remove_duplicate_repositories(all_repositories)

    print("Total unique GitHub repositories:", len(all_repositories))
    logger.info(f"GitHub collection completed. Repositories: {len(all_repositories)}")


    # 3. Collect Hugging Face Models

    huggingface_tasks = [
        "text-generation",
        "text-classification",
        "text-to-image",
        "image-classification",
        "sentence-similarity"
    ]

    all_models = []

    for task in huggingface_tasks:
        models = collect_huggingface_models(task, limit=10)
        all_models.extend(models)

    all_models = remove_duplicate_models(all_models)

    print("Total unique Hugging Face models:", len(all_models))
    logger.info(f"Hugging Face collection completed. Models: {len(all_models)}")


    # 4. Collect arXiv Research Papers

    all_papers = collect_arxiv_papers(limit=50)

    all_papers = remove_duplicate_papers(all_papers)

    print("Total unique research papers:", len(all_papers))
    logger.info(f"arXiv collection completed. Papers: {len(all_papers)}")


    # 5. Save all collected data

    data_folder = Path(__file__).resolve().parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    datasets = {
        "raw_news.json": all_news,
        "github_repositories.json": all_repositories,
        "huggingface_models.json": all_models,
        "arxiv_papers.json": all_papers
    }

    for filename, records in datasets.items():

        output_file = data_folder / filename

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, ensure_ascii=False)

        print(f"Saved {len(records)} records in {filename}")

    print("\n========== TOKENTRAIL AUTOMATION COMPLETED ==========")
    logger.info("TokenTrail automation completed successfully")



if __name__ == "__main__":

    try:
        run_all_collectors()

    except Exception:
        logger.exception("TokenTrail automation failed")
