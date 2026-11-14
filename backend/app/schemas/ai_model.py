from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ModelProviderResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    website_url: str | None = None
    logo_url: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ModelProviderListResponse(BaseModel):
    message: str
    data: list[ModelProviderResponse]


class AIModelResponse(BaseModel):
    id: UUID
    provider_id: UUID | None = None
    name: str
    slug: str
    description: str | None = None
    model_type: str | None = None
    pricing_type: str
    website_url: str | None = None
    documentation_url: str | None = None
    release_date: date | None = None
    context_window: int | None = None
    is_open_source: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AIModelListResponse(BaseModel):
    message: str
    data: list[AIModelResponse]
    total: int | None = None
    limit: int | None = None
    offset: int | None = None


class AIModelDetailResponse(BaseModel):
    message: str
    data: AIModelResponse
