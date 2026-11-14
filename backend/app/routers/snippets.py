
from fastapi import APIRouter

from app.schemas.snippet import SnippetListResponse

router = APIRouter(
    prefix="/api/snippets",
    tags=["AI Snippets"]
)


@router.get("/", response_model=SnippetListResponse)
def get_snippets():
    return {
        "message": "Snippets fetched successfully",
        "data": []
    }
