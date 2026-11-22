from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.models import Article, ArticleCategory, ArticleTopic, Category, Topic
from app.schemas.classify import ClassificationIn, ClassifyError


def apply_classifications(db: Session, results: list[ClassificationIn]) -> tuple[int, list[ClassifyError]]:
    """Save NLP results. Replaces each article's categories and topics, so re-running never duplicates."""
    article_ids = {r.article_id for r in results}
    existing_articles = set(db.scalars(select(Article.id).where(Article.id.in_(article_ids))))
    valid_categories = set(db.scalars(select(Category.id)))
    valid_topics = set(db.scalars(select(Topic.id)))

    updated = 0
    errors: list[ClassifyError] = []

    for result in results:
        if result.article_id not in existing_articles:
            errors.append(ClassifyError(article_id=result.article_id, reason="article not found"))
            continue

        # One score per id: if an id is sent twice, the last one wins
        categories = {c.category_id: c.confidence for c in result.categories or []}
        topics = {t.topic_id: t.relevance for t in result.topics or []}

        unknown_categories = sorted(set(categories) - valid_categories)
        unknown_topics = sorted(set(topics) - valid_topics)
        if unknown_categories or unknown_topics:
            reason = "unknown category_id " + str(unknown_categories) if unknown_categories else "unknown topic_id " + str(unknown_topics)
            errors.append(ClassifyError(article_id=result.article_id, reason=reason))
            continue

        # None = leave as it is, [] = clear, a list = replace
        if result.categories is not None:
            db.execute(delete(ArticleCategory).where(ArticleCategory.article_id == result.article_id))
            if categories:
                db.execute(insert(ArticleCategory), [
                    {"article_id": result.article_id, "category_id": cid, "confidence": score}
                    for cid, score in categories.items()
                ])

        if result.topics is not None:
            db.execute(delete(ArticleTopic).where(ArticleTopic.article_id == result.article_id))
            if topics:
                db.execute(insert(ArticleTopic), [
                    {"article_id": result.article_id, "topic_id": tid, "relevance": score}
                    for tid, score in topics.items()
                ])

        if result.takeaways is not None:
            takeaways = [t.strip() for t in result.takeaways if t.strip()]
            db.execute(update(Article).where(Article.id == result.article_id).values(takeaways=takeaways or None))

        updated += 1

    return updated, errors