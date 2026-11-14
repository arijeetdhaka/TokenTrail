
import logging
import os
import time
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

INGEST_API_KEY = os.getenv("INGEST_API_KEY", "").strip()

BATCH_SIZE = 500
MAX_RETRIES = 3
TIMEOUT = 60

RETRYABLE_STATUS_CODES = {408, 425, 429, 500, 502, 503, 504}


class BackendClientError(Exception):
    pass


def _headers() -> dict[str, str]:
    if not INGEST_API_KEY:
        raise BackendClientError(
            "INGEST_API_KEY is missing from automation/.env"
        )

    return {
        "Content-Type": "application/json",
        "X-API-Key": INGEST_API_KEY
    }


def _send_batch(
    endpoint: str,
    payload: dict[str, Any]
) -> dict[str, Any]:

    url = f"{API_URL}{endpoint}"
    headers = _headers()

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            logger.info(
                "Sending batch to %s. Attempt %s/%s",
                endpoint,
                attempt,
                MAX_RETRIES
            )

            with httpx.Client(timeout=TIMEOUT) as client:
                response = client.post(
                    url,
                    json=payload,
                    headers=headers
                )

            if response.status_code == 200:
                result = response.json()

                logger.info(
                    "Backend response for %s: %s",
                    endpoint,
                    result
                )

                return result

            if response.status_code not in RETRYABLE_STATUS_CODES:
                raise BackendClientError(
                    f"Backend returned HTTP "
                    f"{response.status_code}: {response.text[:1000]}"
                )

            logger.warning(
                "Temporary HTTP error %s from %s",
                response.status_code,
                endpoint
            )

        except httpx.RequestError as error:
            logger.warning(
                "Connection error while calling %s: %s",
                endpoint,
                error
            )

        if attempt < MAX_RETRIES:
            delay = 2 ** attempt
            logger.info("Retrying in %s seconds", delay)
            time.sleep(delay)

    raise BackendClientError(
        f"Failed to send batch to {endpoint} after {MAX_RETRIES} attempts."
    )


def _send_in_batches(
    endpoint: str,
    key: str,
    records: list[dict[str, Any]]
) -> dict[str, int]:

    totals = {
        "received": 0,
        "inserted": 0,
        "skipped": 0
    }

    if not records:
        logger.info("No records available for %s", endpoint)
        return totals

    for start in range(0, len(records), BATCH_SIZE):

        batch = records[start:start + BATCH_SIZE]

        result = _send_batch(
            endpoint,
            {key: batch}
        )

        for field in totals:
            totals[field] += int(result.get(field, 0))

    logger.info(
        "%s completed: received=%s inserted=%s skipped=%s",
        endpoint,
        totals["received"],
        totals["inserted"],
        totals["skipped"]
    )

    return totals


def send_articles(
    articles: list[dict[str, Any]]
) -> dict[str, int]:
    """
    Upload normalized RSS articles to POST /articles/bulk.

    Required fields:
    title, url, source, source_url.
    """

    required_fields = (
        "title",
        "url",
        "source",
        "source_url"
    )

    prepared = []

    for index, article in enumerate(articles):

        missing = [
            field for field in required_fields
            if not article.get(field)
        ]

        if missing:
            raise BackendClientError(
                f"Article at index {index} is missing: "
                f"{', '.join(missing)}"
            )

        prepared.append({
            "title": article["title"],
            "url": article["url"],
            "source": article["source"],
            "source_url": article["source_url"],
            "published_at": article.get("published_at"),
            "summary": article.get("summary")
        })

    return _send_in_batches(
        "/articles/bulk",
        "articles",
        prepared
    )


def send_explore_items(
    items: list[dict[str, Any]]
) -> dict[str, int]:
    """
    Upload repositories, models and papers
    to POST /explore/bulk.
    """

    valid_types = {"repo", "model", "paper"}
    prepared = []

    for index, item in enumerate(items):

        item_type = item.get("type")

        if item_type not in valid_types:
            raise BackendClientError(
                f"Explore item at index {index} has invalid type: "
                f"{item_type}"
            )

        if not item.get("name") or not item.get("url"):
            raise BackendClientError(
                f"Explore item at index {index} "
                "must contain name and url."
            )

        prepared.append({
            "type": item_type,
            "name": item["name"],
            "url": item["url"],
            "description": item.get("description")
        })

    return _send_in_batches(
        "/explore/bulk",
        "items",
        prepared
    )
