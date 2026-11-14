import os
import unittest
from datetime import date, datetime
from uuid import uuid4

# Set TESTING environment variable for safe test authorization
os.environ["TESTING"] = "true"

from fastapi.testclient import TestClient
from app.db.database import SessionLocal
from app.main import app
from app.models.ai_model import AIModel
from app.models.article import Article
from app.models.article_view import ArticleView
from app.models.bookmark import ArticleBookmark, ModelBookmark, SnippetBookmark
from app.models.category import Category
from app.models.model_provider import ModelProvider
from app.models.profile import Profile
from app.models.snippet import Snippet
from app.models.source import Source
from app.models.tag import Tag
from app.models.user_activity import UserActivity


class TestTokenTrailAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.db = SessionLocal()
        cls.test_user_id = uuid4()

        # Create a test profile in DB
        cls.profile = Profile(
            id=cls.test_user_id,
            username=f"testuser_{str(cls.test_user_id)[:8]}",
            display_name="Test User",
            bio="API test profile"
        )
        cls.db.add(cls.profile)

        # Create a test category
        cls.category = Category(
            name="AI Research",
            slug=f"ai-research-{str(uuid4())[:8]}",
            description="Frontier AI news and papers"
        )
        cls.db.add(cls.category)

        # Create a test source
        cls.source = Source(
            name="TechRadar AI",
            source_type="rss",
            website_url="https://techradar.com",
            is_active=True
        )
        cls.db.add(cls.source)

        cls.db.commit()
        cls.db.refresh(cls.category)
        cls.db.refresh(cls.source)

        # Create test article
        cls.article = Article(
            source_id=cls.source.id,
            category_id=cls.category.id,
            title="Google Introduces Gemini 3.8",
            summary="Next-generation reasoning model released with enhanced capabilities.",
            content="Full text content of the article...",
            original_url=f"https://techradar.com/news/{str(uuid4())[:8]}",
            author="Tech Desk",
            published_at=datetime.now()
        )
        cls.db.add(cls.article)

        # Create test snippet
        cls.snippet = Snippet(
            category_id=cls.category.id,
            title="Understanding Transformer Attention",
            content="Self-attention allows tokens to attend to other tokens in parallel.",
            takeaway="Attention mechanisms eliminate recurrence bottlenecks.",
            difficulty="intermediate",
            estimated_read_time=3,
            is_published=True
        )
        cls.db.add(cls.snippet)

        # Create test provider & model
        cls.provider = ModelProvider(
            name=f"DeepMind {str(uuid4())[:6]}",
            slug=f"deepmind-{str(uuid4())[:6]}",
            website_url="https://deepmind.google"
        )
        cls.db.add(cls.provider)
        cls.db.commit()
        cls.db.refresh(cls.provider)

        cls.model = AIModel(
            provider_id=cls.provider.id,
            name="Gemini 3.8 Flash",
            slug=f"gemini-38-flash-{str(uuid4())[:6]}",
            description="Ultra-fast multithreaded reasoning model.",
            model_type="Multimodal LLM",
            pricing_type="freemium",
            is_open_source=False,
            is_active=True
        )
        cls.db.add(cls.model)

        # Create test tag
        cls.tag = Tag(
            name=f"Transformers_{str(uuid4())[:6]}",
            slug=f"transformers-{str(uuid4())[:6]}"
        )
        cls.db.add(cls.tag)

        cls.db.commit()
        cls.db.refresh(cls.article)
        cls.db.refresh(cls.snippet)
        cls.db.refresh(cls.model)
        cls.db.refresh(cls.tag)

    @classmethod
    def tearDownClass(cls):
        try:
            # Clean up all created test entities in strict reverse dependency order
            cls.db.query(ArticleView).filter(ArticleView.user_id == cls.test_user_id).delete()
            cls.db.query(ArticleBookmark).filter(ArticleBookmark.user_id == cls.test_user_id).delete()
            cls.db.query(SnippetBookmark).filter(SnippetBookmark.user_id == cls.test_user_id).delete()
            cls.db.query(ModelBookmark).filter(ModelBookmark.user_id == cls.test_user_id).delete()
            cls.db.query(UserActivity).filter(UserActivity.user_id == cls.test_user_id).delete()

            cls.db.query(Snippet).filter(Snippet.id == cls.snippet.id).delete()
            cls.db.query(Article).filter(Article.id == cls.article.id).delete()
            cls.db.query(AIModel).filter(AIModel.id == cls.model.id).delete()
            cls.db.query(ModelProvider).filter(ModelProvider.id == cls.provider.id).delete()
            cls.db.query(Source).filter(Source.id == cls.source.id).delete()
            cls.db.query(Category).filter(Category.id == cls.category.id).delete()
            cls.db.query(Tag).filter(Tag.id == cls.tag.id).delete()
            cls.db.query(Profile).filter(Profile.id == cls.test_user_id).delete()
            cls.db.commit()
        finally:
            cls.db.close()

    def test_01_health_check(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["database"], "connected")

    def test_02_headlines_list(self):
        resp = self.client.get("/api/headlines/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("message", data)
        self.assertIn("data", data)
        self.assertTrue(len(data["data"]) >= 1)
        # Verify expected fields from prompt
        first = next((h for h in data["data"] if h["id"] == str(self.article.id)), None)
        self.assertIsNotNone(first)
        self.assertEqual(first["title"], "Google Introduces Gemini 3.8")
        self.assertIn("summary", first)
        self.assertIn("original_url", first)
        self.assertIn("author", first)
        self.assertIn("published_at", first)

    def test_03_headline_detail(self):
        resp = self.client.get(f"/api/headlines/{self.article.id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["data"]
        self.assertEqual(data["id"], str(self.article.id))
        self.assertEqual(data["title"], "Google Introduces Gemini 3.8")

    def test_04_headline_not_found(self):
        random_id = uuid4()
        resp = self.client.get(f"/api/headlines/{random_id}")
        self.assertEqual(resp.status_code, 404)

    def test_05_headline_invalid_uuid(self):
        resp = self.client.get("/api/headlines/not-a-valid-uuid")
        self.assertEqual(resp.status_code, 422)

    def test_06_snippets_list(self):
        resp = self.client.get("/api/snippets/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("data", data)
        first = next((s for s in data["data"] if s["id"] == str(self.snippet.id)), None)
        self.assertIsNotNone(first)
        self.assertEqual(first["title"], "Understanding Transformer Attention")
        self.assertTrue(first["is_published"])

    def test_07_snippet_detail(self):
        resp = self.client.get(f"/api/snippets/{self.snippet.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["data"]["title"], "Understanding Transformer Attention")

    def test_08_explore_models_list(self):
        resp = self.client.get("/api/explore/models")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("data", data)
        found = any(m["id"] == str(self.model.id) for m in data["data"])
        self.assertTrue(found)

    def test_09_explore_model_by_slug(self):
        resp = self.client.get(f"/api/explore/models/{self.model.slug}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["data"]["name"], "Gemini 3.8 Flash")

    def test_10_explore_providers(self):
        resp = self.client.get("/api/explore/providers")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        found = any(p["id"] == str(self.provider.id) for p in data["data"])
        self.assertTrue(found)

    def test_11_categories_list_and_detail(self):
        resp = self.client.get("/api/categories/")
        self.assertEqual(resp.status_code, 200)
        found = any(c["id"] == str(self.category.id) for c in resp.json()["data"])
        self.assertTrue(found)

        detail_resp = self.client.get(f"/api/categories/{self.category.slug}")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertEqual(detail_resp.json()["data"]["name"], "AI Research")

    def test_12_sources_list(self):
        resp = self.client.get("/api/sources/")
        self.assertEqual(resp.status_code, 200)
        found = any(s["id"] == str(self.source.id) for s in resp.json()["data"])
        self.assertTrue(found)

    def test_13_tags_list(self):
        resp = self.client.get("/api/tags/")
        self.assertEqual(resp.status_code, 200)
        found = any(t["id"] == str(self.tag.id) for t in resp.json()["data"])
        self.assertTrue(found)

    def test_14_auth_enforcement_on_protected_endpoints(self):
        # Without credentials, protected endpoints must return 401 Unauthorized
        endpoints = [
            ("GET", "/api/progress/"),
            ("GET", "/api/progress/summary"),
            ("POST", "/api/progress/record"),
            ("GET", "/api/bookmarks/articles"),
            ("POST", f"/api/bookmarks/articles/{self.article.id}"),
            ("GET", "/api/bookmarks/snippets"),
            ("POST", f"/api/bookmarks/snippets/{self.snippet.id}"),
            ("GET", "/api/bookmarks/models"),
            ("POST", f"/api/bookmarks/models/{self.model.id}"),
            ("POST", "/api/views/article"),
        ]
        for method, endpoint in endpoints:
            if method == "GET":
                r = self.client.get(endpoint)
            else:
                r = self.client.post(endpoint, json={})
            self.assertEqual(
                r.status_code, 401,
                f"Expected 401 for unauthenticated {method} {endpoint}, got {r.status_code}"
            )

    def test_15_bookmarks_flow(self):
        headers = {"X-Test-User-Id": str(self.test_user_id)}

        # 1. Bookmark article
        resp1 = self.client.post(f"/api/bookmarks/articles/{self.article.id}", headers=headers)
        self.assertEqual(resp1.status_code, 200)
        self.assertTrue(resp1.json()["bookmarked"])

        # 2. Verify in list
        list_resp = self.client.get("/api/bookmarks/articles", headers=headers)
        self.assertEqual(list_resp.status_code, 200)
        self.assertEqual(len(list_resp.json()["data"]), 1)
        self.assertEqual(list_resp.json()["data"][0]["article_id"], str(self.article.id))

        # 3. Toggle off
        resp2 = self.client.post(f"/api/bookmarks/articles/{self.article.id}", headers=headers)
        self.assertEqual(resp2.status_code, 200)
        self.assertFalse(resp2.json()["bookmarked"])

        # 4. Verify list is empty
        list_resp2 = self.client.get("/api/bookmarks/articles", headers=headers)
        self.assertEqual(len(list_resp2.json()["data"]), 0)

    def test_16_reading_views_and_progress_flow(self):
        headers = {"X-Test-User-Id": str(self.test_user_id)}

        # 1. Record reading view for article
        view_resp = self.client.post(
            "/api/views/article",
            headers=headers,
            json={
                "article_id": str(self.article.id),
                "read_duration": 120,
                "is_completed": True
            }
        )
        self.assertEqual(view_resp.status_code, 200)
        self.assertEqual(view_resp.json()["data"]["read_duration"], 120)
        self.assertTrue(view_resp.json()["data"]["is_completed"])

        # 2. Check user progress
        prog_resp = self.client.get("/api/progress/", headers=headers)
        self.assertEqual(prog_resp.status_code, 200)
        activities = prog_resp.json()["data"]
        self.assertTrue(len(activities) >= 1)
        today_activity = next((a for a in activities if a["activity_date"] == str(date.today())), None)
        self.assertIsNotNone(today_activity)
        self.assertTrue(today_activity["articles_read"] >= 1)
        self.assertTrue(today_activity["total_read_time"] >= 120)

        # 3. Check progress summary
        sum_resp = self.client.get("/api/progress/summary", headers=headers)
        self.assertEqual(sum_resp.status_code, 200)
        summary = sum_resp.json()["data"]
        self.assertTrue(summary["total_articles_read"] >= 1)
        self.assertTrue(summary["total_read_time"] >= 120)
        self.assertTrue(summary["days_active"] >= 1)


if __name__ == "__main__":
    unittest.main()
