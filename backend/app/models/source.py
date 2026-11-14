
from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default=""
    )

    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    feed_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    source_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="true"
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
