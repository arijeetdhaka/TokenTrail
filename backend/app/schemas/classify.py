from pydantic import BaseModel, Field


class CategoryScore(BaseModel):
    category_id: int
    confidence: float = Field(ge=0, le=1)


class TopicScore(BaseModel):
    topic_id: int
    relevance: float = Field(ge=0, le=1)


class ClassificationIn(BaseModel):
    article_id: int
    categories: list[CategoryScore] | None = None
    topics: list[TopicScore] | None = None
    takeaways: list[str] | None = Field(default=None, max_length=10)


class ClassifyBulkIn(BaseModel):
    results: list[ClassificationIn] = Field(min_length=1, max_length=500)


class ClassifyError(BaseModel):
    article_id: int
    reason: str


class ClassifyResult(BaseModel):
    received: int
    updated: int
    failed: int
    errors: list[ClassifyError]