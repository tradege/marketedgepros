"""Authentication middleware"""
from functools import wraps
from flask import request, jsonify, g
from src.models import User
import jwt
from flask import current_app
from src.constants.roles import Roles


def jwt_required(f):
    """JWT authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=["HS256"]
            )
            
            # Get user
            current_user = User.query.get(data['user_id'])
            if not current_user or not current_user.is_active:
                return jsonify({'error': 'Invalid or inactive user'}), 401
            
            # Store in g object
            g.current_user = current_user
            
            # Set hierarchy scope for automatic filtering
            from src.utils.hierarchy_scoping import set_request_hierarchy_scope
            from src.database import db
            set_request_hierarchy_scope(db.session, current_user)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': f'Authentication failed: {str(e)}'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user():
    """Get current authenticated user from g object"""
    return g.get('current_user', None)


def admin_required(f):
    """Admin role required decorator"""
    @wraps(f)
    @jwt_required
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()
        
        if not current_user or not Roles.is_admin(current_user.role):
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def agent_required(f):
    """Agent role required decorator"""
    @wraps(f)
    @jwt_required
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()
        
        if not current_user or (current_user.role not in ['admin', 'agent'] and not current_user.agent_profile):
            return jsonify({'error': 'Agent access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

