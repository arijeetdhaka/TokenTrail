from datetime import date, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user_id
from app.db.database import get_db
from app.models.article import Article
from app.models.article_view import ArticleView
from app.models.profile import Profile
from app.models.user_activity import UserActivity
from app.schemas.article_view import ArticleViewActionResponse, ArticleViewCreate

router = APIRouter(
    prefix="/api/views",
    tags=["Article Views & Reading Activity"]
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


@router.post("/article", response_model=ArticleViewActionResponse)
def record_article_view(
    payload: ArticleViewCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(Article.id == payload.article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{payload.article_id}' not found"
        )

    _ensure_profile_exists(user_id, db)

    try:
        # 1. Create or update article view record
        view = (
            db.query(ArticleView)
            .filter(
                ArticleView.user_id == user_id,
                ArticleView.article_id == payload.article_id
            )
            .first()
        )

        new_completion = False
        if view:
            view.read_duration += payload.read_duration
            if payload.is_completed and not view.is_completed:
                view.is_completed = True
                new_completion = True
            view.viewed_at = datetime.now()
        else:
            view = ArticleView(
                user_id=user_id,
                article_id=payload.article_id,
                read_duration=payload.read_duration,
                is_completed=payload.is_completed,
            )
            if payload.is_completed:
                new_completion = True
            db.add(view)

        # 2. Update user activity log for today
        today = date.today()
        activity = (
            db.query(UserActivity)
            .filter(
                UserActivity.user_id == user_id,
                UserActivity.activity_date == today
            )
            .first()
        )

        if activity:
            activity.total_read_time += payload.read_duration
            if new_completion:
                activity.articles_read += 1
            activity.updated_at = datetime.now()
        else:
            activity = UserActivity(
                user_id=user_id,
                activity_date=today,
                articles_read=1 if new_completion else 0,
                total_read_time=payload.read_duration,
            )
            db.add(activity)

        db.commit()
        db.refresh(view)

        return {
            "message": "Article view recorded successfully",
            "data": view
        }

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to record article view"
        ) from error
