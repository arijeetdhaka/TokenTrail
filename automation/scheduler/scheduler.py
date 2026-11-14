
import sys
import logging
from pathlib import Path
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

AUTOMATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTOMATION_DIR))

from main import (
    run_rss_collection,
    run_github_collection,
    run_huggingface_collection,
    run_arxiv_collection
)

LOG_DIR = AUTOMATION_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "scheduler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

scheduler = BlockingScheduler(timezone="Asia/Kolkata")


def execute_job(job_name, collection_function):

    logger.info(f"{job_name} scheduled job started")

    try:
        collection_function()
        logger.info(f"{job_name} scheduled job completed successfully")

    except Exception:
        logger.exception(f"{job_name} scheduled job failed")


scheduler.add_job(
    execute_job,
    trigger="interval",
    minutes=30,
    args=["RSS", run_rss_collection],
    id="rss_collection",
    max_instances=1,
    next_run_time=datetime.now()
)

scheduler.add_job(
    execute_job,
    trigger="interval",
    hours=6,
    args=["GitHub", run_github_collection],
    id="github_collection",
    max_instances=1,
    next_run_time=datetime.now()
)

scheduler.add_job(
    execute_job,
    trigger="interval",
    hours=6,
    args=["Hugging Face", run_huggingface_collection],
    id="huggingface_collection",
    max_instances=1,
    next_run_time=datetime.now()
)

scheduler.add_job(
    execute_job,
    trigger="interval",
    hours=24,
    args=["arXiv", run_arxiv_collection],
    id="arxiv_collection",
    max_instances=1,
    next_run_time=datetime.now()
)

print("TokenTrail scheduler started.")
print("RSS: Every 30 minutes")
print("GitHub: Every 6 hours")
print("Hugging Face: Every 6 hours")
print("arXiv: Every 24 hours")

logger.info("TokenTrail scheduler started")

try:
    scheduler.start()

except (KeyboardInterrupt, SystemExit):
    logger.info("TokenTrail scheduler stopped")
    print("TokenTrail scheduler stopped")
