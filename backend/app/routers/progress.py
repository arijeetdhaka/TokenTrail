
from fastapi import APIRouter

from app.schemas.progress import ProgressListResponse

router = APIRouter(
    prefix="/api/progress",
    tags=["My Progress"]
)


@router.get("/", response_model=ProgressListResponse)
def get_progress():
    return {
        "message": "Progress fetched successfully",
        "data": []
    }
