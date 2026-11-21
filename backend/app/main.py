from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.routers import articles, auth, categories, topics, explore, snippets, ingest

app = FastAPI(title="TokenTrail API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}

app.include_router(articles.router)
app.include_router(categories.router)
app.include_router(topics.router)
app.include_router(snippets.router)
app.include_router(explore.router)
app.include_router(ingest.router)
app.include_router(auth.router)