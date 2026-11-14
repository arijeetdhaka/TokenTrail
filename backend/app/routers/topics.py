from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Topic
from app.schemas.topic import TopicOut

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=list[TopicOut])
def list_topics(domain: str | None = None, db: Session = Depends(get_db)):
    query = select(Topic).order_by(Topic.domain, Topic.name)
    if domain:
        query = query.where(Topic.domain == domain)
    return db.scalars(query).all()


@router.get("/domains", response_model=list[str])
def list_domains(db: Session = Depends(get_db)):
    return db.scalars(select(Topic.domain).distinct().order_by(Topic.domain)).all()


@router.get("/{slug}", response_model=TopicOut)
def get_topic(slug: str, db: Session = Depends(get_db)):
    topic = db.scalar(select(Topic).where(Topic.slug == slug))
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic