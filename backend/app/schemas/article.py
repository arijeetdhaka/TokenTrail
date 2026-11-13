from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.category import CategoryOut
from app.schemas.topic import TopicOut


class SourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ArticleListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    url: str
    published_at: datetime | None
    summary: str | None
    source: SourceOut
    categories: list[CategoryOut]


class ArticleDetail(ArticleListItem):
    takeaways: list[str] | None
    topics: list[TopicOut]


class ArticlePage(BaseModel):
    items: list[ArticleListItem]
    total: int
    page: int
    page_size: int