-- ================================================================
-- MarketEdgePros Commission System Migration
-- Date: 2024-10-30
-- Description: Add commission tracking, payment methods, and withdrawals
-- ================================================================

BEGIN;

-- ================================================================
-- STEP 1: Add new columns to users table
-- ================================================================

-- Commission tracking fields
ALTER TABLE users ADD COLUMN IF NOT EXISTS paid_customers_count INTEGER DEFAULT 0 NOT NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS commission_balance NUMERIC(12,2) DEFAULT 0.00 NOT NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS pending_commission NUMERIC(12,2) DEFAULT 0.00 NOT NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_withdrawal_date TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS can_withdraw BOOLEAN DEFAULT FALSE NOT NULL;

COMMENT ON COLUMN users.paid_customers_count IS 'Number of customers who made a payment (for 10-customer threshold)';
COMMENT ON COLUMN users.commission_balance IS 'Available balance for withdrawal (released commissions)';
COMMENT ON COLUMN users.pending_commission IS 'Locked commissions waiting for 10-customer threshold';
COMMENT ON COLUMN users.last_withdrawal_date IS 'Date of last withdrawal request (for 30-day cooldown)';
COMMENT ON COLUMN users.can_withdraw IS 'Whether user has reached 10-customer threshold and can withdraw';

-- ================================================================
-- STEP 2: Add new columns to commissions table
-- ================================================================

ALTER TABLE commissions ADD COLUMN IF NOT EXISTS released_at TIMESTAMP;
ALTER TABLE commissions ADD COLUMN IF NOT EXISTS customer_id INTEGER REFERENCES users(id) ON DELETE SET NULL;

COMMENT ON COLUMN commissions.released_at IS 'When commission was released from pending to balance (10-customer threshold reached)';
COMMENT ON COLUMN commissions.customer_id IS 'Direct link to customer who made the purchase';

-- Create index for customer lookups
CREATE INDEX IF NOT EXISTS idx_commissions_customer_id ON commissions(customer_id);

-- ================================================================
-- STEP 3: Create payment_methods table
-- ================================================================

CREATE TABLE IF NOT EXISTS payment_methods (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Method type and status
    method_type VARCHAR(20) NOT NULL CHECK (method_type IN ('bank', 'paypal', 'crypto', 'wise')),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    
    -- Bank transfer fields
    bank_name VARCHAR(100),
    account_number VARCHAR(100),
    branch_number VARCHAR(20),
    account_holder_name VARCHAR(100),
    
    -- PayPal fields
    paypal_email VARCHAR(100),
    
    -- Cryptocurrency fields
    crypto_address VARCHAR(200),
    crypto_network VARCHAR(20) CHECK (crypto_network IN ('TRC20', 'ERC20', 'BEP20', NULL)),
    
    -- Wise fields
    wise_email VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

COMMENT ON TABLE payment_methods IS 'User payment methods for commission withdrawals';
COMMENT ON COLUMN payment_methods.method_type IS 'Payment method: bank, paypal, crypto, wise';
COMMENT ON COLUMN payment_methods.is_active IS 'Only one active method per user allowed';

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_payment_methods_user_active ON payment_methods(user_id, is_active);

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_payment_methods_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_payment_methods_updated_at
    BEFORE UPDATE ON payment_methods
    FOR EACH ROW
    EXECUTE FUNCTION update_payment_methods_updated_at();

-- ================================================================
-- STEP 4: Create withdrawals table
-- ================================================================

CREATE TABLE IF NOT EXISTS withdrawals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Withdrawal details
    amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
    method_type VARCHAR(20) NOT NULL,
    payment_details JSONB NOT NULL,
    
    -- Status and notes
    status VARCHAR(20) DEFAULT 'pending' NOT NULL CHECK (status IN ('pending', 'approved', 'paid', 'rejected')),
    notes TEXT,
    
    -- Timestamps
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    approved_at TIMESTAMP,
    paid_at TIMESTAMP,
    rejected_at TIMESTAMP,
    
    -- Admin who approved
    approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL
);

COMMENT ON TABLE withdrawals IS 'Commission withdrawal requests from affiliates/agents';
COMMENT ON COLUMN withdrawals.amount IS 'Withdrawal amount in USD';
COMMENT ON COLUMN withdrawals.payment_details IS 'Snapshot of payment method details at time of request';
COMMENT ON COLUMN withdrawals.status IS 'pending → approved → paid (or rejected)';

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_withdrawals_user_status ON withdrawals(user_id, status);
CREATE INDEX IF NOT EXISTS idx_withdrawals_status ON withdrawals(status);
CREATE INDEX IF NOT EXISTS idx_withdrawals_requested_at ON withdrawals(requested_at DESC);

-- ================================================================
-- STEP 5: Migrate existing commission data (if any)
-- ================================================================

-- Update customer_id in commissions based on referral relationship
UPDATE commissions c
SET customer_id = r.referred_user_id
FROM referrals r
WHERE c.referral_id = r.id
AND c.customer_id IS NULL;

-- Calculate paid_customers_count for existing agents
UPDATE users u
SET paid_customers_count = (
    SELECT COUNT(DISTINCT c.customer_id)
    FROM commissions c
    WHERE c.agent_id = u.id
    AND c.customer_id IS NOT NULL
    AND c.status IN ('approved', 'paid')
)
WHERE u.role IN ('agent', 'master', 'supermaster');

