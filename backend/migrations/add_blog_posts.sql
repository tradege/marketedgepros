-- Migration: Add blog_posts table
-- Description: Create blog_posts table for content management system
-- Date: 2025-10-26

-- Create blog_posts table
CREATE TABLE IF NOT EXISTS blog_posts (
    id SERIAL PRIMARY KEY,
    
    -- Content
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(250) UNIQUE NOT NULL,
    excerpt TEXT,
    content TEXT NOT NULL,
    
    -- Media
    featured_image VARCHAR(500),
    featured_image_alt VARCHAR(200),
    
    -- Categorization
    category VARCHAR(50) NOT NULL,
    tags VARCHAR(500),
    
    -- SEO
    meta_title VARCHAR(200),
    meta_description VARCHAR(300),
    meta_keywords VARCHAR(500),
    
    -- Author & Publishing
    author_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    published_at TIMESTAMP,
    
    -- Engagement
    view_count INTEGER DEFAULT 0,
    featured BOOLEAN DEFAULT FALSE,
    reading_time INTEGER DEFAULT 5,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_blog_posts_category ON blog_posts(category);
CREATE INDEX IF NOT EXISTS idx_blog_posts_status ON blog_posts(status);
CREATE INDEX IF NOT EXISTS idx_blog_posts_author_id ON blog_posts(author_id);
CREATE INDEX IF NOT EXISTS idx_blog_posts_published_at ON blog_posts(published_at);
CREATE INDEX IF NOT EXISTS idx_blog_posts_featured ON blog_posts(featured);
CREATE INDEX IF NOT EXISTS idx_blog_status_published ON blog_posts(status, published_at);
CREATE INDEX IF NOT EXISTS idx_blog_category_status ON blog_posts(category, status);
CREATE INDEX IF NOT EXISTS idx_blog_featured_status ON blog_posts(featured, status);

-- Create full-text search index
CREATE INDEX IF NOT EXISTS idx_blog_posts_search ON blog_posts USING gin(to_tsvector('english', title || ' ' || COALESCE(excerpt, '') || ' ' || COALESCE(content, '')));

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_blog_posts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_blog_posts_updated_at
    BEFORE UPDATE ON blog_posts
    FOR EACH ROW
    EXECUTE FUNCTION update_blog_posts_updated_at();

-- Insert sample blog posts (optional - for testing)
-- Note: Replace author_id with actual user ID from your database
INSERT INTO blog_posts (title, slug, excerpt, content, category, tags, author_id, status, published_at, featured, reading_time)
VALUES
    (
        '5 Essential Risk Management Strategies for Prop Traders',
        '5-essential-risk-management-strategies-for-prop-traders',
        'Learn the top 5 risk management strategies that every successful prop trader must master to protect their capital and maximize profits.',
        '<h2>Introduction</h2><p>Risk management is the cornerstone of successful prop trading. In this comprehensive guide, we''ll explore the five essential strategies that will help you protect your capital and achieve consistent profitability.</p><h2>1. Position Sizing</h2><p>Never risk more than 1-2% of your account on a single trade. This fundamental rule ensures that even a series of losses won''t significantly impact your trading capital.</p><h2>2. Stop Loss Placement</h2><p>Always use stop losses and place them at logical levels based on market structure, not arbitrary percentages.</p><h2>3. Risk-Reward Ratios</h2><p>Aim for a minimum 1:2 risk-reward ratio on every trade. This means your potential profit should be at least twice your potential loss.</p><h2>4. Diversification</h2><p>Don''t put all your eggs in one basket. Trade multiple instruments and strategies to spread your risk.</p><h2>5. Daily Loss Limits</h2><p>Set a maximum daily loss limit and stick to it. If you hit this limit, stop trading for the day to prevent emotional decisions.</p><h2>Conclusion</h2><p>Mastering these five risk management strategies will significantly improve your trading performance and help you pass prop firm challenges with confidence.</p>',
        'risk_management',
        'risk management, prop trading, trading strategies, position sizing',
        1,
        'published',
        CURRENT_TIMESTAMP - INTERVAL '7 days',
        true,
        8
    ),
    (
        'How to Pass Your First Prop Firm Challenge',
        'how-to-pass-your-first-prop-firm-challenge',
        'A complete step-by-step guide to successfully passing your first prop firm challenge and becoming a funded trader.',
        '<h2>Understanding the Challenge</h2><p>Prop firm challenges are designed to test your trading skills, discipline, and risk management. Here''s everything you need to know to pass on your first attempt.</p><h2>Step 1: Choose the Right Challenge</h2><p>Start with a challenge size that matches your experience level. Don''t jump into a $100K challenge if you''ve never traded with more than $10K.</p><h2>Step 2: Create a Trading Plan</h2><p>Document your strategy, risk management rules, and trading schedule before you start. Stick to this plan throughout the challenge.</p><h2>Step 3: Focus on Consistency</h2><p>Prop firms value consistency over big wins. Aim for steady, small profits rather than trying to hit the profit target in a few trades.</p><h2>Step 4: Manage Your Emotions</h2><p>Stay calm and disciplined. Don''t revenge trade after losses or overtrade after wins.</p><h2>Step 5: Track Your Progress</h2><p>Keep a detailed trading journal and review your performance daily. Learn from both wins and losses.</p><h2>Common Mistakes to Avoid</h2><ul><li>Overtrading to reach profit targets quickly</li><li>Ignoring daily loss limits</li><li>Trading during high-impact news without proper preparation</li><li>Deviating from your trading plan</li></ul><h2>Conclusion</h2><p>Passing a prop firm challenge is achievable with the right mindset, preparation, and discipline. Follow these steps and you''ll be on your way to becoming a funded trader.</p>',
        'prop_trading',
        'prop trading, funded trader, trading challenge, prop firm',
        1,
        'published',
        CURRENT_TIMESTAMP - INTERVAL '5 days',
        true,
        10
    ),
    (
        'Top 10 Trading Indicators Every Trader Should Know',
        'top-10-trading-indicators-every-trader-should-know',
        'Discover the most effective trading indicators used by professional traders to identify trends, momentum, and entry/exit points.',
        '<h2>Introduction</h2><p>Technical indicators are essential tools for traders. In this guide, we''ll cover the top 10 indicators that every trader should master.</p><h2>1. Moving Averages (MA)</h2><p>Simple and exponential moving averages help identify trends and support/resistance levels.</p><h2>2. Relative Strength Index (RSI)</h2><p>RSI measures momentum and helps identify overbought and oversold conditions.</p><h2>3. MACD (Moving Average Convergence Divergence)</h2><p>MACD shows the relationship between two moving averages and helps identify trend changes.</p><h2>4. Bollinger Bands</h2><p>These bands show volatility and potential reversal points.</p><h2>5. Fibonacci Retracement</h2><p>Fibonacci levels help identify potential support and resistance levels.</p><h2>6. Stochastic Oscillator</h2><p>This momentum indicator compares closing prices to price ranges over time.</p><h2>7. Average True Range (ATR)</h2><p>ATR measures market volatility and helps set stop losses.</p><h2>8. Volume</h2><p>Volume confirms price movements and trend strength.</p><h2>9. Ichimoku Cloud</h2><p>A comprehensive indicator that shows support, resistance, momentum, and trend direction.</p><h2>10. Parabolic SAR</h2><p>This indicator helps identify potential reversal points in trending markets.</p><h2>Conclusion</h2><p>Master these 10 indicators and you''ll have a solid foundation for technical analysis.</p>',
        'trading_strategies',
        'technical analysis, trading indicators, chart patterns, trading tools',
        1,
        'published',
        CURRENT_TIMESTAMP - INTERVAL '3 days',
        false,
        12
    ),
    (
        'Market Analysis: Gold Price Forecast for Q4 2025',
        'market-analysis-gold-price-forecast-q4-2025',
        'In-depth analysis of gold price movements and forecast for the fourth quarter of 2025 based on technical and fundamental factors.',
        '<h2>Current Market Overview</h2><p>Gold has shown strong performance in 2025, driven by global economic uncertainty and central bank policies.</p><h2>Technical Analysis</h2><p>Gold is currently trading near key resistance at $2,100. A breakout above this level could target $2,200 in Q4.</p><h2>Fundamental Factors</h2><ul><li>Federal Reserve interest rate policy</li><li>Global inflation trends</li><li>Geopolitical tensions</li><li>Central bank gold purchases</li></ul><h2>Price Forecast</h2><p>Based on current trends, we expect gold to trade between $2,050 and $2,250 in Q4 2025.</p><h2>Trading Opportunities</h2><p>Look for pullbacks to $2,050 support as potential buying opportunities with targets at $2,150 and $2,200.</p>',
        'market_analysis',
        'gold, market analysis, price forecast, commodities',
        1,
        'published',
        CURRENT_TIMESTAMP - INTERVAL '1 day',
        false,
        6
    ),
    (
        'The Psychology of Trading: Mastering Your Mindset',
        'the-psychology-of-trading-mastering-your-mindset',
        'Explore the psychological aspects of trading and learn how to develop the mental discipline needed for consistent profitability.',
        '<h2>Why Psychology Matters</h2><p>Trading psychology is often more important than strategy. Even the best strategy will fail if you can''t control your emotions.</p><h2>Common Psychological Pitfalls</h2><ul><li>Fear of missing out (FOMO)</li><li>Revenge trading after losses</li><li>Overconfidence after wins</li><li>Analysis paralysis</li></ul><h2>Developing Mental Discipline</h2><p>Create a trading routine, practice mindfulness, and maintain a trading journal to improve your psychological edge.</p><h2>Managing Emotions</h2><p>Learn to recognize emotional triggers and develop strategies to stay calm under pressure.</p><h2>Building Confidence</h2><p>Confidence comes from preparation, practice, and consistent execution of your trading plan.</p>',
        'education',
        'trading psychology, mindset, discipline, emotional control',
        1,
        'published',
        CURRENT_TIMESTAMP,
        false,
        7
    ),
    (
        'Breaking News: Major Central Bank Policy Changes',
        'breaking-news-major-central-bank-policy-changes',
        'Latest updates on central bank policy decisions and their impact on financial markets.',
        '<h2>Federal Reserve Announcement</h2><p>The Federal Reserve has announced a surprise policy change that could significantly impact currency and commodity markets.</p><h2>Market Impact</h2><p>Initial market reaction shows increased volatility across major currency pairs and stock indices.</p><h2>Trading Implications</h2><p>Traders should exercise caution and adjust position sizes during this period of heightened volatility.</p>',
        'news',
        'news, central bank, federal reserve, market news',
        1,
        'published',
        CURRENT_TIMESTAMP,
        true,
        4
    );

COMMENT ON TABLE blog_posts IS 'Blog posts for content management system';
COMMENT ON COLUMN blog_posts.slug IS 'URL-friendly unique identifier for the post';
COMMENT ON COLUMN blog_posts.status IS 'Post status: draft, published, or archived';
COMMENT ON COLUMN blog_posts.featured IS 'Whether the post should be featured on the homepage';
COMMENT ON COLUMN blog_posts.reading_time IS 'Estimated reading time in minutes';

