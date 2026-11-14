from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, PrimaryKeyConstraint, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    slug: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )


class ArticleTag(Base):
    __tablename__ = "article_tags"

    # Important schema requirement: column is named tag_at, not tag_id
    article_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("articles.id"),
        nullable=False
    )

    tag_at: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tags.id"),
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint("article_id", "tag_at"),
    )


class SnippetTag(Base):
    __tablename__ = "snippets_tags"

    snippet_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("snippets.id"),
        nullable=False
    )

    tag_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tags.id"),
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint("snippet_id", "tag_id"),
    )
