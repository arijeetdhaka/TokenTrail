import unittest
from sqlalchemy import inspect
from app.db.database import engine
from app.models import (
    AIModel,
    Article,
    ArticleBookmark,
    ArticleTag,
    ArticleView,
    Category,
    IngestionJob,
    IngestionRun,
    ModelBookmark,
    ModelProvider,
    Profile,
    Snippet,
    SnippetBookmark,
    SnippetTag,
    Source,
    Tag,
    UserActivity,
)


class TestModelsRegistry(unittest.TestCase):
    def test_all_17_models_registered(self):
        inspector = inspect(engine)
        table_names = inspector.get_table_names()

        expected_tables = [
            "categories",
            "sources",
            "articles",
            "snippets",
            "model_providers",
            "ai_models",
            "profiles",
            "article_bookmarks",
            "snippet_bookmarks",
            "model_bookmarks",
            "article_views",
            "user_activity",
            "ingestion_jobs",
            "ingestion_runs",
            "tags",
            "article_tags",
            "snippets_tags",
        ]

        for table in expected_tables:
            self.assertIn(table, table_names, f"Table '{table}' missing from PostgreSQL schema")

    def test_article_tags_column_name_is_tag_at(self):
        inspector = inspect(engine)
        cols = [c["name"] for c in inspector.get_columns("article_tags")]
        self.assertIn("article_id", cols)
        self.assertIn("tag_at", cols)
        self.assertNotIn("tag_id", cols, "article_tags must use 'tag_at', not 'tag_id'")

    def test_snippets_tags_column_name_is_tag_id(self):
        inspector = inspect(engine)
        cols = [c["name"] for c in inspector.get_columns("snippets_tags")]
        self.assertIn("snippet_id", cols)
        self.assertIn("tag_id", cols)

    def test_categories_uuid_pk(self):
        inspector = inspect(engine)
        cols = {c["name"]: str(c["type"]) for c in inspector.get_columns("categories")}
        self.assertIn("id", cols)
        self.assertIn("UUID", cols["id"].upper())
        self.assertIn("slug", cols)
        self.assertIn("description", cols)
        self.assertIn("created_at", cols)


if __name__ == "__main__":
    unittest.main()
