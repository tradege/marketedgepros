#!/usr/bin/env python3
"""Create analytics and marketing tables"""

from src.app import app
from src.database import db
from sqlalchemy import text

with app.app_context():
    sql = '''
    -- Revenue Analytics
    CREATE TABLE IF NOT EXISTS revenue_analytics (
        id SERIAL PRIMARY KEY,
        date DATE NOT NULL UNIQUE,
        total_revenue DECIMAL(12,2) DEFAULT 0,
        challenge_revenue DECIMAL(12,2) DEFAULT 0,
        net_revenue DECIMAL(12,2) DEFAULT 0,
        transaction_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Referrals
    CREATE TABLE IF NOT EXISTS referrals (
        id SERIAL PRIMARY KEY,
        referrer_id INTEGER REFERENCES users(id),
        referred_id INTEGER REFERENCES users(id),
        referral_code VARCHAR(50) UNIQUE,
        status VARCHAR(20) DEFAULT 'pending',
        reward_value DECIMAL(10,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);
    CREATE INDEX IF NOT EXISTS idx_referrals_code ON referrals(referral_code);

    -- Affiliates
    CREATE TABLE IF NOT EXISTS affiliates (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) UNIQUE,
        affiliate_code VARCHAR(50) UNIQUE NOT NULL,
        commission_rate DECIMAL(5,2) DEFAULT 10.00,
        total_earnings DECIMAL(12,2) DEFAULT 0,
        pending_earnings DECIMAL(12,2) DEFAULT 0,
        paid_earnings DECIMAL(12,2) DEFAULT 0,
        total_referrals INTEGER DEFAULT 0,
        status VARCHAR(20) DEFAULT 'active',
        payment_method VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Affiliate Commissions
    CREATE TABLE IF NOT EXISTS affiliate_commissions (
        id SERIAL PRIMARY KEY,
        affiliate_id INTEGER REFERENCES affiliates(id),
        user_id INTEGER REFERENCES users(id),
        transaction_id INTEGER,
        amount DECIMAL(10,2) NOT NULL,
        commission_amount DECIMAL(10,2),
        status VARCHAR(20) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_affiliate_comm_affiliate ON affiliate_commissions(affiliate_id);
    CREATE INDEX IF NOT EXISTS idx_affiliate_comm_status ON affiliate_commissions(status);

    -- Email Templates
    CREATE TABLE IF NOT EXISTS email_templates (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        subject VARCHAR(200),
        html_content TEXT,
        category VARCHAR(50),
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    
    try:
        with db.engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
        print('✅ All tables created successfully!')
    except Exception as e:
        print(f'❌ Error: {e}')
