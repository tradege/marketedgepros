"""Add code column to email_verification_tokens and password_reset_tokens

Revision ID: 004
Revises: 003
Create Date: 2025-10-18 17:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add code column to email_verification_tokens table
    op.add_column('email_verification_tokens', sa.Column('code', sa.String(length=6), nullable=True))
    op.create_index(op.f('ix_email_verification_tokens_code'), 'email_verification_tokens', ['code'], unique=False)
    
    # Add code column to password_reset_tokens table
    op.add_column('password_reset_tokens', sa.Column('code', sa.String(length=6), nullable=True))
    op.create_index(op.f('ix_password_reset_tokens_code'), 'password_reset_tokens', ['code'], unique=False)


def downgrade() -> None:
    # Remove code column from password_reset_tokens table
    op.drop_index(op.f('ix_password_reset_tokens_code'), table_name='password_reset_tokens')
    op.drop_column('password_reset_tokens', 'code')
    
    # Remove code column from email_verification_tokens table
    op.drop_index(op.f('ix_email_verification_tokens_code'), table_name='email_verification_tokens')
    op.drop_column('email_verification_tokens', 'code')

