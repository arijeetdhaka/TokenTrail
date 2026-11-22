"""Give a topic to every explore item that doesn't have one yet. Safe to run more than once.

Run with: python -m app.link_topics
"""
from sqlalchemy import select

from app.db.database import SessionLocal
from app.models import ExploreItem, Topic
from app.services.topic_matcher import match_topic


def main() -> None:
    with SessionLocal() as db:
        topic_ids = dict(db.execute(select(Topic.slug, Topic.id)).all())
        items = db.scalars(select(ExploreItem).where(ExploreItem.topic_id.is_(None))).all()

        linked = 0
        for item in items:
            topic_id = topic_ids.get(match_topic(item.name, item.description))
            if topic_id:
                item.topic_id = topic_id
                linked += 1

        db.commit()
        print(f"Explore items without a topic: {len(items)}, linked now: {linked}, still unmatched: {len(items) - linked}")


if __name__ == "__main__":
    main()
