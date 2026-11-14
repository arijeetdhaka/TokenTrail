from pydantic import BaseModel, ConfigDict

from app.schemas.topic import TopicOut


class ExploreItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    description: str | None
    url: str
    topic: TopicOut | None