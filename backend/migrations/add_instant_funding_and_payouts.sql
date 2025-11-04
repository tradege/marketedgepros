-- Migration: Add Instant Funding and On-Demand Payouts
-- Date: 2025-11-03

-- 1. Add payout_mode to trading_programs
ALTER TABLE trading_programs 
ADD COLUMN IF NOT EXISTS payout_mode VARCHAR(20) DEFAULT 'standard';
-- Options: 'standard', 'on_demand_full', 'on_demand_rules'

-- 2. Add instant_funding flag to trading_programs
ALTER TABLE trading_programs 
ADD COLUMN IF NOT EXISTS instant_funding BOOLEAN DEFAULT FALSE;

-- 3. Add profit_split_percentage to trading_programs
ALTER TABLE trading_programs 
ADD COLUMN IF NOT EXISTS profit_split_percentage INTEGER DEFAULT 80;
-- Range: 70-100

-- 4. Add minimum_payout_amount to trading_programs
ALTER TABLE trading_programs 
ADD COLUMN IF NOT EXISTS minimum_payout_amount DECIMAL(10,2) DEFAULT 50.00;

-- 5. Add minimum_trading_days to trading_programs
ALTER TABLE trading_programs 
ADD COLUMN IF NOT EXISTS minimum_trading_days INTEGER DEFAULT 0;

-- 6. Create payout_requests table
CREATE TABLE IF NOT EXISTS payout_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    program_id INTEGER REFERENCES trading_programs(id) ON DELETE SET NULL,
    amount DECIMAL(10,2) NOT NULL,
    profit_split_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- Status: pending, approved, processing, paid, rejected, cancelled
    payout_mode VARCHAR(20) NOT NULL,
    -- Mode: on_demand_full, on_demand_rules, standard
    payment_method VARCHAR(50),
    -- Method: bank_wire, crypto, paypal, rise, etc.
    payment_details JSONB,
    request_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_date TIMESTAMP,
    processed_date TIMESTAMP,
    paid_date TIMESTAMP,
    approved_by INTEGER REFERENCES users(id),
    notes TEXT,
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_payout_requests_user_id ON payout_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_payout_requests_status ON payout_requests(status);
CREATE INDEX IF NOT EXISTS idx_payout_requests_request_date ON payout_requests(request_date DESC);

-- 8. Add available_balance to users (for tracking)
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS available_balance DECIMAL(10,2) DEFAULT 0.00;

-- 9. Add total_withdrawn to users
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS total_withdrawn DECIMAL(10,2) DEFAULT 0.00;

-- 10. Add payout_count to users
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS payout_count INTEGER DEFAULT 0;

-- 11. Update existing programs to have default values
UPDATE trading_programs 
SET payout_mode = 'standard',
    instant_funding = FALSE,
    profit_split_percentage = 80,
    minimum_payout_amount = 50.00,
    minimum_trading_days = 14
WHERE payout_mode IS NULL;

COMMENT ON TABLE payout_requests IS 'Stores all payout requests from traders';
COMMENT ON COLUMN payout_requests.payout_mode IS 'on_demand_full: No restrictions, on_demand_rules: With minimum requirements, standard: Bi-weekly';
COMMENT ON COLUMN trading_programs.instant_funding IS 'If true, no evaluation needed - immediate funding';
COMMENT ON COLUMN trading_programs.payout_mode IS 'Determines payout flexibility for this program';

