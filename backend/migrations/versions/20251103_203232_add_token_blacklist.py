"""add token blacklist table

Revision ID: $(date +%Y%m%d_%H%M%S)
Create Date: $(date +"%Y-%m-%d %H:%M:%S")

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "token_blacklist_001"
down_revision = None  # Will be set to latest migration
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "token_blacklist",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("jti", sa.String(length=36), nullable=False),
        sa.Column("token_type", sa.String(length=10), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("jti")
    )
    op.create_index(op.f("ix_token_blacklist_jti"), "token_blacklist", ["jti"], unique=True)
    
    # Add token_version column to users table if it doesn't exist
    try:
        op.add_column("users", sa.Column("token_version", sa.Integer(), nullable=True, server_default="0"))
    except:
        pass  # Column already exists


def downgrade():
    op.drop_index(op.f("ix_token_blacklist_jti"), table_name="token_blacklist")
    op.drop_table("token_blacklist")
    
    try:
        op.drop_column("users", "token_version")
    except:
        pass