-- Set can_withdraw flag for agents with 10+ customers
UPDATE users
SET can_withdraw = TRUE
WHERE role IN ('agent', 'master', 'supermaster')
AND paid_customers_count >= 10;

-- Calculate commission_balance (sum of approved but not paid commissions)
UPDATE users u
SET commission_balance = COALESCE((
    SELECT SUM(c.commission_amount)
    FROM commissions c
    WHERE c.agent_id = u.id
    AND c.status = 'approved'
), 0)
WHERE u.role IN ('agent', 'master', 'supermaster');

-- Calculate pending_commission (sum of pending commissions for agents under 10 customers)
UPDATE users u
SET pending_commission = COALESCE((
    SELECT SUM(c.commission_amount)
    FROM commissions c
    WHERE c.agent_id = u.id
    AND c.status = 'pending'
), 0)
WHERE u.role IN ('agent', 'master', 'supermaster')
AND u.paid_customers_count < 10;

-- ================================================================
-- STEP 6: Create helper functions
-- ================================================================

-- Function to release pending commissions when agent reaches 10 customers
CREATE OR REPLACE FUNCTION release_pending_commissions(p_agent_id INTEGER)
RETURNS VOID AS $$
DECLARE
    v_pending_total NUMERIC(12,2);
BEGIN
    -- Get total pending commissions
    SELECT COALESCE(SUM(commission_amount), 0)
    INTO v_pending_total
    FROM commissions
    WHERE agent_id = p_agent_id
    AND status = 'pending';
    
    -- Update commissions to released status
    UPDATE commissions
    SET status = 'approved',
        released_at = CURRENT_TIMESTAMP,
        approved_at = CURRENT_TIMESTAMP
    WHERE agent_id = p_agent_id
    AND status = 'pending';
    
    -- Move pending to balance
    UPDATE users
    SET commission_balance = commission_balance + pending_commission,
        pending_commission = 0,
        can_withdraw = TRUE
    WHERE id = p_agent_id;
    
    RAISE NOTICE 'Released % in commissions for agent %', v_pending_total, p_agent_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION release_pending_commissions IS 'Release all pending commissions when agent reaches 10 customers';

-- ================================================================
-- STEP 7: Create trigger to auto-release commissions at 10 customers
-- ================================================================

CREATE OR REPLACE FUNCTION check_commission_threshold()
RETURNS TRIGGER AS $$
BEGIN
    -- If paid_customers_count just reached 10, release commissions
    IF NEW.paid_customers_count >= 10 AND OLD.paid_customers_count < 10 THEN
        PERFORM release_pending_commissions(NEW.id);
        RAISE NOTICE 'Agent % reached 10 customers! Commissions released.', NEW.id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_commission_threshold
    AFTER UPDATE OF paid_customers_count ON users
    FOR EACH ROW
    WHEN (NEW.role IN ('agent', 'master', 'supermaster'))
    EXECUTE FUNCTION check_commission_threshold();

COMMENT ON TRIGGER trigger_commission_threshold ON users IS 'Auto-release commissions when agent reaches 10 customers';

-- ================================================================
-- STEP 8: Verify migration
-- ================================================================

DO $$
DECLARE
    v_users_columns INTEGER;
    v_commissions_columns INTEGER;
    v_payment_methods_exists BOOLEAN;
    v_withdrawals_exists BOOLEAN;
BEGIN
    -- Check users table columns
    SELECT COUNT(*) INTO v_users_columns
    FROM information_schema.columns
    WHERE table_name = 'users'
    AND column_name IN ('paid_customers_count', 'commission_balance', 'pending_commission', 'last_withdrawal_date', 'can_withdraw');
    
    -- Check commissions table columns
    SELECT COUNT(*) INTO v_commissions_columns
    FROM information_schema.columns
    WHERE table_name = 'commissions'
    AND column_name IN ('released_at', 'customer_id');
    
    -- Check payment_methods table
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'payment_methods'
    ) INTO v_payment_methods_exists;
    
    -- Check withdrawals table
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'withdrawals'
    ) INTO v_withdrawals_exists;
    
    -- Report results
    RAISE NOTICE '=== Migration Verification ===';
    RAISE NOTICE 'Users table: % / 5 columns added', v_users_columns;
    RAISE NOTICE 'Commissions table: % / 2 columns added', v_commissions_columns;
    RAISE NOTICE 'Payment methods table: %', CASE WHEN v_payment_methods_exists THEN 'EXISTS' ELSE 'MISSING' END;
    RAISE NOTICE 'Withdrawals table: %', CASE WHEN v_withdrawals_exists THEN 'EXISTS' ELSE 'MISSING' END;
    
    IF v_users_columns = 5 AND v_commissions_columns = 2 AND v_payment_methods_exists AND v_withdrawals_exists THEN
        RAISE NOTICE '✅ Migration completed successfully!';
    ELSE
        RAISE WARNING '⚠️  Migration incomplete! Please review.';
    END IF;
END $$;

COMMIT;

-- ================================================================
-- Migration Complete!
-- ================================================================

