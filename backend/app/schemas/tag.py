from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TagResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagListResponse(BaseModel):
    message: str
    data: list[TagResponse]
