from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.routers import (
    bookmarks,
    categories,
    explore,
    headlines,
    progress,
    snippets,
    sources,
    tags,
    views,
)

app = FastAPI(
    title="TokenTrail API",
    version="0.1.0",
    description="Backend API for TokenTrail - AI-powered intelligence, discovery, and learning ecosystem."
)

# Register routers
app.include_router(headlines.router)
app.include_router(snippets.router)
app.include_router(explore.router)
app.include_router(progress.router)
app.include_router(categories.router)
app.include_router(sources.router)
app.include_router(tags.router)
app.include_router(bookmarks.router)
app.include_router(views.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
