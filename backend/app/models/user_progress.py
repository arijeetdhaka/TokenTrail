from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.topic import Topic
    from app.models.user import User


class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (
        CheckConstraint("status IN ('explored', 'learning', 'completed')", name="ck_user_progress_status"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="explored")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="progress")
    topic: Mapped["Topic"] = relationship()