from pydantic import BaseModel, ConfigDict


class TopicOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    domain: str
    description: str | None