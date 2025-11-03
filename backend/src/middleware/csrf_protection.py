"""
CSRF Protection Middleware
Protects against Cross-Site Request Forgery attacks
"""
from flask import request, jsonify, session
from flask_wtf.csrf import CSRFProtect, CSRFError
import secrets
from functools import wraps

# Initialize CSRF protection
csrf = CSRFProtect()

def init_csrf_protection(app):
    """
    Initialize CSRF protection with Flask app
    
    Args:
        app: Flask application instance
    """
    csrf.init_app(app)
    
    # Configure CSRF settings
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = None  # Token doesn't expire
    app.config['WTF_CSRF_SSL_STRICT'] = True  # Enforce HTTPS in production
    app.config['WTF_CSRF_CHECK_DEFAULT'] = True
    
    # Custom error handler for CSRF errors
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return jsonify({
            'error': 'CSRF token missing or invalid',
            'message': 'Please refresh the page and try again',
            'code': 'CSRF_ERROR'
        }), 400
    
    return csrf

def csrf_exempt(view):
    """
    Decorator to exempt a view from CSRF protection
    Use sparingly and only for public APIs
    
    Usage:
        @app.route('/public-api')
        @csrf_exempt
        def public_api():
            return {'data': 'public'}
    """
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        return view(*args, **kwargs)
    
    wrapped_view._csrf_exempt = True
    return wrapped_view

def generate_csrf_token():
    """
    Generate a new CSRF token
    
    Returns:
        str: CSRF token
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']

def validate_csrf_token(token):
    """
    Validate CSRF token
    
    Args:
        token: Token to validate
        
    Returns:
        bool: True if valid
    """
    if '_csrf_token' not in session:
        return False
    return secrets.compare_digest(session['_csrf_token'], token)
