"""Load the starting categories and topics. Safe to run more than once."""
import re

from sqlalchemy import func, select

from app.db.database import SessionLocal
from app.models import Category, Topic

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

        category_count = db.scalar(select(func.count()).select_from(Category))
        topic_count = db.scalar(select(func.count()).select_from(Topic))
        print(f"Categories: {category_count}, Topics: {topic_count}")


if __name__ == "__main__":
    main()