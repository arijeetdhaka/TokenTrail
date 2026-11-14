"""complete authoritative schema and update categories to uuid

Revision ID: a1b2c3d4e5f6
Revises: 75b34e731b25
Create Date: 2026-11-14 15:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '75b34e731b25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Update categories table from old Integer PK to authoritative UUID schema.
    # Safe to drop and recreate because table was empty.
    op.drop_table('categories')

    op.create_table(
        'categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # 2. sources table
    op.create_table(
        'sources',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.String(), server_default='', nullable=False),
        sa.Column('website_url', sa.Text(), nullable=True),
        sa.Column('feed_url', sa.Text(), nullable=True),
        sa.Column('source_type', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 3. articles table
    op.create_table(
        'articles',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('original_url', sa.Text(), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('author', sa.String(), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('content_hash', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('original_url')
    )

    # 4. snippets table
    op.create_table(
        'snippets',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('takeaway', sa.Text(), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(), nullable=True),
        sa.Column('estimated_read_time', sa.BigInteger(), nullable=True),
        sa.Column('is_published', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id']),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. model_providers table
    op.create_table(
        'model_providers',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('website_url', sa.Text(), nullable=True),
        sa.Column('logo_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )

    # 6. ai_models table
    op.create_table(
        'ai_models',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('provider_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('model_type', sa.String(), nullable=True),
        sa.Column('pricing_type', sa.String(), nullable=False),
        sa.Column('website_url', sa.Text(), nullable=True),
        sa.Column('documentation_url', sa.Text(), nullable=True),
        sa.Column('release_date', sa.Date(), nullable=True),
        sa.Column('context_window', sa.BigInteger(), nullable=True),
        sa.Column('is_open_source', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['provider_id'], ['model_providers.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # 7. profiles table
    op.create_table(
        'profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('display_name', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.Text(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )

    # 8. article_bookmarks table
    op.create_table(
        'article_bookmarks',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id']),
        sa.ForeignKeyConstraint(['user_id'], ['profiles.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('article_id'),
        sa.UniqueConstraint('user_id')
    )

    # 9. snippet_bookmarks table
    op.create_table(
        'snippet_bookmarks',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('snippet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['snippet_id'], ['snippets.id']),
        sa.ForeignKeyConstraint(['user_id'], ['profiles.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('snippet_id'),
        sa.UniqueConstraint('user_id')
    )

    # 10. model_bookmarks table
    op.create_table(
        'model_bookmarks',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('model_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['model_id'], ['ai_models.id']),
        sa.ForeignKeyConstraint(['user_id'], ['profiles.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('model_id'),
        sa.UniqueConstraint('user_id')
    )

    # 11. article_views table
    op.create_table(
        'article_views',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('viewed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('read_duration', sa.BigInteger(), server_default='0', nullable=False),
        sa.Column('is_completed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id']),
        sa.ForeignKeyConstraint(['user_id'], ['profiles.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # 12. user_activity table
    op.create_table(
        'user_activity',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('activity_date', sa.Date(), nullable=False),
        sa.Column('articles_read', sa.BigInteger(), server_default='0', nullable=False),
        sa.Column('snippets_viewed', sa.BigInteger(), server_default='0', nullable=False),
        sa.Column('models_explored', sa.BigInteger(), server_default='0', nullable=False),
        sa.Column('total_read_time', sa.BigInteger(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['profiles.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('activity_date'),
        sa.UniqueConstraint('user_id')
    )

    # 13. ingestion_jobs table
    op.create_table(
        'ingestion_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('job_type', sa.String(), nullable=False),
        sa.Column('schedule_cron', sa.String(), nullable=False),
        sa.Column('timezone', sa.String(), server_default='utc', nullable=True),
        sa.Column('next_run_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_run_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # 14. ingestion_runs table
    op.create_table(
        'ingestion_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('job_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('items_found', sa.BigInteger(), server_default='0', nullable=False),
        sa.Column('items_added', sa.BigInteger(), server_default='0', nullable=False),
        sa.Column('items_skipped', sa.BigInteger(), server_default='0', nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['ingestion_jobs.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # 15. tags table
    op.create_table(
        'tags',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )

    # 16. article_tags table (composite PK: article_id, tag_at)
    op.create_table(
        'article_tags',
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tag_at', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id']),
        sa.ForeignKeyConstraint(['tag_at'], ['tags.id']),
        sa.PrimaryKeyConstraint('article_id', 'tag_at')
    )

    # 17. snippets_tags table (composite PK: snippet_id, tag_id)
    op.create_table(
        'snippets_tags',
        sa.Column('snippet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tag_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['snippet_id'], ['snippets.id']),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id']),
        sa.PrimaryKeyConstraint('snippet_id', 'tag_id')
    )


def downgrade() -> None:
    # Drop tables in reverse order of foreign key dependencies
    op.drop_table('snippets_tags')
    op.drop_table('article_tags')
    op.drop_table('tags')
    op.drop_table('ingestion_runs')
    op.drop_table('ingestion_jobs')
    op.drop_table('user_activity')
    op.drop_table('article_views')
    op.drop_table('model_bookmarks')
    op.drop_table('snippet_bookmarks')
    op.drop_table('article_bookmarks')
    op.drop_table('profiles')
    op.drop_table('ai_models')
    op.drop_table('model_providers')
    op.drop_table('snippets')
    op.drop_table('articles')
    op.drop_table('sources')
    op.drop_table('categories')

    # Restore the initial categories table from 75b34e731b25
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
