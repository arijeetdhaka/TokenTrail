from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.tag import Tag
from app.schemas.tag import TagListResponse

router = APIRouter(
    prefix="/api/tags",
    tags=["Tags"]
)


@router.get("/", response_model=TagListResponse)
def get_tags(db: Session = Depends(get_db)):
    try:
        tags = db.query(Tag).order_by(Tag.name.asc()).all()
        return {
            "message": "Tags fetched successfully",
            "data": tags
        }
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch tags"
        ) from error
