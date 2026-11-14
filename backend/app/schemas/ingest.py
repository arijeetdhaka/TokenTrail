from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ArticleIn(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    url: str = Field(min_length=1, max_length=1000)
    source: str = Field(min_length=1, max_length=200)
    source_url: str = Field(min_length=1, max_length=500)
    published_at: datetime | None = None
    summary: str | None = None

    @field_validator("published_at", mode="before")
    @classmethod
    def accept_rss_dates(cls, value):
        """Accept ISO dates and RSS dates like 'Fri, 13 Nov 2026 15:00:00 GMT'."""
        if not value:
            return None
        if isinstance(value, str) and not value[:4].isdigit():
            return parsedate_to_datetime(value)
        return value


class ArticleBulkIn(BaseModel):
    articles: list[ArticleIn] = Field(min_length=1, max_length=500)


class ExploreItemIn(BaseModel):
    type: Literal["repo", "model", "paper", "tool", "framework"]
    name: str = Field(min_length=1, max_length=500)
    url: str = Field(min_length=1, max_length=1000)
    description: str | None = None


class ExploreBulkIn(BaseModel):
    items: list[ExploreItemIn] = Field(min_length=1, max_length=500)


class BulkResult(BaseModel):
    received: int
    inserted: int
    skipped: int