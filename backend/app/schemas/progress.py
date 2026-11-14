from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    activity_date: date
    articles_read: int
    snippets_viewed: int
    models_explored: int
    total_read_time: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProgressListResponse(BaseModel):
    message: str
    data: list[ProgressResponse]


class ActivityRecordRequest(BaseModel):
    articles_read: int = Field(default=0, ge=0)
    snippets_viewed: int = Field(default=0, ge=0)
    models_explored: int = Field(default=0, ge=0)
    read_duration: int = Field(default=0, ge=0)


class ProgressSummaryData(BaseModel):
    total_articles_read: int
    total_snippets_viewed: int
    total_models_explored: int
    total_read_time: int
    days_active: int


class ProgressSummaryResponse(BaseModel):
    message: str
    data: ProgressSummaryData
