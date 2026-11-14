from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.db.database import get_db
from app.models import ExploreItem, Topic
from app.schemas.explore_item import ExploreItemOut

router = APIRouter(prefix="/explore", tags=["explore"])


@router.get("", response_model=list[ExploreItemOut])
def list_explore_items(
    item_type: str | None = Query(None, alias="type"),
    topic: str | None = None,
    q: str | None = None,
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = select(ExploreItem).options(selectinload(ExploreItem.topic))
    if item_type:
        query = query.where(ExploreItem.type == item_type)
    if topic:
        query = query.join(Topic).where(Topic.slug == topic)
    if q:
        pattern = f"%{q}%"
        query = query.where(or_(ExploreItem.name.ilike(pattern), ExploreItem.description.ilike(pattern)))
    query = query.order_by(ExploreItem.name).offset(offset).limit(limit)
    return db.scalars(query).all()