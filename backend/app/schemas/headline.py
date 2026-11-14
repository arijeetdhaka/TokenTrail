
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class HeadlineResponse(BaseModel):
    id: UUID
    title: str
    summary: str | None = None
    original_url: str
    image_url: str | None = None
    author: str | None = None
    published_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class HeadlineListResponse(BaseModel):
    message: str
    data: list[HeadlineResponse]