"""Add performance indexes

Revision ID: 007_add_performance_indexes
Revises: 006_add_hierarchy_and_referral
Create Date: 2025-10-28
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '007_add_performance_indexes'
down_revision = '006_add_hierarchy_and_referral'
branch_labels = None
depends_on = None


def upgrade():
    """Add performance indexes to improve query speed"""
    
    # Commissions table indexes
    op.create_index(
        'ix_commission_agent_status',
        'commissions',
        ['agent_id', 'status'],
        unique=False
    )
    
    op.create_index(
        'ix_commission_created_at',
        'commissions',
        ['created_at'],
        unique=False
    )
    
    # Challenges table indexes
    op.create_index(
        'ix_challenge_user_status',
        'challenges',
        ['user_id', 'status'],
        unique=False
    )
    
    op.create_index(
        'ix_challenge_program_id',
        'challenges',
        ['program_id'],
        unique=False
    )
    
    op.create_index(
        'ix_challenge_created_at',
        'challenges',
        ['created_at'],
        unique=False
    )
    
    # Referrals table indexes
    op.create_index(
        'ix_referral_agent_id',
        'referrals',
        ['agent_id'],
        unique=False
    )
    
    op.create_index(
        'ix_referral_code',
        'referrals',
        ['referral_code'],
        unique=False
    )
    
    op.create_index(
        'ix_referral_status',
        'referrals',
        ['status'],
        unique=False
    )
    
    # Users table indexes (if not already exist)
    try:
        op.create_index(
            'ix_user_email',
            'users',
            ['email'],
            unique=True
        )
    except:
        pass  # Index might already exist
    
    try:
        op.create_index(
            'ix_user_role',
            'users',
            ['role'],
            unique=False
        )
    except:
        pass
    
    # Affiliate links indexes
    try:
        op.create_index(
            'ix_affiliate_link_code',
            'affiliate_links',
            ['code'],
            unique=True
        )
    except:
        pass
    
    try:
        op.create_index(
            'ix_affiliate_link_user_id',
            'affiliate_links',
            ['user_id'],
            unique=False
        )
    except:
        pass


def downgrade():
    """Remove performance indexes"""
    
    # Drop all indexes created in upgrade
    op.drop_index('ix_commission_agent_status', table_name='commissions')
    op.drop_index('ix_commission_created_at', table_name='commissions')
    
    op.drop_index('ix_challenge_user_status', table_name='challenges')
    op.drop_index('ix_challenge_program_id', table_name='challenges')
    op.drop_index('ix_challenge_created_at', table_name='challenges')
    
    op.drop_index('ix_referral_agent_id', table_name='referrals')
    op.drop_index('ix_referral_code', table_name='referrals')
    op.drop_index('ix_referral_status', table_name='referrals')
    
    # Optional indexes
    try:
        op.drop_index('ix_user_email', table_name='users')
    except:
        pass
    
    try:
        op.drop_index('ix_user_role', table_name='users')
    except:
        pass
    
    try:
        op.drop_index('ix_affiliate_link_code', table_name='affiliate_links')
    except:
        pass
    
    try:
        op.drop_index('ix_affiliate_link_user_id', table_name='affiliate_links')
    except:
        pass
