from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.auth import get_current_user
from app.db.database import get_db
from app.models import (
    Article,
    ArticleCategory,
    ExploreItem,
    ExploreVisit,
    SavedArticle,
    Snippet,
    SnippetRead,
    Topic,
    User,
    UserProgress,
)
from app.schemas.article import ArticleListItem
from app.schemas.progress import ProgressOut, TopicStatusIn
from app.schemas.topic import TopicOut
from app.services.progress import build_progress, mark_topic_explored, recommend_topics

router = APIRouter(prefix="/me", tags=["my progress"])


@router.get("/progress", response_model=ProgressOut)
def get_progress(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return build_progress(db, user.id)


@router.get("/recommendations", response_model=list[TopicOut])
def get_recommendations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return recommend_topics(db, user.id)


@router.get("/saved-articles", response_model=list[ArticleListItem])
def list_saved_articles(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(
        select(Article)
        .join(SavedArticle, SavedArticle.article_id == Article.id)
        .where(SavedArticle.user_id == user.id)
        .options(
            selectinload(Article.source),
            selectinload(Article.category_links).selectinload(ArticleCategory.category),
        )
        .order_by(SavedArticle.saved_at.desc())
    ).all()


@router.put("/saved-articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def save_article(article_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.get(Article, article_id) is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if db.get(SavedArticle, (user.id, article_id)) is None:
        db.add(SavedArticle(user_id=user.id, article_id=article_id))
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/saved-articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def unsave_article(article_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    saved = db.get(SavedArticle, (user.id, article_id))
    if saved is not None:
        db.delete(saved)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/snippets/{snippet_id}/read", status_code=status.HTTP_204_NO_CONTENT)
def mark_snippet_read(snippet_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    snippet = db.get(Snippet, snippet_id)
    if snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    if db.get(SnippetRead, (user.id, snippet_id)) is None:
        db.add(SnippetRead(user_id=user.id, snippet_id=snippet_id))
    mark_topic_explored(db, user.id, snippet.topic_id)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/explore/{item_id}/visit", status_code=status.HTTP_204_NO_CONTENT)
def mark_explore_visited(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(ExploreItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Explore item not found")
    if db.get(ExploreVisit, (user.id, item_id)) is None:
        db.add(ExploreVisit(user_id=user.id, explore_item_id=item_id))
    mark_topic_explored(db, user.id, item.topic_id)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/topics/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def set_topic_status(
    slug: str,
    payload: TopicStatusIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    topic = db.scalar(select(Topic).where(Topic.slug == slug))
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    progress = db.get(UserProgress, (user.id, topic.id))
    if progress is None:
        db.add(UserProgress(user_id=user.id, topic_id=topic.id, status=payload.status))
    else:
        progress.status = payload.status
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)