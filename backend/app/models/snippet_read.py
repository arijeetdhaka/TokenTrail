from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class SnippetRead(Base):
    __tablename__ = "snippet_reads"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    snippet_id: Mapped[int] = mapped_column(ForeignKey("snippets.id", ondelete="CASCADE"), primary_key=True, index=True)
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())