"""
Professional Test Configuration for MarketEdgePros
Supports both SQLite (unit tests) and PostgreSQL (integration tests)
"""
import os
from datetime import timedelta
from src.config import Config


class TestConfig(Config):
    """Base testing configuration"""
    
    # Testing mode
    TESTING = True
    DEBUG = False
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Disable rate limiting for tests
    RATELIMIT_ENABLED = False
    
    # Use simple cache for testing
    CACHE_TYPE = 'simple'
    
    # Disable email sending in tests
    SENDGRID_API_KEY = 'test_key'
    MAIL_SUPPRESS_SEND = True
    
    # Short token expiration for testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=10)
    
    # Test secret keys
    SECRET_KEY = 'test-secret-key-for-testing-only'
    JWT_SECRET_KEY = 'test-jwt-secret-key-for-testing-only'
    
    # Disable security features for testing
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    LOG_DIR = '/tmp/marketedgepros_test_logs'
    
    # Storage (mock)
    STORAGE_TYPE = 'local'
    UPLOAD_FOLDER = '/tmp/marketedgepros_test_uploads'
    
    # External services (mock)
    NOWPAYMENTS_API_KEY = 'test_nowpayments_key'
    DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/test'
    
    # Frontend URL
    FRONTEND_URL = 'http://localhost:3000'


class SQLiteTestConfig(TestConfig):
    """SQLite configuration for fast unit tests"""
    
    # Use in-memory SQLite for maximum speed
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # SQLite specific settings
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class PostgreSQLTestConfig(TestConfig):
    """PostgreSQL configuration for integration tests"""
    
    # Use dedicated test database
    # Default to environment variable or local test database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL',
        'postgresql://user:password@localhost:5432/test_db'
    )
    
    # PostgreSQL specific settings
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 5,
        'max_overflow': 10
    }


# Default to PostgreSQL (SQLite doesn't support JSONB)
DefaultTestConfig = PostgreSQLTestConfig

