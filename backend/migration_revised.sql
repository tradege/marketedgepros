-- ================================================================
-- MarketEdgePros Commission System Migration (REVISED)
-- Date: 2024-10-30
-- Description: Add 10-customer threshold system to existing agent structure
-- ================================================================

BEGIN;

-- ================================================================
-- STEP 1: Add new columns to agents table
-- ================================================================

-- Add paid customers count for 10-customer threshold
ALTER TABLE agents ADD COLUMN IF NOT EXISTS paid_customers_count INTEGER DEFAULT 0 NOT NULL;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS can_withdraw BOOLEAN DEFAULT FALSE NOT NULL;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS last_withdrawal_date TIMESTAMP;

COMMENT ON COLUMN agents.paid_customers_count IS 'Number of customers who made a payment (for 10-customer threshold)';
COMMENT ON COLUMN agents.can_withdraw IS 'Whether agent has reached 10-customer threshold and can withdraw';
COMMENT ON COLUMN agents.last_withdrawal_date IS 'Date of last withdrawal request (for 30-day cooldown)';

-- ================================================================
-- STEP 2: Rename pending_balance to match our system
-- ================================================================

-- Note: agents.pending_balance already exists and serves the same purpose
-- We'll just add a comment to clarify
COMMENT ON COLUMN agents.pending_balance IS 'Locked commissions waiting for 10-customer threshold (or available if threshold reached)';

-- ================================================================
-- STEP 3: Add new columns to commissions table
-- ================================================================

ALTER TABLE commissions ADD COLUMN IF NOT EXISTS released_at TIMESTAMP;
ALTER TABLE commissions ADD COLUMN IF NOT EXISTS customer_id INTEGER REFERENCES users(id) ON DELETE SET NULL;

COMMENT ON COLUMN commissions.released_at IS 'When commission was released from pending (10-customer threshold reached)';
COMMENT ON COLUMN commissions.customer_id IS 'Direct link to customer who made the purchase';

-- Create index for customer lookups
CREATE INDEX IF NOT EXISTS idx_commissions_customer_id ON commissions(customer_id);

-- ================================================================
-- STEP 4: Create payment_methods table
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
-- STEP 5: Add columns to existing withdrawals table
-- ================================================================

-- Add requested_at if it doesn't exist
ALTER TABLE withdrawals ADD COLUMN IF NOT EXISTS requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Add payment_details as JSONB if it's currently JSON
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'withdrawals'
        AND column_name = 'payment_details'
        AND data_type = 'json'
    ) THEN
        ALTER TABLE withdrawals ALTER COLUMN payment_details TYPE JSONB USING payment_details::jsonb;
    END IF;
END $$;

-- ================================================================
-- STEP 6: Migrate existing data
-- ================================================================

-- Update customer_id in commissions based on referral relationship
UPDATE commissions c
SET customer_id = r.referred_user_id
FROM referrals r
WHERE c.referral_id = r.id
AND c.customer_id IS NULL;

-- Calculate paid_customers_count for existing agents
UPDATE agents a
SET paid_customers_count = (
    SELECT COUNT(DISTINCT c.customer_id)
    FROM commissions c
    WHERE c.agent_id = a.id
    AND c.customer_id IS NOT NULL
    AND c.status IN ('approved', 'paid')
)
WHERE a.is_active = TRUE;

-- Set can_withdraw flag for agents with 10+ customers
UPDATE agents
SET can_withdraw = TRUE
WHERE is_active = TRUE
AND paid_customers_count >= 10;

-- For agents under 10 customers, their pending_balance should remain locked
-- For agents with 10+ customers, their pending_balance is available
-- (This is already handled by can_withdraw flag)

-- ================================================================
-- STEP 7: Create helper function to release commissions
-- ================================================================

CREATE OR REPLACE FUNCTION release_pending_commissions(p_agent_id INTEGER)
RETURNS VOID AS $$
BEGIN
    -- Update commissions to released status
    UPDATE commissions
    SET status = 'approved',
        released_at = CURRENT_TIMESTAMP,
        approved_at = CURRENT_TIMESTAMP
    WHERE agent_id = p_agent_id
    AND status = 'pending';
    
    -- Set can_withdraw flag
    UPDATE agents
    SET can_withdraw = TRUE
    WHERE id = p_agent_id;
    
    RAISE NOTICE 'Released pending commissions for agent %', p_agent_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION release_pending_commissions IS 'Release all pending commissions when agent reaches 10 customers';

