from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.source import Source
from app.schemas.source import SourceDetailResponse, SourceListResponse

router = APIRouter(
    prefix="/api/sources",
    tags=["Sources"]
)


@router.get("/", response_model=SourceListResponse)
def get_sources(
    source_type: str | None = Query(None, description="Filter by source type"),
    active_only: bool = Query(True, description="Only active sources"),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Source)
        if active_only:
            query = query.filter(Source.is_active.is_(True))
        if source_type:
            query = query.filter(Source.source_type.ilike(source_type))

        sources = query.order_by(Source.name.asc()).all()
        return {
            "message": "Sources fetched successfully",
            "data": sources
        }
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch sources"
        ) from error


@router.get("/{id}", response_model=SourceDetailResponse)
def get_source_by_id(
    id: UUID,
    db: Session = Depends(get_db)
):
    source = db.query(Source).filter(Source.id == id).first()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID '{id}' not found"
        )

    return {
        "message": "Source fetched successfully",
        "data": source
    }
