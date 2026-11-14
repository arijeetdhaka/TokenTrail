
from fastapi import APIRouter

from app.schemas.ai_model import AIModelListResponse

router = APIRouter(
    prefix="/api/explore",
    tags=["Explore AI"]
)


@router.get("/models", response_model=AIModelListResponse)
def get_ai_models():
    return {
        "message": "AI models fetched successfully",
        "data": []
    }
