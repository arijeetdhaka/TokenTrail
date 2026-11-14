from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user_id
from app.db.database import get_db
from app.models.article import Article
from app.models.ai_model import AIModel
from app.models.bookmark import ArticleBookmark, ModelBookmark, SnippetBookmark
from app.models.profile import Profile
from app.models.snippet import Snippet
from app.schemas.bookmark import (
    ArticleBookmarkListResponse,
    BookmarkActionResponse,
    ModelBookmarkListResponse,
    SnippetBookmarkListResponse,
)

router = APIRouter(
    prefix="/api/bookmarks",
    tags=["Bookmarks"]
)


def _ensure_profile_exists(user_id: UUID, db: Session):
    profile = db.query(Profile).filter(Profile.id == user_id).first()
    if not profile:
        profile = Profile(
            id=user_id,
            username=f"user_{str(user_id)[:8]}",
            display_name="TokenTrail Learner"
        )
        db.add(profile)
        db.commit()
    return profile


# --- Article Bookmarks ---

@router.get("/articles", response_model=ArticleBookmarkListResponse)
def get_article_bookmarks(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    bookmarks = (
        db.query(ArticleBookmark)
        .filter(ArticleBookmark.user_id == user_id)
        .order_by(ArticleBookmark.created_at.desc())
        .all()
    )
    return {
        "message": "Article bookmarks fetched successfully",
        "data": bookmarks
    }


@router.post("/articles/{article_id}", response_model=BookmarkActionResponse)
def toggle_article_bookmark(
    article_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{article_id}' not found"
        )

    _ensure_profile_exists(user_id, db)

    existing = (
        db.query(ArticleBookmark)
        .filter(
            ArticleBookmark.user_id == user_id,
            ArticleBookmark.article_id == article_id
        )
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        return {
            "message": "Article bookmark removed",
            "bookmarked": False
        }
    else:
        new_bookmark = ArticleBookmark(
            user_id=user_id,
            article_id=article_id
        )
        db.add(new_bookmark)
        db.commit()
        return {
            "message": "Article bookmarked successfully",
            "bookmarked": True
        }


# --- Snippet Bookmarks ---

@router.get("/snippets", response_model=SnippetBookmarkListResponse)
def get_snippet_bookmarks(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    bookmarks = (
        db.query(SnippetBookmark)
        .filter(SnippetBookmark.user_id == user_id)
        .order_by(SnippetBookmark.created_at.desc())
        .all()
    )
    return {
        "message": "Snippet bookmarks fetched successfully",
        "data": bookmarks
    }


@router.post("/snippets/{snippet_id}", response_model=BookmarkActionResponse)
def toggle_snippet_bookmark(
    snippet_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    snippet = db.query(Snippet).filter(Snippet.id == snippet_id).first()
    if not snippet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Snippet '{snippet_id}' not found"
        )

    _ensure_profile_exists(user_id, db)

    existing = (
        db.query(SnippetBookmark)
        .filter(
            SnippetBookmark.user_id == user_id,
            SnippetBookmark.snippet_id == snippet_id
        )
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        return {
            "message": "Snippet bookmark removed",
            "bookmarked": False
        }
    else:
        new_bookmark = SnippetBookmark(
            user_id=user_id,
            snippet_id=snippet_id
        )
        db.add(new_bookmark)
        db.commit()
        return {
            "message": "Snippet bookmarked successfully",
            "bookmarked": True
        }


# --- Model Bookmarks ---

@router.get("/models", response_model=ModelBookmarkListResponse)
def get_model_bookmarks(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    bookmarks = (
        db.query(ModelBookmark)
        .filter(ModelBookmark.user_id == user_id)
        .order_by(ModelBookmark.created_at.desc())
        .all()
    )
    return {
        "message": "Model bookmarks fetched successfully",
        "data": bookmarks
    }


@router.post("/models/{model_id}", response_model=BookmarkActionResponse)
def toggle_model_bookmark(
    model_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI model '{model_id}' not found"
        )

    _ensure_profile_exists(user_id, db)

    existing = (
        db.query(ModelBookmark)
        .filter(
            ModelBookmark.user_id == user_id,
            ModelBookmark.model_id == model_id
        )
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        return {
            "message": "Model bookmark removed",
            "bookmarked": False
        }
    else:
        new_bookmark = ModelBookmark(
            user_id=user_id,
            model_id=model_id
        )
        db.add(new_bookmark)
        db.commit()
        return {
            "message": "Model bookmarked successfully",
            "bookmarked": True
        }
