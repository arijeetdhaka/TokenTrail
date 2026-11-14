from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class TopicStatusIn(BaseModel):
    status: Literal["explored", "learning", "completed"]


class TopicProgressOut(BaseModel):
    slug: str
    name: str
    domain: str
    status: str
    updated_at: datetime


class DomainProgressOut(BaseModel):
    domain: str
    explored: int
    total: int


class ProgressOut(BaseModel):
    overall_percent: int
    topics_explored: int
    topics_total: int
    snippets_read: int
    snippets_total: int
    explore_visited: int
    explore_total: int
    saved_articles: int
    saved_article_ids: list[int]
    read_snippet_ids: list[int]
    visited_explore_ids: list[int]
    domains: list[DomainProgressOut]
    topics: list[TopicProgressOut]