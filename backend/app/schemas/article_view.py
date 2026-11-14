from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ArticleViewCreate(BaseModel):
    article_id: UUID
    read_duration: int = Field(default=0, ge=0)
    is_completed: bool = False


class ArticleViewResponse(BaseModel):
    id: UUID
    user_id: UUID
    article_id: UUID
    viewed_at: datetime
    read_duration: int
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)


class ArticleViewActionResponse(BaseModel):
    message: str
    data: ArticleViewResponse
