-- ============================================================
-- Commission System Migration
-- MarketEdgePros - Prop Trading Firm Platform
-- ============================================================

-- Add commission tracking fields to users table
ALTER TABLE users
ADD COLUMN IF NOT EXISTS commission_rate FLOAT DEFAULT 20.0 NOT NULL,
ADD COLUMN IF NOT EXISTS paid_customers_count INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN IF NOT EXISTS commission_balance FLOAT DEFAULT 0.0 NOT NULL,
ADD COLUMN IF NOT EXISTS pending_commission FLOAT DEFAULT 0.0 NOT NULL,
ADD COLUMN IF NOT EXISTS last_withdrawal_date TIMESTAMP NULL,
ADD COLUMN IF NOT EXISTS can_withdraw BOOLEAN DEFAULT FALSE NOT NULL;

-- Add comments to new columns
COMMENT ON COLUMN users.commission_rate IS 'Percentage commission rate (e.g., 20 = 20%)';
COMMENT ON COLUMN users.paid_customers_count IS 'Number of customers who have made payments';
COMMENT ON COLUMN users.commission_balance IS 'Available commission balance for withdrawal';
COMMENT ON COLUMN users.pending_commission IS 'Commission waiting for 10 customers threshold';
COMMENT ON COLUMN users.last_withdrawal_date IS 'Date of last withdrawal request';
COMMENT ON COLUMN users.can_withdraw IS 'Whether user is eligible to withdraw (reached 10 customers)';

-- ============================================================
-- Create commissions table
-- ============================================================
CREATE TABLE IF NOT EXISTS commissions (
    id SERIAL PRIMARY KEY,
    affiliate_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    customer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    order_id VARCHAR(100) NOT NULL,
    
    amount FLOAT NOT NULL,
    commission_rate FLOAT NOT NULL,
    
    status VARCHAR(20) DEFAULT 'pending' NOT NULL CHECK (status IN ('pending', 'released', 'paid')),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    released_at TIMESTAMP NULL,
    paid_at TIMESTAMP NULL,
    
    CONSTRAINT commissions_amount_positive CHECK (amount >= 0),
    CONSTRAINT commissions_rate_valid CHECK (commission_rate >= 0 AND commission_rate <= 100)
);

-- Add indexes for commissions table
CREATE INDEX IF NOT EXISTS idx_commissions_affiliate_status ON commissions(affiliate_id, status);
CREATE INDEX IF NOT EXISTS idx_commissions_customer ON commissions(customer_id);
CREATE INDEX IF NOT EXISTS idx_commissions_order ON commissions(order_id);
CREATE INDEX IF NOT EXISTS idx_commissions_created_at ON commissions(created_at DESC);

-- Add comments
COMMENT ON TABLE commissions IS 'Tracks commission earnings for affiliates';
COMMENT ON COLUMN commissions.status IS 'pending: waiting for threshold, released: available for withdrawal, paid: withdrawn';

-- ============================================================
-- Create payment_methods table
-- ============================================================
CREATE TABLE IF NOT EXISTS payment_methods (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    method_type VARCHAR(20) NOT NULL CHECK (method_type IN ('bank', 'paypal', 'crypto', 'wise')),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    
    -- Bank transfer fields
    bank_name VARCHAR(100) NULL,
    account_number VARCHAR(100) NULL,
    branch_number VARCHAR(20) NULL,
    account_holder_name VARCHAR(100) NULL,
    
    -- PayPal fields
    paypal_email VARCHAR(100) NULL,
    
    -- Cryptocurrency fields
    crypto_address VARCHAR(200) NULL,
    crypto_network VARCHAR(20) NULL CHECK (crypto_network IS NULL OR crypto_network IN ('TRC20', 'ERC20')),
    
    -- Wise fields
    wise_email VARCHAR(100) NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Add indexes for payment_methods table
CREATE INDEX IF NOT EXISTS idx_payment_methods_user_active ON payment_methods(user_id, is_active);

-- Add comments
COMMENT ON TABLE payment_methods IS 'User payment methods for receiving withdrawals';
COMMENT ON COLUMN payment_methods.method_type IS 'Type of payment method: bank, paypal, crypto, wise';

-- ============================================================
-- Create withdrawals table
-- ============================================================
CREATE TABLE IF NOT EXISTS withdrawals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    amount FLOAT NOT NULL,
    method_type VARCHAR(20) NOT NULL,
    payment_details JSONB NOT NULL,
    
    status VARCHAR(20) DEFAULT 'pending' NOT NULL CHECK (status IN ('pending', 'approved', 'paid', 'rejected')),
    notes TEXT NULL,
    
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    approved_at TIMESTAMP NULL,
    paid_at TIMESTAMP NULL,
    rejected_at TIMESTAMP NULL,
    
    approved_by INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    
    CONSTRAINT withdrawals_amount_positive CHECK (amount > 0)
);

-- Add indexes for withdrawals table
CREATE INDEX IF NOT EXISTS idx_withdrawals_user_status ON withdrawals(user_id, status);
CREATE INDEX IF NOT EXISTS idx_withdrawals_status ON withdrawals(status);
CREATE INDEX IF NOT EXISTS idx_withdrawals_requested_at ON withdrawals(requested_at DESC);

-- Add comments
COMMENT ON TABLE withdrawals IS 'Withdrawal requests from affiliates';
COMMENT ON COLUMN withdrawals.status IS 'pending: awaiting approval, approved: approved but not paid, paid: completed, rejected: denied';
COMMENT ON COLUMN withdrawals.payment_details IS 'Snapshot of payment method details at time of request';

-- ============================================================
-- Create trigger to update updated_at timestamp
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_payment_methods_updated_at
    BEFORE UPDATE ON payment_methods
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- Sample data for testing (optional - comment out for production)
-- ============================================================

-- Update existing affiliates with default commission rate
-- UPDATE users SET commission_rate = 20.0 WHERE role = 'affiliate';

-- ============================================================
-- Verification queries
-- ============================================================

-- Check if all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('commissions', 'payment_methods', 'withdrawals');

-- Check if user columns were added
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'users'
AND column_name IN ('commission_rate', 'paid_customers_count', 'commission_balance', 'pending_commission', 'last_withdrawal_date', 'can_withdraw');

-- ============================================================
-- Rollback script (use with caution!)
-- ============================================================

/*
-- Drop tables
DROP TABLE IF EXISTS withdrawals CASCADE;
DROP TABLE IF EXISTS payment_methods CASCADE;
DROP TABLE IF EXISTS commissions CASCADE;

-- Remove columns from users table
ALTER TABLE users
DROP COLUMN IF EXISTS commission_rate,
DROP COLUMN IF EXISTS paid_customers_count,
DROP COLUMN IF EXISTS commission_balance,
DROP COLUMN IF EXISTS pending_commission,
DROP COLUMN IF EXISTS last_withdrawal_date,
DROP COLUMN IF EXISTS can_withdraw;

-- Drop trigger and function
DROP TRIGGER IF EXISTS update_payment_methods_updated_at ON payment_methods;
DROP FUNCTION IF EXISTS update_updated_at_column();
*/

