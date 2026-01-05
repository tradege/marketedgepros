"""Add avatar_url to users table

Revision ID: 003
Revises: 002
Create Date: 2025-10-18 17:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add avatar_url column to users table
    op.add_column('users', sa.Column('avatar_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    # Remove avatar_url column from users table
    op.drop_column('users', 'avatar_url')

