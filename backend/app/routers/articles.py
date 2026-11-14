from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.db.database import get_db
from app.models import Article, ArticleCategory, ArticleTopic
from app.schemas.article import ArticleDetail, ArticlePage

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=ArticlePage)
def list_articles(
    category_id: int | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = select(Article)
    if category_id is not None:
        query = query.join(ArticleCategory).where(ArticleCategory.category_id == category_id)

    total = db.scalar(select(func.count()).select_from(query.subquery()))

    articles = db.scalars(
        query.options(
            selectinload(Article.source),
            selectinload(Article.category_links).selectinload(ArticleCategory.category),
        )
        .order_by(Article.published_at.desc().nulls_last(), Article.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return {"items": articles, "total": total, "page": page, "page_size": page_size}


@router.get("/{article_id}", response_model=ArticleDetail)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.scalar(
        select(Article)
        .where(Article.id == article_id)
        .options(
            selectinload(Article.source),
            selectinload(Article.category_links).selectinload(ArticleCategory.category),
            selectinload(Article.topic_links).selectinload(ArticleTopic.topic),
        )
    )
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article