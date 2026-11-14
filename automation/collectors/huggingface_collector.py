
import json
import time
import logging
import httpx
from pathlib import Path
from datetime import datetime, timezone


def collect_huggingface_models(task, limit=10):

    models = []

    url = "https://huggingface.co/api/models"

    params = {
        "pipeline_tag": task,
        "sort": "downloads",
        "direction": "-1",
        "limit": limit
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

            data = response.json()

            for model in data:

                model_id = model.get("modelId") or model.get("id", "")

                model_info = {
                    "model_id": model_id,
                    "downloads": model.get("downloads", 0),
                    "likes": model.get("likes", 0),
                    "pipeline_tag": model.get("pipeline_tag", task),
                    "url": "https://huggingface.co/" + model_id,
                    "collected_at": datetime.now(timezone.utc).isoformat()
                }

                models.append(model_info)

            print(f"Collected {len(models)} models for {task}")

            return models

        except httpx.HTTPError as error:

            logging.warning(
                f"Hugging Face collection failed for {task}. "
                f"Attempt {attempt}/{max_attempts}: {error}"
            )

            if attempt < max_attempts:
                print(f"Retrying Hugging Face collection for {task} in 5 seconds...")
                time.sleep(5)

            else:
                logging.error(
                    f"Hugging Face collection failed for {task} "
                    f"after {max_attempts} attempts."
                )

        except Exception:
            logging.exception(
                f"Unexpected error while collecting Hugging Face task: {task}"
            )
            raise

    raise RuntimeError(
        f"Hugging Face collection failed for {task} "
        f"after {max_attempts} attempts."
    )


def remove_duplicate_models(models):

    unique_models = []
    seen_model_ids = set()

    for model in models:

        model_id = model["model_id"]

        if model_id and model_id not in seen_model_ids:
            unique_models.append(model)
            seen_model_ids.add(model_id)

    return unique_models


if __name__ == "__main__":

    tasks = [
        "text-generation",
        "text-classification",
        "text-to-image",
        "image-classification",
        "sentence-similarity"
    ]

    all_models = []

    for task in tasks:

        models = collect_huggingface_models(
            task=task,
            limit=10
        )

        all_models.extend(models)

    print("\nModels before removing duplicates:", len(all_models))

    all_models = remove_duplicate_models(all_models)

    print("Models after removing duplicates:", len(all_models))

    data_folder = Path(__file__).resolve().parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    output_file = data_folder / "huggingface_models.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_models, file, indent=4, ensure_ascii=False)

    print("\nTotal unique models:", len(all_models))
    print("Models saved successfully at:", output_file)