-- ================================================================
-- STEP 8: Create trigger to auto-release at 10 customers
-- ================================================================

CREATE OR REPLACE FUNCTION check_agent_commission_threshold()
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

DROP TRIGGER IF EXISTS trigger_agent_commission_threshold ON agents;

CREATE TRIGGER trigger_agent_commission_threshold
    AFTER UPDATE OF paid_customers_count ON agents
    FOR EACH ROW
    WHEN (NEW.is_active = TRUE)
    EXECUTE FUNCTION check_agent_commission_threshold();

COMMENT ON TRIGGER trigger_agent_commission_threshold ON agents IS 'Auto-release commissions when agent reaches 10 customers';

-- ================================================================
-- STEP 9: Create view for agent dashboard stats
-- ================================================================

CREATE OR REPLACE VIEW agent_dashboard_stats AS
SELECT 
    a.id as agent_id,
    a.user_id,
    a.agent_code,
    a.commission_rate,
    a.paid_customers_count,
    a.can_withdraw,
    a.pending_balance,
    a.total_earned,
    a.total_withdrawn,
    a.last_withdrawal_date,
    CASE 
        WHEN a.paid_customers_count >= 10 THEN a.pending_balance
        ELSE 0
    END as available_balance,
    CASE 
        WHEN a.paid_customers_count < 10 THEN a.pending_balance
        ELSE 0
    END as locked_balance,
    a.referral_count,
    a.active_referrals,
    COALESCE(pending_commissions.count, 0) as pending_commission_count,
    COALESCE(pending_commissions.amount, 0) as pending_commission_amount
FROM agents a
LEFT JOIN (
    SELECT 
        agent_id,
        COUNT(*) as count,
        SUM(commission_amount) as amount
    FROM commissions
    WHERE status = 'pending'
    GROUP BY agent_id
) pending_commissions ON a.id = pending_commissions.agent_id;

COMMENT ON VIEW agent_dashboard_stats IS 'Comprehensive agent statistics for dashboard';

-- ================================================================
-- STEP 10: Verify migration
-- ================================================================

DO $$
DECLARE
    v_agents_columns INTEGER;
    v_commissions_columns INTEGER;
    v_payment_methods_exists BOOLEAN;
    v_function_exists BOOLEAN;
    v_trigger_exists BOOLEAN;
BEGIN
    -- Check agents table columns
    SELECT COUNT(*) INTO v_agents_columns
    FROM information_schema.columns
    WHERE table_name = 'agents'
    AND column_name IN ('paid_customers_count', 'can_withdraw', 'last_withdrawal_date');
    
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
    
    -- Check function exists
    SELECT EXISTS (
        SELECT 1 FROM pg_proc
        WHERE proname = 'release_pending_commissions'
    ) INTO v_function_exists;
    
    -- Check trigger exists
    SELECT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'trigger_agent_commission_threshold'
    ) INTO v_trigger_exists;
    
    -- Report results
    RAISE NOTICE '=== Migration Verification ===';
    RAISE NOTICE 'Agents table: % / 3 columns added', v_agents_columns;
    RAISE NOTICE 'Commissions table: % / 2 columns added', v_commissions_columns;
    RAISE NOTICE 'Payment methods table: %', CASE WHEN v_payment_methods_exists THEN '✅ EXISTS' ELSE '❌ MISSING' END;
    RAISE NOTICE 'Release function: %', CASE WHEN v_function_exists THEN '✅ EXISTS' ELSE '❌ MISSING' END;
    RAISE NOTICE 'Auto-release trigger: %', CASE WHEN v_trigger_exists THEN '✅ EXISTS' ELSE '❌ MISSING' END;
    
    IF v_agents_columns = 3 AND v_commissions_columns = 2 AND v_payment_methods_exists AND v_function_exists AND v_trigger_exists THEN
        RAISE NOTICE '✅ Migration completed successfully!';
    ELSE
        RAISE WARNING '⚠️  Migration incomplete! Please review.';
    END IF;
END $$;

COMMIT;

-- ================================================================
-- Migration Complete!
-- ================================================================

