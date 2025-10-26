-- Add course_enrollments table for drip campaign
CREATE TABLE IF NOT EXISTS course_enrollments (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- Drip campaign tracking
    module_1_sent BOOLEAN DEFAULT FALSE,
    module_1_sent_at TIMESTAMP,
    
    module_2_sent BOOLEAN DEFAULT FALSE,
    module_2_sent_at TIMESTAMP,
    
    module_3_sent BOOLEAN DEFAULT FALSE,
    module_3_sent_at TIMESTAMP,
    
    module_4_sent BOOLEAN DEFAULT FALSE,
    module_4_sent_at TIMESTAMP,
    
    module_5_sent BOOLEAN DEFAULT FALSE,
    module_5_sent_at TIMESTAMP,
    
    -- Engagement tracking
    last_email_opened_at TIMESTAMP,
    unsubscribed BOOLEAN DEFAULT FALSE,
    unsubscribed_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_course_email UNIQUE (email)
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_course_enrollments_email ON course_enrollments(email);

-- Create index on unsubscribed for filtering
CREATE INDEX IF NOT EXISTS idx_course_enrollments_unsubscribed ON course_enrollments(unsubscribed);

-- Create index on enrolled_at for drip campaign queries
CREATE INDEX IF NOT EXISTS idx_course_enrollments_enrolled_at ON course_enrollments(enrolled_at);

