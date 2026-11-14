from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_ingest_key
from app.db.database import get_db
from app.schemas.ingest import ArticleBulkIn, BulkResult, ExploreBulkIn
from app.services.ingest import ingest_articles, ingest_explore_items

router = APIRouter(tags=["ingestion"], dependencies=[Depends(require_ingest_key)])


@router.post("/articles/bulk", response_model=BulkResult)
def bulk_add_articles(payload: ArticleBulkIn, db: Session = Depends(get_db)):
    inserted, skipped = ingest_articles(db, payload.articles)
    db.commit()
    return BulkResult(received=len(payload.articles), inserted=inserted, skipped=skipped)


@router.post("/explore/bulk", response_model=BulkResult)
def bulk_add_explore_items(payload: ExploreBulkIn, db: Session = Depends(get_db)):
    inserted, skipped = ingest_explore_items(db, payload.items)
    db.commit()
    return BulkResult(received=len(payload.items), inserted=inserted, skipped=skipped)