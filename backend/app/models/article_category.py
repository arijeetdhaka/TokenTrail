from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.category import Category


class ArticleCategory(Base):
    __tablename__ = "article_categories"

    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True, index=True)
    confidence: Mapped[float | None] = mapped_column(Float)

    article: Mapped["Article"] = relationship(back_populates="category_links")
    category: Mapped["Category"] = relationship(back_populates="article_links")