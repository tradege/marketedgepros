-- Support System Migration
-- Creates tables for support tickets, messages, and FAQ

-- =====================================================
-- 1. Support Tickets Table
-- =====================================================

CREATE TABLE IF NOT EXISTS support_tickets (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(20) UNIQUE NOT NULL,
    
    -- User info
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(200) NOT NULL,
    
    -- Ticket details
    subject VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'open',
    
    -- Assignment
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    
    -- Attachments
    attachments TEXT,
    
    -- Tracking
    first_response_at TIMESTAMP,
    resolved_at TIMESTAMP,
    closed_at TIMESTAMP,
    
    -- Ratings
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes for support_tickets
CREATE INDEX IF NOT EXISTS idx_support_tickets_ticket_number ON support_tickets(ticket_number);
CREATE INDEX IF NOT EXISTS idx_support_tickets_user_id ON support_tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_support_tickets_email ON support_tickets(email);
CREATE INDEX IF NOT EXISTS idx_support_tickets_category ON support_tickets(category);
CREATE INDEX IF NOT EXISTS idx_support_tickets_priority ON support_tickets(priority);
CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON support_tickets(status);
CREATE INDEX IF NOT EXISTS idx_support_tickets_assigned_to ON support_tickets(assigned_to);
CREATE INDEX IF NOT EXISTS idx_support_tickets_created_at ON support_tickets(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_support_tickets_status_priority ON support_tickets(status, priority);

-- =====================================================
-- 2. Ticket Messages Table
-- =====================================================

CREATE TABLE IF NOT EXISTS ticket_messages (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES support_tickets(id) ON DELETE CASCADE NOT NULL,
    
    -- Message details
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    email VARCHAR(255),
    name VARCHAR(200),
    message TEXT NOT NULL,
    is_staff BOOLEAN DEFAULT FALSE,
    is_internal BOOLEAN DEFAULT FALSE,
    
    -- Attachments
    attachments TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes for ticket_messages
CREATE INDEX IF NOT EXISTS idx_ticket_messages_ticket_id ON ticket_messages(ticket_id);
CREATE INDEX IF NOT EXISTS idx_ticket_messages_user_id ON ticket_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_ticket_messages_created_at ON ticket_messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ticket_messages_is_staff ON ticket_messages(is_staff);

-- =====================================================
-- 3. FAQs Table
-- =====================================================

CREATE TABLE IF NOT EXISTS faqs (
    id SERIAL PRIMARY KEY,
    
    -- Content
    question VARCHAR(500) NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    
    -- Display
    "order" INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT FALSE,
    is_published BOOLEAN DEFAULT TRUE,
    
    -- Tracking
    view_count INTEGER DEFAULT 0,
    helpful_count INTEGER DEFAULT 0,
    not_helpful_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes for faqs
CREATE INDEX IF NOT EXISTS idx_faqs_category ON faqs(category);
CREATE INDEX IF NOT EXISTS idx_faqs_is_published ON faqs(is_published);
CREATE INDEX IF NOT EXISTS idx_faqs_is_featured ON faqs(is_featured);
CREATE INDEX IF NOT EXISTS idx_faqs_order ON faqs("order");
CREATE INDEX IF NOT EXISTS idx_faqs_category_order ON faqs(category, "order");

-- =====================================================
-- 4. Triggers for auto-update timestamps
-- =====================================================

-- Trigger for support_tickets
CREATE OR REPLACE FUNCTION update_support_tickets_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_support_tickets_updated_at ON support_tickets;
CREATE TRIGGER trigger_update_support_tickets_updated_at
    BEFORE UPDATE ON support_tickets
    FOR EACH ROW
    EXECUTE FUNCTION update_support_tickets_updated_at();

-- Trigger for faqs
CREATE OR REPLACE FUNCTION update_faqs_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_faqs_updated_at ON faqs;
CREATE TRIGGER trigger_update_faqs_updated_at
    BEFORE UPDATE ON faqs
    FOR EACH ROW
    EXECUTE FUNCTION update_faqs_updated_at();

-- =====================================================
-- 5. Sample FAQs
-- =====================================================

INSERT INTO faqs (question, answer, category, "order", is_featured, is_published) VALUES
    (
        'How do I get started with MarketEdgePros?',
        '<p>Getting started is easy! Follow these steps:</p><ol><li>Create your free account</li><li>Complete your profile and KYC verification</li><li>Choose a challenge program that fits your goals</li><li>Make your payment and receive your trading credentials</li><li>Start trading and pass your evaluation!</li></ol><p>Need help? Our support team is here 24/7.</p>',
        'getting_started',
        1,
        TRUE,
        TRUE
    ),
    (
        'What are the trading rules for prop firm challenges?',
        '<p>Our challenges have clear and fair rules:</p><ul><li><strong>Daily Loss Limit:</strong> Maximum 5% loss per day</li><li><strong>Max Drawdown:</strong> 10% total drawdown limit</li><li><strong>Profit Target:</strong> 8-10% depending on your program</li><li><strong>Trading Days:</strong> Minimum 5 trading days required</li><li><strong>Allowed Instruments:</strong> Forex, indices, commodities, and crypto</li></ul><p>Always trade within the rules to ensure your challenge success!</p>',
        'trading',
        2,
        TRUE,
        TRUE
    ),
    (
        'How long does KYC verification take?',
        '<p>KYC verification typically takes 24-48 hours. To speed up the process:</p><ul><li>Upload clear, high-quality documents</li><li>Ensure all information matches your ID exactly</li><li>Provide both proof of identity and proof of address</li></ul><p>You''ll receive an email once your verification is complete.</p>',
        'account',
        3,
        TRUE,
        TRUE
    ),
    (
        'When can I withdraw my profits?',
        '<p>Profit withdrawals are available:</p><ul><li><strong>First Payout:</strong> After 14 days of funded trading</li><li><strong>Regular Payouts:</strong> Bi-weekly (every 2 weeks)</li><li><strong>Processing Time:</strong> 1-3 business days</li><li><strong>Methods:</strong> Bank transfer, crypto, or e-wallet</li></ul><p>Minimum withdrawal amount is $100.</p>',
        'payments',
        4,
        TRUE,
        TRUE
    ),
    (
        'What payment methods do you accept?',
        '<p>We accept multiple payment methods for your convenience:</p><ul><li>Credit/Debit Cards (Visa, Mastercard)</li><li>Cryptocurrency (Bitcoin, Ethereum, USDT)</li><li>Bank Transfer</li><li>E-wallets (PayPal, Skrill, Neteller)</li></ul><p>All payments are processed securely through our payment partners.</p>',
        'payments',
        5,
        FALSE,
        TRUE
    ),
    (
        'Can I use Expert Advisors (EAs) or trading bots?',
        '<p>Yes! You can use Expert Advisors and trading bots with these conditions:</p><ul><li>No high-frequency scalping (HFT)</li><li>No tick scalping or arbitrage strategies</li><li>No copy trading from external sources</li><li>All trading must comply with our risk rules</li></ul><p>If you''re unsure about your EA, contact support before using it.</p>',
        'trading',
        6,
        FALSE,
        TRUE
    ),
    (
        'What happens if I fail my challenge?',
        '<p>Don''t worry! Failing a challenge is a learning opportunity:</p><ul><li>You can purchase a new challenge at any time</li><li>We offer discount codes for retry attempts</li><li>Review your trading statistics to improve</li><li>Consider our free trading course for better preparation</li></ul><p>Many successful traders fail their first attempt - persistence is key!</p>',
        'trading',
        7,
        FALSE,
        TRUE
    ),
    (
        'How do I reset my password?',
        '<p>To reset your password:</p><ol><li>Go to the login page</li><li>Click "Forgot Password"</li><li>Enter your registered email address</li><li>Check your email for the reset link</li><li>Follow the link and create a new password</li></ol><p>If you don''t receive the email within 5 minutes, check your spam folder or contact support.</p>',
        'account',
        8,
        FALSE,
        TRUE
    ),
    (
        'Is my trading data and personal information secure?',
        '<p>Absolutely! We take security seriously:</p><ul><li>SSL encryption for all data transmission</li><li>Secure database storage with regular backups</li><li>Compliance with GDPR and data protection laws</li><li>Two-factor authentication (2FA) available</li><li>Regular security audits and updates</li></ul><p>Your data is never shared with third parties without your consent.</p>',
        'technical',
        9,
        FALSE,
        TRUE
    ),
    (
        'Can I trade during news events?',
        '<p>Yes, you can trade during news events, but be cautious:</p><ul><li>High volatility can lead to rapid losses</li><li>Spreads may widen significantly</li><li>Ensure you have proper risk management in place</li><li>Consider avoiding major news if you''re close to your limits</li></ul><p>Many successful traders avoid high-impact news to protect their accounts.</p>',
        'trading',
        10,
        FALSE,
        TRUE
    );

-- =====================================================
-- Migration Complete
-- =====================================================

SELECT 'Support system migration completed successfully!' AS status;
SELECT COUNT(*) AS faq_count FROM faqs;

