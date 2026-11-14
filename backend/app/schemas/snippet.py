
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SnippetResponse(BaseModel):
    id: UUID
    article_id: UUID | None = None
    category_id: UUID
    title: str
    content: str
    takeaway: str | None = None
    image_url: str | None = None
    difficulty: str | None = None
    estimated_read_time: int | None = None
    is_published: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class SnippetListResponse(BaseModel):
    message: str
    data: list[SnippetResponse]
