from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, func, false
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ArticleView(Base):
    __tablename__ = "article_views"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("profiles.id"),
        nullable=False
    )

    article_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("articles.id"),
        nullable=False
    )

    viewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    read_duration: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )
