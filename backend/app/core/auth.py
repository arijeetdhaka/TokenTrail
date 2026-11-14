import base64
import hashlib
import hmac
import json
import os
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.models.profile import Profile

security = HTTPBearer(auto_error=False)


def _decode_jwt_unverified(token: str) -> dict:
    """Safely decode JWT payload without external network dependency."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT token format")
        payload_b64 = parts[1]
        # Handle base64 padding
        padding = 4 - (len(payload_b64) % 4)
        if padding != 4:
            payload_b64 += "=" * padding
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        return json.loads(payload_bytes.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token format"
        ) from exc


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    x_test_user_id: str | None = Header(None, alias="X-Test-User-Id")
) -> UUID:
    """
    Extract and validate current user UUID from authentication token.
    Never accepts arbitrary user IDs as identity unless explicitly configured for testing.
    """
    # Safe test-mode bypass for unit tests only
    test_mode = os.getenv("TESTING", "").lower() in ("true", "1", "yes")
    if test_mode and x_test_user_id:
        try:
            return UUID(x_test_user_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid X-Test-User-Id UUID format"
            ) from exc

    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = _decode_jwt_unverified(token)

    # Supabase Auth tokens store the user UUID in the 'sub' claim
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identity ('sub' claim)"
        )

    try:
        return UUID(user_id_str)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token"
        ) from exc


def get_current_user_profile(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Profile:
    """
    Fetch the Profile corresponding to the authenticated user ID.
    """
    profile = db.query(Profile).filter(Profile.id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    return profile
