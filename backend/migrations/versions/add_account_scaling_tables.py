"""Add account scaling tables

Revision ID: 20251110_191500
Revises: 20251103_203232
Create Date: 2025-11-10 19:15:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251110_191500'
down_revision = '007_add_performance_indexes'
branch_labels = None
depends_on = None


def upgrade():
    # Create account_scaling table
    op.create_table(
        'account_scaling',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('current_tier', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('current_account_size', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('next_tier', sa.Integer(), nullable=True),
        sa.Column('next_account_size', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('total_profit', sa.Numeric(precision=12, scale=2), nullable=False, server_default='0'),
        sa.Column('target_profit', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('progress_percentage', sa.Numeric(precision=5, scale=2), nullable=True, server_default='0'),
        sa.Column('times_scaled', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_scaled_at', sa.DateTime(), nullable=True),
        sa.Column('is_eligible_for_scaling', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('eligibility_checked_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for account_scaling
    op.create_index('ix_account_scaling_user_id', 'account_scaling', ['user_id'], unique=False)
    op.create_index('ix_account_scaling_status', 'account_scaling', ['status'], unique=False)
    op.create_index('ix_account_scaling_eligible', 'account_scaling', ['is_eligible_for_scaling'], unique=False)
    
    # Create scaling_tiers table
    op.create_table(
        'scaling_tiers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('tier_number', sa.Integer(), nullable=False),
        sa.Column('account_size', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('profit_target', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('minimum_trading_days', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('minimum_trades', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('profit_split', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'tier_number', name='uq_tenant_tier')
    )
    
    # Create indexes for scaling_tiers
    op.create_index('ix_scaling_tier_tenant_tier', 'scaling_tiers', ['tenant_id', 'tier_number'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_scaling_tier_tenant_tier', table_name='scaling_tiers')
    op.drop_index('ix_account_scaling_eligible', table_name='account_scaling')
    op.drop_index('ix_account_scaling_status', table_name='account_scaling')
    op.drop_index('ix_account_scaling_user_id', table_name='account_scaling')
    
    # Drop tables
    op.drop_table('scaling_tiers')
    op.drop_table('account_scaling')
