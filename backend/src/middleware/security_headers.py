"""
Security Headers Middleware
Adds security headers to all responses
"""
from flask import request
from flask import Flask
from flask_talisman import Talisman

def init_security_headers(app: Flask, force_https: bool = False):
    """
    Initialize security headers with Flask app
    
    Args:
        app: Flask application instance
        force_https: Whether to force HTTPS (set True in production)
    """
    
    # Content Security Policy
    csp = {
        'default-src': ["'self'"],
        'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", 'https://cdn.jsdelivr.net'],
        'style-src': ["'self'", "'unsafe-inline'", 'https://fonts.googleapis.com'],
        'font-src': ["'self'", 'https://fonts.gstatic.com'],
        'img-src': ["'self'", 'data:', 'https:'],
        'connect-src': ["'self'"],
        'frame-ancestors': ["'none'"],
        'base-uri': ["'self'"],
        'form-action': ["'self'"],
    }
    
    # Initialize Talisman for security headers
    Talisman(
        app,
        force_https=force_https,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,  # 1 year
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src'],
        referrer_policy='strict-origin-when-cross-origin',
        feature_policy={
            'geolocation': "'none'",
            'microphone': "'none'",
            'camera': "'none'",
            'payment': "'self'",
        }
    )
    
    @app.after_request
    def add_security_headers(response):
        """Add additional security headers to all responses"""
        
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions policy (formerly Feature-Policy)
        response.headers['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=(self)'
        )
        
        # Remove server header
        response.headers.pop('Server', None)
        
        # Add custom security header
        response.headers['X-Security-Protected'] = 'MarketEdgePros'
        
        return response
    
    return app

def add_cors_headers(app: Flask, allowed_origins: list = None):
    """
    Add CORS headers for API endpoints
    
    Args:
        app: Flask application instance
        allowed_origins: List of allowed origins (default: localhost only)
    """
    if allowed_origins is None:
        allowed_origins = ['http://localhost:3000', 'http://localhost:5000']
    
    @app.after_request
    def cors_headers(response):
        origin = request.headers.get('Origin')
        
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRF-Token'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Max-Age'] = '3600'
        
        return response
    
    return app
