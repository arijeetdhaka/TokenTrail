
from fastapi import APIRouter

from app.schemas.headline import HeadlineListResponse

router = APIRouter(
    prefix="/api/headlines",
    tags=["AI Headlines"]
)


@router.get("/", response_model=HeadlineListResponse)
def get_headlines():
    return {
        "message": "Headlines fetched successfully",
        "data": []
    }
