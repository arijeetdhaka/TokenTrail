
from datetime import date, datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
    false,
    true
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AIModel(Base):
    __tablename__ = "ai_models"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    provider_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("model_providers.id"),
        nullable=True
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    slug: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_type: Mapped[str | None] = mapped_column(String, nullable=True)

    pricing_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    documentation_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    release_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    context_window: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    is_open_source: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=true()
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
