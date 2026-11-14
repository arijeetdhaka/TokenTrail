from datetime import date, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.auth import get_current_user_id
from app.db.database import get_db
from app.models.profile import Profile
from app.models.user_activity import UserActivity
from app.schemas.progress import (
    ActivityRecordRequest,
    ProgressListResponse,
    ProgressResponse,
    ProgressSummaryData,
    ProgressSummaryResponse,
)

router = APIRouter(
    prefix="/api/progress",
    tags=["My Progress"]
)


def _ensure_profile_exists(user_id: UUID, db: Session):
    """
    Ensure a Profile record exists for this user_id in the local database
    to satisfy foreign-key constraints on user_activity and bookmarks.
    """
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


@router.get("/", response_model=ProgressListResponse)
def get_user_progress(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Fetch the activity and learning progress for the currently authenticated user.
    Strictly scoped to the caller's verified user identity.
    """
    try:
        activities = (
            db.query(UserActivity)
            .filter(UserActivity.user_id == user_id)
            .order_by(UserActivity.activity_date.desc())
            .all()
        )

        return {
            "message": "User progress fetched successfully",
            "data": activities
        }

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch user progress"
        ) from error


@router.get("/summary", response_model=ProgressSummaryResponse)
def get_progress_summary(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Fetch aggregate lifetime metrics (articles read, snippets viewed, models explored, total read time).
    """
    try:
        aggregates = (
            db.query(
                func.coalesce(func.sum(UserActivity.articles_read), 0).label("articles"),
                func.coalesce(func.sum(UserActivity.snippets_viewed), 0).label("snippets"),
                func.coalesce(func.sum(UserActivity.models_explored), 0).label("models"),
                func.coalesce(func.sum(UserActivity.total_read_time), 0).label("duration"),
                func.count(UserActivity.id).label("days")
            )
            .filter(UserActivity.user_id == user_id)
            .first()
        )

        summary = ProgressSummaryData(
            total_articles_read=int(aggregates.articles) if aggregates else 0,
            total_snippets_viewed=int(aggregates.snippets) if aggregates else 0,
            total_models_explored=int(aggregates.models) if aggregates else 0,
            total_read_time=int(aggregates.duration) if aggregates else 0,
            days_active=int(aggregates.days) if aggregates else 0,
        )

        return {
            "message": "User progress summary fetched successfully",
            "data": summary
        }

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to calculate user progress summary"
        ) from error


@router.post("/record", response_model=ProgressResponse)
def record_user_activity(
    payload: ActivityRecordRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Record or increment today's activity metrics for the authenticated user.
    """
    try:
        _ensure_profile_exists(user_id, db)
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
            activity.articles_read += payload.articles_read
            activity.snippets_viewed += payload.snippets_viewed
            activity.models_explored += payload.models_explored
            activity.total_read_time += payload.read_duration
            activity.updated_at = datetime.now()
        else:
            activity = UserActivity(
                user_id=user_id,
                activity_date=today,
                articles_read=payload.articles_read,
                snippets_viewed=payload.snippets_viewed,
                models_explored=payload.models_explored,
                total_read_time=payload.read_duration,
            )
            db.add(activity)

        db.commit()
        db.refresh(activity)

        return activity

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to record activity"
        ) from error
