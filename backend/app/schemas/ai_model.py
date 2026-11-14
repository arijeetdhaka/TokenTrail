
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AIModelResponse(BaseModel):
    id: UUID
    provider_id: UUID | None = None
    name: str
    slug: str
    description: str | None = None
    model_type: str | None = None
    pricing_type: str | None = None
    website_url: str | None = None
    documentation_url: str | None = None
    release_date: date | None = None
    context_window: int | None = None
    is_open_source: bool
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AIModelListResponse(BaseModel):
    message: str
    data: list[AIModelResponse]
