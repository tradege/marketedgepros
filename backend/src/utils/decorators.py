"""Decorators for authentication and authorization"""
from functools import wraps
from flask import request, jsonify, g
from src.models import User
from src.services.auth_service import AuthService
from src.constants.roles import Roles
from src.utils.hierarchy_scoping import set_request_hierarchy_scope
from src.database import db


def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Check if token is blacklisted
        if AuthService.is_token_blacklisted(token):
            return jsonify({'error': 'Token has been revoked'}), 401
        
        # Verify token
        payload = User.verify_token(token, token_type='access')
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get user
        current_user = User.query.get(payload['user_id'])
        if not current_user or not current_user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        # Store user in g
        g.current_user = current_user
        g.token = token
        
        # Enable hierarchy scoping for this request
        set_request_hierarchy_scope(db.session, current_user)
        
        return f(*args, **kwargs)
    
    return decorated


def role_required(*roles):
    """Decorator to require specific role(s)"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, 'current_user'):
                return jsonify({'error': 'Authentication required'}), 401
            
            if g.current_user.role not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator


def tenant_required(f):
    """Decorator to ensure user belongs to a tenant"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'current_user'):
            return jsonify({'error': 'Authentication required'}), 401
        
        if not g.current_user.tenant_id:
            return jsonify({'error': 'User must belong to a tenant'}), 403
        
        return f(*args, **kwargs)
    
    return decorated


def verified_email_required(f):
    """Decorator to require verified email"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'current_user'):
            return jsonify({'error': 'Authentication required'}), 401
        
        if not g.current_user.is_verified:
            return jsonify({'error': 'Email verification required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated



def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'current_user'):
            return jsonify({'error': 'Authentication required'}), 401
        
        if not Roles.is_admin(g.current_user.role):
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated

