"""Load the starting categories, topics, snippets and explore resources. Safe to run more than once."""
import re

from sqlalchemy import func, select

from app.db.database import SessionLocal
from app.models import Category, ExploreItem, Snippet, Topic
from app.seed_content import RESOURCES, SNIPPETS

CATEGORIES = [
    "AI News", "Machine Learning", "Deep Learning", "Generative AI",
    "Large Language Models", "AI Agents", "Research and Breakthroughs",
    "Open Source AI", "AI Tools and Frameworks", "Computer Vision",
    "Natural Language Processing", "Robotics", "AI Companies and Industry",
    "Model Releases and Updates",
]

TOPICS = {
    "Foundations": ["Mathematics for AI", "Python for AI", "Statistics and Probability", "Data Structures and Algorithms"],
    "Machine Learning": ["Supervised Learning", "Unsupervised Learning", "Regression", "Classification", "Clustering", "Model Evaluation", "Feature Engineering"],
    "Deep Learning": ["Neural Networks", "CNNs", "RNNs", "Transformers", "Optimization"],
    "Generative AI": ["LLMs", "Prompt Engineering", "Embeddings", "Vector Databases", "RAG", "Fine-tuning", "Multimodal AI"],
    "AI Agents": ["Agent Architectures", "Tool Calling", "Planning", "Memory", "Multi-Agent Systems", "Agentic Workflows"],
    "Other AI Domains": ["Computer Vision", "NLP", "Reinforcement Learning", "Robotics", "MLOps", "AI Deployment"],
}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main() -> None:
    with SessionLocal() as db:
        existing_categories = set(db.scalars(select(Category.name)))
        for name in CATEGORIES:
            if name not in existing_categories:
                db.add(Category(name=name))

        existing_slugs = set(db.scalars(select(Topic.slug)))
        for domain, names in TOPICS.items():
            for name in names:
                slug = slugify(name)
                if slug not in existing_slugs:
                    db.add(Topic(name=name, slug=slug, domain=domain))
                    existing_slugs.add(slug)

        db.commit()

        # Snippets and resources point at topics by slug, so look up the ids
        topic_ids = dict(db.execute(select(Topic.slug, Topic.id)).all())
        unknown = {item["topic"] for item in SNIPPETS + RESOURCES if item["topic"] and item["topic"] not in topic_ids}
        if unknown:
            raise SystemExit(f"Unknown topic slugs in seed_content.py: {sorted(unknown)}")

        existing_titles = set(db.scalars(select(Snippet.title)))
        for item in SNIPPETS:
            if item["title"] not in existing_titles:
                db.add(Snippet(
                    title=item["title"],
                    summary=item["summary"],
                    body=item["body"],
                    level=item["level"],
                    read_minutes=item["read_minutes"],
                    topic_id=topic_ids.get(item["topic"]),
                ))

        existing_urls = set(db.scalars(select(ExploreItem.url)))
        for item in RESOURCES:
            if item["url"] not in existing_urls:
                db.add(ExploreItem(
                    name=item["name"],
                    type=item["type"],
                    description=item["description"],
                    url=item["url"],
                    topic_id=topic_ids.get(item["topic"]),
                ))

        db.commit()

        category_count = db.scalar(select(func.count()).select_from(Category))
        topic_count = db.scalar(select(func.count()).select_from(Topic))
        snippet_count = db.scalar(select(func.count()).select_from(Snippet))
        explore_count = db.scalar(select(func.count()).select_from(ExploreItem))
        print(f"Categories: {category_count}, Topics: {topic_count}, Snippets: {snippet_count}, Explore items: {explore_count}")


if __name__ == "__main__":
    main()
