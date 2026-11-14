from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.article import Article
from app.schemas.headline import HeadlineDetailResponse, HeadlineListResponse

router = APIRouter(
    prefix="/api/headlines",
    tags=["AI Headlines"]
)


@router.get("/", response_model=HeadlineListResponse)
def get_headlines(
    category_id: UUID | None = Query(None, description="Filter by category UUID"),
    source_id: UUID | None = Query(None, description="Filter by source UUID"),
    search: str | None = Query(None, min_length=1, max_length=100, description="Search in title or summary"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Article)

        if category_id:
            query = query.filter(Article.category_id == category_id)

        if source_id:
            query = query.filter(Article.source_id == source_id)

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Article.title.ilike(search_filter)) | (Article.summary.ilike(search_filter))
            )

        total = query.count()
        articles = (
            query.order_by(
                Article.published_at.desc().nullslast(),
                Article.created_at.desc().nullslast()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "message": "Headlines fetched successfully",
            "data": articles,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch headlines"
        ) from error


@router.get("/{id}", response_model=HeadlineDetailResponse)
def get_headline_by_id(
    id: UUID,
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Headline with ID '{id}' not found"
        )

    return {
        "message": "Headline fetched successfully",
        "data": article
    }
