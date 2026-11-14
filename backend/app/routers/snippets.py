from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.snippet import Snippet
from app.schemas.snippet import SnippetDetailResponse, SnippetListResponse

router = APIRouter(
    prefix="/api/snippets",
    tags=["AI Snippets"]
)


@router.get("/", response_model=SnippetListResponse)
def get_snippets(
    category_id: UUID | None = Query(None, description="Filter by category UUID"),
    difficulty: str | None = Query(None, description="Filter by difficulty level"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Snippet).filter(Snippet.is_published.is_(True))

        if category_id:
            query = query.filter(Snippet.category_id == category_id)

        if difficulty:
            query = query.filter(Snippet.difficulty.ilike(difficulty))

        total = query.count()
        snippets = (
            query.order_by(Snippet.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "message": "Snippets fetched successfully",
            "data": snippets,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch snippets"
        ) from error


@router.get("/{id}", response_model=SnippetDetailResponse)
def get_snippet_by_id(
    id: UUID,
    db: Session = Depends(get_db)
):
    snippet = (
        db.query(Snippet)
        .filter(Snippet.id == id, Snippet.is_published.is_(True))
        .first()
    )
    if not snippet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Published snippet with ID '{id}' not found"
        )

    return {
        "message": "Snippet fetched successfully",
        "data": snippet
    }
