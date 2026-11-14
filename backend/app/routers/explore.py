from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.ai_model import AIModel
from app.models.model_provider import ModelProvider
from app.schemas.ai_model import (
    AIModelDetailResponse,
    AIModelListResponse,
    ModelProviderListResponse,
)

router = APIRouter(
    prefix="/api/explore",
    tags=["Explore AI"]
)


@router.get("/models", response_model=AIModelListResponse)
def get_ai_models(
    provider_id: UUID | None = Query(None, description="Filter by provider UUID"),
    model_type: str | None = Query(None, description="Filter by model type (e.g. LLM, Vision)"),
    pricing_type: str | None = Query(None, description="Filter by pricing (e.g. free, paid, api)"),
    is_open_source: bool | None = Query(None, description="Filter open source models"),
    search: str | None = Query(None, min_length=1, max_length=100, description="Search name or description"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(AIModel).filter(AIModel.is_active.is_(True))

        if provider_id:
            query = query.filter(AIModel.provider_id == provider_id)

        if model_type:
            query = query.filter(AIModel.model_type.ilike(model_type))

        if pricing_type:
            query = query.filter(AIModel.pricing_type.ilike(pricing_type))

        if is_open_source is not None:
            query = query.filter(AIModel.is_open_source.is_(is_open_source))

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (AIModel.name.ilike(search_filter)) | (AIModel.description.ilike(search_filter))
            )

        total = query.count()
        models = (
            query.order_by(AIModel.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "message": "AI models fetched successfully",
            "data": models,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch AI models"
        ) from error


@router.get("/models/{slug_or_id}", response_model=AIModelDetailResponse)
def get_ai_model_by_slug_or_id(
    slug_or_id: str,
    db: Session = Depends(get_db)
):
    query = db.query(AIModel).filter(AIModel.is_active.is_(True))

    try:
        parsed_uuid = UUID(slug_or_id)
        model = query.filter((AIModel.id == parsed_uuid) | (AIModel.slug == slug_or_id)).first()
    except ValueError:
        model = query.filter(AIModel.slug == slug_or_id).first()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Active AI model '{slug_or_id}' not found"
        )

    return {
        "message": "AI model fetched successfully",
        "data": model
    }


@router.get("/providers", response_model=ModelProviderListResponse)
def get_model_providers(db: Session = Depends(get_db)):
    try:
        providers = db.query(ModelProvider).order_by(ModelProvider.name.asc()).all()
        return {
            "message": "Model providers fetched successfully",
            "data": providers
        }
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch model providers"
        ) from error
