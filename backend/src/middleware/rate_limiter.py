"""
Rate Limiting Middleware
Prevents brute force attacks and API abuse
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request
import os

def get_user_identifier():
    """
    Get user identifier for rate limiting
    Uses JWT user_id if authenticated, otherwise IP address
    """
    # Try to get user from JWT token
    from flask_jwt_extended import get_jwt_identity
    try:
        user_id = get_jwt_identity()
        if user_id:
            return f"user:{user_id}"
    except:
        pass
    
    # Fallback to IP address
    return get_remote_address()

# Initialize limiter
limiter = Limiter(
    key_func=get_user_identifier,
    default_limits=["1000 per day", "200 per hour"],
    storage_uri="memory://",  # Use Redis in production: redis://localhost:6379
    strategy="fixed-window",
    headers_enabled=True,
)

# Rate limit configurations for different endpoint types
RATE_LIMITS = {
    # Authentication endpoints - strict limits
    'auth_login': "5 per minute",  # Prevent brute force
    'auth_register': "3 per hour",  # Prevent spam accounts
    'auth_password_reset': "3 per hour",  # Prevent abuse
    'auth_verify_email': "10 per hour",  # Allow retries but prevent spam
    
    # Payment endpoints - moderate limits
    'payment_create': "10 per hour",  # Prevent payment spam
    'payment_list': "60 per minute",  # Allow frequent checks
    
    # Challenge endpoints - moderate limits
    'challenge_create': "5 per hour",  # Prevent abuse
    'challenge_list': "100 per minute",  # Allow frequent checks
    
    # Withdrawal endpoints - strict limits
    'withdrawal_create': "3 per hour",  # Prevent abuse
    'withdrawal_list': "60 per minute",
    
    # User endpoints - lenient limits
    'user_profile': "100 per minute",  # Allow frequent access
    'user_update': "20 per hour",  # Moderate updates
    
    # Admin endpoints - very strict limits
    'admin_action': "100 per hour",  # Prevent abuse of admin powers
    
    # API general - default limits
    'api_default': "200 per hour",
}

def get_rate_limit(endpoint_type):
    """Get rate limit for specific endpoint type"""
    return RATE_LIMITS.get(endpoint_type, RATE_LIMITS['api_default'])

def init_rate_limiter(app):
    """Initialize rate limiter with Flask app"""
    limiter.init_app(app)
    
    # Add custom error handler
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return {
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.',
            'retry_after': e.description
        }, 429
    
    return limiter
