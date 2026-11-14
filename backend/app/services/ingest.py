import hashlib
import html
import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Article, ExploreItem, Source
from app.schemas.ingest import ArticleIn, ExploreItemIn

SUMMARY_LIMIT = 400


def clean_text(raw: str | None) -> str:
    """Remove HTML tags and extra spaces."""
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def short_summary(text: str) -> str | None:
    """Use the feed's own text as a first summary, cut at a word boundary."""
    if not text:
        return None
    if len(text) <= SUMMARY_LIMIT:
        return text
    return text[:SUMMARY_LIMIT].rsplit(" ", 1)[0] + "..."


def content_hash(title: str, text: str) -> str:
    return hashlib.sha256(f"{title}\n{text}".lower().encode("utf-8")).hexdigest()


def get_or_create_source(db: Session, cache: dict[str, Source], name: str, url: str) -> Source:
    if url in cache:
        return cache[url]
    source = db.scalar(select(Source).where(Source.url == url))
    if source is None:
        source = db.scalar(select(Source).where(Source.name == name))
    if source is None:
        source = Source(name=name, url=url, type="rss")
        db.add(source)
    cache[url] = source
    return source


def ingest_articles(db: Session, items: list[ArticleIn]) -> tuple[int, int]:
    prepared = []
    for item in items:
        title = item.title.strip()
        text = clean_text(item.summary)
        prepared.append((item, title, text, content_hash(title, text)))

    urls = [item.url.strip() for item, _, _, _ in prepared]
    hashes = [digest for _, _, _, digest in prepared]
    seen_urls = set(db.scalars(select(Article.url).where(Article.url.in_(urls))))
    seen_hashes = set(db.scalars(select(Article.content_hash).where(Article.content_hash.in_(hashes))))

    sources: dict[str, Source] = {}
    inserted = skipped = 0
    for item, title, text, digest in prepared:
        url = item.url.strip()
        if url in seen_urls or digest in seen_hashes:
            skipped += 1
            continue
        source = get_or_create_source(db, sources, item.source.strip(), item.source_url.strip())
        db.add(
            Article(
                source=source,
                title=title,
                url=url,
                published_at=item.published_at,
                raw_text=text or None,
                summary=short_summary(text),
                content_hash=digest,
            )
        )
        seen_urls.add(url)
        seen_hashes.add(digest)
        inserted += 1
    return inserted, skipped


def ingest_explore_items(db: Session, items: list[ExploreItemIn]) -> tuple[int, int]:
    urls = [item.url.strip() for item in items]
    seen_urls = set(db.scalars(select(ExploreItem.url).where(ExploreItem.url.in_(urls))))

    inserted = skipped = 0
    for item in items:
        url = item.url.strip()
        if url in seen_urls:
            skipped += 1
            continue
        db.add(
            ExploreItem(
                type=item.type,
                name=clean_text(item.name)[:200],
                description=clean_text(item.description) or None,
                url=url,
            )
        )
        seen_urls.add(url)
        inserted += 1
    return inserted, skipped