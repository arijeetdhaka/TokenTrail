
from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProgressResponse(BaseModel):
    user_id: UUID
    activity_date: date
    total_read_time: int

    model_config = ConfigDict(from_attributes=True)


class ProgressListResponse(BaseModel):
    message: str
    data: list[ProgressResponse]
