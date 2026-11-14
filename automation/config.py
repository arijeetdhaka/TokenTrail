import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

# Explicitly load automation/.env regardless of current working directory
load_dotenv(ENV_PATH)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")
INGEST_API_KEY = os.getenv("INGEST_API_KEY", "").strip()

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
