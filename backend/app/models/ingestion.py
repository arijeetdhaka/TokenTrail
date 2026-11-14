from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
    true
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    source_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("sources.id"),
        nullable=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    job_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    schedule_cron: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    timezone: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        server_default="utc"
    )

    next_run_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    last_run_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    is_active: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        server_default=true()
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now()
    )


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    job_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ingestion_jobs.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    items_found: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    items_added: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    items_skipped: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
