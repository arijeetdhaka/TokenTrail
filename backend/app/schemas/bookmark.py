from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ArticleBookmarkResponse(BaseModel):
    id: UUID
    user_id: UUID
    article_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ArticleBookmarkListResponse(BaseModel):
    message: str
    data: list[ArticleBookmarkResponse]


class SnippetBookmarkResponse(BaseModel):
    id: UUID
    user_id: UUID
    snippet_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SnippetBookmarkListResponse(BaseModel):
    message: str
    data: list[SnippetBookmarkResponse]


class ModelBookmarkResponse(BaseModel):
    id: UUID
    user_id: UUID
    model_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ModelBookmarkListResponse(BaseModel):
    message: str
    data: list[ModelBookmarkResponse]


class BookmarkActionResponse(BaseModel):
    message: str
    bookmarked: bool
