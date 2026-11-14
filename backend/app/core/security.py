import secrets

from fastapi import Header, HTTPException, status

from app.core.config import settings


def require_ingest_key(x_api_key: str | None = Header(default=None)) -> None:
    """Allow the request only if it carries the correct X-API-Key header."""
    if not settings.ingest_api_key:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="Ingestion is not configured")
    if x_api_key is None or not secrets.compare_digest(x_api_key, settings.ingest_api_key):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")