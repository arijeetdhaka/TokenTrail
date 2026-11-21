from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ExploreVisit(Base):
    __tablename__ = "explore_visits"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    explore_item_id: Mapped[int] = mapped_column(ForeignKey("explore_items.id", ondelete="CASCADE"), primary_key=True, index=True)
    visited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())