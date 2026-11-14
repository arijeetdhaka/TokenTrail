from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    # In Supabase, id references auth.users(id).
    # Locally, we keep it as a standalone UUID primary key without an auth.users FK.
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    display_name: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    avatar_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
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
