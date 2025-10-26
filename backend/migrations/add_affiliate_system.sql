-- Affiliate Program System Migration
-- Creates tables for affiliate links, referrals, commissions, and payouts

-- Affiliate Links Table
CREATE TABLE IF NOT EXISTS affiliate_links (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100),
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    total_revenue NUMERIC(10, 2) DEFAULT 0,
    total_commission NUMERIC(10, 2) DEFAULT 0,
    commission_rate NUMERIC(5, 2) DEFAULT 10.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_click_at TIMESTAMP
);

-- Affiliate Referrals Table
CREATE TABLE IF NOT EXISTS affiliate_referrals (
    id SERIAL PRIMARY KEY,
    affiliate_link_id INTEGER NOT NULL REFERENCES affiliate_links(id) ON DELETE CASCADE,
    affiliate_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    referred_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    landing_page VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending',
    program_id INTEGER REFERENCES trading_programs(id) ON DELETE SET NULL,
    purchase_amount NUMERIC(10, 2),
    commission_amount NUMERIC(10, 2),
    click_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    conversion_date TIMESTAMP
);

-- Affiliate Commissions Table
CREATE TABLE IF NOT EXISTS affiliate_commissions (
    id SERIAL PRIMARY KEY,
    affiliate_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    referral_id INTEGER REFERENCES affiliate_referrals(id) ON DELETE SET NULL,
    amount NUMERIC(10, 2) NOT NULL,
    type VARCHAR(20) DEFAULT 'one_time',
    status VARCHAR(20) DEFAULT 'pending',
    description VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    paid_at TIMESTAMP,
    payout_id INTEGER REFERENCES affiliate_payouts(id) ON DELETE SET NULL
);

-- Affiliate Payouts Table
CREATE TABLE IF NOT EXISTS affiliate_payouts (
    id SERIAL PRIMARY KEY,
    affiliate_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount NUMERIC(10, 2) NOT NULL,
    method VARCHAR(50),
    payment_details JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    notes TEXT,
    transaction_id VARCHAR(100),
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Affiliate Settings Table
CREATE TABLE IF NOT EXISTS affiliate_settings (
    id SERIAL PRIMARY KEY,
    default_commission_rate NUMERIC(5, 2) DEFAULT 10.00,
    min_payout_amount NUMERIC(10, 2) DEFAULT 50.00,
    cookie_duration_days INTEGER DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE,
    auto_approve_affiliates BOOLEAN DEFAULT FALSE,
    auto_approve_commissions BOOLEAN DEFAULT FALSE,
    terms_and_conditions TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add foreign key constraint for commissions -> payouts (circular dependency)
ALTER TABLE affiliate_commissions 
ADD CONSTRAINT fk_commission_payout 
FOREIGN KEY (payout_id) REFERENCES affiliate_payouts(id) ON DELETE SET NULL;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_affiliate_links_user_id ON affiliate_links(user_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_links_code ON affiliate_links(code);
CREATE INDEX IF NOT EXISTS idx_affiliate_referrals_affiliate_link ON affiliate_referrals(affiliate_link_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_referrals_affiliate_user ON affiliate_referrals(affiliate_user_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_referrals_referred_user ON affiliate_referrals(referred_user_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_referrals_status ON affiliate_referrals(status);
CREATE INDEX IF NOT EXISTS idx_affiliate_commissions_affiliate_user ON affiliate_commissions(affiliate_user_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_commissions_status ON affiliate_commissions(status);
CREATE INDEX IF NOT EXISTS idx_affiliate_payouts_affiliate_user ON affiliate_payouts(affiliate_user_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_payouts_status ON affiliate_payouts(status);

-- Insert default settings
INSERT INTO affiliate_settings (
    default_commission_rate,
    min_payout_amount,
    cookie_duration_days,
    is_active,
    auto_approve_affiliates,
    auto_approve_commissions,
    terms_and_conditions
) VALUES (
    10.00,
    50.00,
    30,
    TRUE,
    FALSE,
    FALSE,
    'By participating in the MarketEdgePros Affiliate Program, you agree to promote our services ethically and honestly. Commissions are earned on qualified sales only. Minimum payout is $50. Payments are processed monthly.'
) ON CONFLICT DO NOTHING;

-- Success message
SELECT 'Affiliate system tables created successfully!' as message;

