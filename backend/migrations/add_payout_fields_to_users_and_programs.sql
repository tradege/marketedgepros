-- Migration: Add payout-related fields to users and trading_programs tables
-- Date: 2025-11-04

-- Add financial/payout fields to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS available_balance NUMERIC(12, 2) DEFAULT 0.00,
ADD COLUMN IF NOT EXISTS total_withdrawn NUMERIC(12, 2) DEFAULT 0.00,
ADD COLUMN IF NOT EXISTS payout_count INTEGER DEFAULT 0;

-- Add payout fields to trading_programs table
ALTER TABLE trading_programs
ADD COLUMN IF NOT EXISTS profit_split_percentage NUMERIC(5, 2) DEFAULT 80.00,
ADD COLUMN IF NOT EXISTS minimum_payout_amount NUMERIC(10, 2) DEFAULT 50.00,
ADD COLUMN IF NOT EXISTS payout_mode VARCHAR(50) DEFAULT 'on_demand';

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_available_balance ON users(available_balance);
CREATE INDEX IF NOT EXISTS idx_trading_programs_payout_mode ON trading_programs(payout_mode);

-- Comments
COMMENT ON COLUMN users.available_balance IS 'Available balance for payout requests';
COMMENT ON COLUMN users.total_withdrawn IS 'Total amount withdrawn by user';
COMMENT ON COLUMN users.payout_count IS 'Number of successful payouts';
COMMENT ON COLUMN trading_programs.profit_split_percentage IS 'Percentage of profit split to trader';
COMMENT ON COLUMN trading_programs.minimum_payout_amount IS 'Minimum amount for payout request';
COMMENT ON COLUMN trading_programs.payout_mode IS 'Payout mode: on_demand, on_demand_rules, scheduled';
