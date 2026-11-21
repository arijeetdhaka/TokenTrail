from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    ExploreItem,
    ExploreVisit,
    SavedArticle,
    Snippet,
    SnippetRead,
    Topic,
    UserProgress,
)


def count(db: Session, query) -> int:
    return db.scalar(select(func.count()).select_from(query.subquery())) or 0


def mark_topic_explored(db: Session, user_id: int, topic_id: int | None) -> None:
    """Record that the user has touched a topic, without downgrading 'learning' or 'completed'."""
    if topic_id is None:
        return
    if db.get(UserProgress, (user_id, topic_id)) is None:
        db.add(UserProgress(user_id=user_id, topic_id=topic_id, status="explored"))


def build_progress(db: Session, user_id: int) -> dict:
    saved_ids = list(db.scalars(select(SavedArticle.article_id).where(SavedArticle.user_id == user_id)))
    read_ids = list(db.scalars(select(SnippetRead.snippet_id).where(SnippetRead.user_id == user_id)))
    visited_ids = list(db.scalars(select(ExploreVisit.explore_item_id).where(ExploreVisit.user_id == user_id)))

    rows = db.execute(
        select(Topic.slug, Topic.name, Topic.domain, UserProgress.status, UserProgress.updated_at)
        .join(UserProgress, UserProgress.topic_id == Topic.id)
        .where(UserProgress.user_id == user_id)
        .order_by(UserProgress.updated_at.desc())
    ).all()
    topics = [
        {"slug": slug, "name": name, "domain": domain, "status": status, "updated_at": updated_at}
        for slug, name, domain, status, updated_at in rows
    ]

    totals = dict(db.execute(select(Topic.domain, func.count()).group_by(Topic.domain)).all())
    explored_by_domain: dict[str, int] = {}
    for topic in topics:
        explored_by_domain[topic["domain"]] = explored_by_domain.get(topic["domain"], 0) + 1
    domains = [
        {"domain": domain, "explored": explored_by_domain.get(domain, 0), "total": total}
        for domain, total in sorted(totals.items())
    ]

    topics_total = sum(totals.values())
    return {
        "overall_percent": round(100 * len(topics) / topics_total) if topics_total else 0,
        "topics_explored": len(topics),
        "topics_total": topics_total,
        "snippets_read": len(read_ids),
        "snippets_total": count(db, select(Snippet.id)),
        "explore_visited": len(visited_ids),
        "explore_total": count(db, select(ExploreItem.id)),
        "saved_articles": len(saved_ids),
        "saved_article_ids": saved_ids,
        "read_snippet_ids": read_ids,
        "visited_explore_ids": visited_ids,
        "domains": domains,
        "topics": topics,
    }


def recommend_topics(db: Session, user_id: int, limit: int = 5) -> list[Topic]:
    """Unexplored topics in domains the user has started; Foundations for a new user."""
    touched = select(UserProgress.topic_id).where(UserProgress.user_id == user_id)
    started_domains = list(
        db.scalars(select(Topic.domain).where(Topic.id.in_(touched)).distinct())
    )
    query = select(Topic).where(Topic.id.not_in(touched)).order_by(Topic.domain, Topic.name).limit(limit)

    if started_domains:
        picks = list(db.scalars(query.where(Topic.domain.in_(started_domains))))
    else:
        picks = list(db.scalars(query.where(Topic.domain == "Foundations")))

    if not picks:
        picks = list(db.scalars(query))
    return picks