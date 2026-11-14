from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryDetailResponse, CategoryListResponse

router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"]
)


@router.get("/", response_model=CategoryListResponse)
def get_categories(db: Session = Depends(get_db)):
    try:
        categories = db.query(Category).order_by(Category.name.asc()).all()
        return {
            "message": "Categories fetched successfully",
            "data": categories
        }
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch categories"
        ) from error


@router.get("/{slug_or_id}", response_model=CategoryDetailResponse)
def get_category_by_slug_or_id(
    slug_or_id: str,
    db: Session = Depends(get_db)
):
    try:
        parsed_uuid = UUID(slug_or_id)
        category = db.query(Category).filter((Category.id == parsed_uuid) | (Category.slug == slug_or_id)).first()
    except ValueError:
        category = db.query(Category).filter(Category.slug == slug_or_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category '{slug_or_id}' not found"
        )

    return {
        "message": "Category fetched successfully",
        "data": category
    }
