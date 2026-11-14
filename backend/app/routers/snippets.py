from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.database import get_db
from app.models import Snippet, Topic
from app.schemas.snippet import SnippetOut

router = APIRouter(prefix="/snippets", tags=["snippets"])


@router.get("", response_model=list[SnippetOut])
def list_snippets(
    topic: str | None = None,
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = select(Snippet).options(selectinload(Snippet.topic))
    if topic:
        query = query.join(Topic).where(Topic.slug == topic)
    query = query.order_by(Snippet.created_at.desc(), Snippet.id.desc()).offset(offset).limit(limit)
    return db.scalars(query).all()