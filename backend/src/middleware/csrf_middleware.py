"""
CSRF Protection Middleware
Implements Double Submit Cookie pattern for CSRF protection
"""
import secrets
from flask import request, jsonify, g
from functools import wraps


def generate_csrf_token():
    """
    Generate a cryptographically secure CSRF token
    
    Returns:
        str: A URL-safe random token (32 bytes)
    """
    return secrets.token_urlsafe(32)


def csrf_protect(f):
    """
    Decorator to protect routes from CSRF attacks
    
    Uses Double Submit Cookie pattern:
    - Token is sent in both cookie (httpOnly) and custom header
    - Both must match for the request to be valid
    
    Usage:
        @app.route('/api/profile', methods=['PUT'])
        @token_required
        @csrf_protect
        def update_profile():
            ...
    
    Args:
        f: The route function to protect
        
    Returns:
        The decorated function with CSRF protection
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Skip CSRF check for safe methods (GET, HEAD, OPTIONS)
        # These methods should not modify state
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return f(*args, **kwargs)
        
        # Get CSRF token from cookie
        cookie_token = request.cookies.get('csrf_token')
        
        # Get CSRF token from header
        header_token = request.headers.get('X-CSRF-Token')
        
        # Validate both tokens exist
        if not cookie_token:
            return jsonify({
                'error': 'CSRF token missing in cookie',
                'code': 'CSRF_COOKIE_MISSING'
            }), 403
        
        if not header_token:
            return jsonify({
                'error': 'CSRF token missing in header',
                'code': 'CSRF_HEADER_MISSING'
            }), 403
        
        # Validate tokens match (constant-time comparison)
        if not secrets.compare_digest(cookie_token, header_token):
            return jsonify({
                'error': 'CSRF token mismatch',
                'code': 'CSRF_TOKEN_MISMATCH'
            }), 403
        
        # Store token in g for potential use in the route
        g.csrf_token = cookie_token
        
        return f(*args, **kwargs)
    
    return decorated


def set_csrf_cookie(response, csrf_token):
    """
    Helper function to set CSRF token cookie on response
    
    Args:
        response: Flask response object
        csrf_token: The CSRF token to set
        
    Returns:
        The response object with CSRF cookie set
    """
    response.set_cookie(
        'csrf_token',
        value=csrf_token,
        httponly=True,  # Not accessible to JavaScript
        secure=True,    # HTTPS only
        samesite='Lax', # CSRF protection
        max_age=3600    # 1 hour (same as access token)
    )
    return response
