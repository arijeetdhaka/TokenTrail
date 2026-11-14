from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.topic import TopicOut


class SnippetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    source_url: str | None
    article_id: int | None
    topic: TopicOut | None
    created_at: datetime