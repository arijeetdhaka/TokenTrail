
from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ModelProvider(Base):
    __tablename__ = "model_providers"

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

    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
