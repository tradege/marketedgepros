-- Add support_articles table for knowledge base
CREATE TABLE IF NOT EXISTS support_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    excerpt VARCHAR(500),
    
    -- Category & Organization
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    tags JSONB,
    
    -- SEO
    meta_description VARCHAR(160),
    meta_keywords VARCHAR(255),
    
    -- Status & Publishing
    status VARCHAR(20) DEFAULT 'draft' NOT NULL,
    published_at TIMESTAMP,
    
    -- Author
    author_id INTEGER REFERENCES users(id),
    
    -- Engagement
    views INTEGER DEFAULT 0,
    helpful_count INTEGER DEFAULT 0,
    not_helpful_count INTEGER DEFAULT 0,
    
    -- Ordering
    "order" INTEGER DEFAULT 0,
    featured BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_status CHECK (status IN ('draft', 'published', 'archived'))
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_support_articles_slug ON support_articles(slug);
CREATE INDEX IF NOT EXISTS idx_support_articles_category ON support_articles(category);
CREATE INDEX IF NOT EXISTS idx_support_articles_status ON support_articles(status);
CREATE INDEX IF NOT EXISTS idx_support_articles_featured ON support_articles(featured);
CREATE INDEX IF NOT EXISTS idx_support_articles_published_at ON support_articles(published_at);

-- Create full-text search index
CREATE INDEX IF NOT EXISTS idx_support_articles_search ON support_articles USING gin(to_tsvector('english', title || ' ' || content));

