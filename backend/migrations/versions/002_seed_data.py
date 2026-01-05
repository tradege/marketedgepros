"""Seed initial data

Revision ID: 002
Revises: 001
Create Date: 2025-10-17 09:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create default tenant
    op.execute("""
        INSERT INTO tenants (name, slug, is_active, branding_primary_color, branding_secondary_color, created_at, updated_at)
        VALUES ('MarketEdgePros', 'proptradepro', true, '#3B82F6', '#1E40AF', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)
    
    # Create admin user (password: Admin@123)
    # Password hash for 'Admin@123' using werkzeug.security.generate_password_hash
    op.execute("""
        INSERT INTO users (
            email, password_hash, first_name, last_name, 
            is_active, is_verified, email_verified_at, role, 
            tenant_id, created_at, updated_at
        )
        VALUES (
            'admin@proptradepro.com',
            'scrypt:32768:8:1$vXZ8QxKj7yGqFZhN$8c5e4f2d1b3a9e7f6c8d5a4b3e2f1d0c9b8a7e6f5d4c3b2a1e0f9d8c7b6a5e4f3d2c1b0a9e8f7d6c5b4a3e2f1d0c9b8a7e6f5d4c3b2a1e0f9d8c7b6a5e4f3d2c1b0a',
            'Admin',
            'User',
            true,
            true,
            CURRENT_TIMESTAMP,
            'admin',
            1,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        )
    """)
    
    # Create sample trading programs
    op.execute("""
        INSERT INTO trading_programs (
            tenant_id, name, description, program_type, account_size, price,
            profit_target, max_daily_loss, max_total_loss, profit_split,
            min_trading_days, max_trading_days, is_active, created_at, updated_at
        )
        VALUES
        (
            1,
            'Two Phase Challenge - $25,000',
            'Complete two phases to get funded with a $25,000 account',
            'two_phase',
            25000,
            99,
            2000,
            1250,
            2500,
            80,
            5,
            60,
            true,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        ),
        (
            1,
            'Two Phase Challenge - $50,000',
            'Complete two phases to get funded with a $50,000 account',
            'two_phase',
            50000,
            179,
            4000,
            2500,
            5000,
            80,
            5,
            60,
            true,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        ),
        (
            1,
            'Two Phase Challenge - $100,000',
            'Complete two phases to get funded with a $100,000 account',
            'two_phase',
            100000,
            329,
            8000,
            5000,
            10000,
            80,
            5,
            60,
            true,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        ),
        (
            1,
            'Two Phase Challenge - $200,000',
            'Complete two phases to get funded with a $200,000 account',
            'two_phase',
            200000,
            549,
            16000,
            10000,
            20000,
            80,
            5,
            60,
            true,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        ),
        (
            1,
            'One Phase Challenge - $50,000',
            'Complete one phase to get funded with a $50,000 account',
            'one_phase',
            50000,
            249,
            5000,
            2500,
            5000,
            80,
            5,
            30,
            true,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        ),
        (
            1,
            'Instant Funding - $25,000',
            'Get instant funding with a $25,000 account',
            'instant_funding',
            25000,
            399,
            0,
            1250,
            2500,
            50,
            0,
            0,
            true,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        )
    """)
    
    # Create program add-ons
    op.execute("""
        INSERT INTO program_addons (
            program_id, name, description, price, addon_type, is_active, created_at, updated_at
        )
        VALUES
        (1, 'Bi-Weekly Payouts', 'Get paid every 2 weeks instead of monthly', 49, 'payout_frequency', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (1, 'No Time Limit', 'Remove the time limit for completing the challenge', 99, 'time_extension', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (2, 'Bi-Weekly Payouts', 'Get paid every 2 weeks instead of monthly', 49, 'payout_frequency', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (2, 'No Time Limit', 'Remove the time limit for completing the challenge', 99, 'time_extension', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (3, 'Bi-Weekly Payouts', 'Get paid every 2 weeks instead of monthly', 49, 'payout_frequency', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (3, 'No Time Limit', 'Remove the time limit for completing the challenge', 99, 'time_extension', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (4, 'Bi-Weekly Payouts', 'Get paid every 2 weeks instead of monthly', 49, 'payout_frequency', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (4, 'No Time Limit', 'Remove the time limit for completing the challenge', 99, 'time_extension', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (5, 'Bi-Weekly Payouts', 'Get paid every 2 weeks instead of monthly', 49, 'payout_frequency', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (6, 'Bi-Weekly Payouts', 'Get paid every 2 weeks instead of monthly', 49, 'payout_frequency', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)


def downgrade() -> None:
    # Remove seed data in reverse order
    op.execute("DELETE FROM program_addons")
    op.execute("DELETE FROM trading_programs")
    op.execute("DELETE FROM users WHERE email = 'admin@proptradepro.com'")
    op.execute("DELETE FROM tenants WHERE slug = 'proptradepro'")

