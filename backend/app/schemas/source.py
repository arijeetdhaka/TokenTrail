from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SourceResponse(BaseModel):
    id: UUID
    name: str
    website_url: str | None = None
    feed_url: str | None = None
    source_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SourceListResponse(BaseModel):
    message: str
    data: list[SourceResponse]


class SourceDetailResponse(BaseModel):
    message: str
    data: SourceResponse
