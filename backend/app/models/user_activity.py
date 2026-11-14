from datetime import date, datetime
from uuid import UUID

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class UserActivity(Base):
    __tablename__ = "user_activity"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("profiles.id"),
        unique=True,
        nullable=False
    )

    activity_date: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False
    )

    articles_read: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    snippets_viewed: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    models_explored: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    total_read_time: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
