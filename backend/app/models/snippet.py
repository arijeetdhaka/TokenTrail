from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.topic import Topic


class Snippet(Base):
    __tablename__ = "snippets"
    __table_args__ = (
        CheckConstraint("level IN ('Beginner', 'Intermediate', 'Advanced')", name="ck_snippets_level"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str] = mapped_column(Text)
    level: Mapped[str | None] = mapped_column(String(20))
    read_minutes: Mapped[int | None] = mapped_column(Integer)
    topic_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"), index=True)
    article_id: Mapped[int | None] = mapped_column(ForeignKey("articles.id", ondelete="SET NULL"), index=True)
    source_url: Mapped[str | None] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    topic: Mapped[Optional["Topic"]] = relationship(back_populates="snippets")
    article: Mapped[Optional["Article"]] = relationship()