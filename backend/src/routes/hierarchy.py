"""
Hierarchy routes for MLM structure
"""
from flask import Blueprint, request, jsonify, g
from src.database import db
from src.models.user import User
from src.utils.decorators import token_required
from datetime import datetime
from sqlalchemy import or_

hierarchy_bp = Blueprint('hierarchy', __name__)


@hierarchy_bp.route('/my-downline', methods=['GET'])
@token_required
def get_my_downline():
    """Get current user's entire downline"""
    try:
        current_user = g.current_user
        
        # Get all descendants
        descendants = current_user.get_all_descendants()
        
        # Organize by level
        downline_by_level = {}
        for user in descendants:
            level_diff = user.level - current_user.level
            if level_diff not in downline_by_level:
                downline_by_level[level_diff] = []
            
            downline_by_level[level_diff].append({
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'level': user.level,
                'parent_id': user.parent_id,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'children_count': len(user.children)
            })
        
        return jsonify({
            'total_downline': len(descendants),
            'downline_by_level': downline_by_level,
            'levels_deep': max(downline_by_level.keys()) if downline_by_level else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hierarchy_bp.route('/my-direct-team', methods=['GET'])
@token_required
def get_my_direct_team():
    """Get only direct children (1 level down)"""
    try:
        current_user = g.current_user
        
        # Get filters
        role = request.args.get('role')
        status = request.args.get('status')
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = User.query.filter_by(parent_id=current_user.id)
        
        if role:
            query = query.filter_by(role=role)
        
        if status:
            is_active = status == 'active'
            query = query.filter_by(is_active=is_active)
        
        if search:
            query = query.filter(
                or_(
                    User.email.ilike(f'%{search}%'),
                    User.first_name.ilike(f'%{search}%'),
                    User.last_name.ilike(f'%{search}%')
                )
            )
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        users = []
        for user in pagination.items:
            users.append({
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'level': user.level,
                'is_active': user.is_active,
                'kyc_status': user.kyc_status,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'children_count': len(user.children),
                'downline_count': user.get_downline_count()
            })
        
        return jsonify({
            'users': users,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hierarchy_bp.route('/create-user', methods=['POST'])
@token_required
def create_downline_user():
    """Create a new user in downline"""
    try:
        current_user = g.current_user
        data = request.get_json()
        
        # Validate required fields
        required = ['email', 'password', 'first_name', 'last_name', 'role']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user can create this role
        target_role = data['role']
        if not current_user.can_create_user(target_role):
            return jsonify({'error': f'You cannot create users with role: {target_role}'}), 403
        
        # Check if email exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        new_user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=target_role,
            parent_id=current_user.id,
            level=current_user.level + 1,
            phone=data.get('phone'),
            is_active=True,
            is_verified=data.get('email_verified', False),
            commission_rate=data.get('commission_rate', 0.00)
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.flush()  # Get the ID
        
        # Update tree path
        new_user.update_tree_path()
        
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'role': new_user.role,
                'level': new_user.level,
                'parent_id': new_user.parent_id,
                'tree_path': new_user.tree_path
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@hierarchy_bp.route('/user/<int:user_id>', methods=['GET'])
@token_required
def get_downline_user(user_id):
    """Get details of a user in downline"""
    try:
        current_user = g.current_user
        
        # Get the user
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if user is in current user's downline
        if user.id != current_user.id:
            ancestors = user.get_ancestors()
            if current_user not in ancestors:
                return jsonify({'error': 'Access denied'}), 403
        
        # Get user details with hierarchy info
        return jsonify({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'role': user.role,
            'level': user.level,
            'parent_id': user.parent_id,
            'tree_path': user.tree_path,
            'commission_rate': float(user.commission_rate) if user.commission_rate else 0.00,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'kyc_status': user.kyc_status,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'parent': {
                'id': user.parent.id,
                'email': user.parent.email,
                'name': f"{user.parent.first_name} {user.parent.last_name}",
                'role': user.parent.role
            } if user.parent else None,
            'children_count': len(user.children),
            'downline_count': user.get_downline_count()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hierarchy_bp.route('/user/<int:user_id>', methods=['PUT'])
@token_required
def update_downline_user(user_id):
    """Update a user in downline"""
    try:
        current_user = g.current_user
        data = request.get_json()
        
        # Get the user
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if user is in current user's downline
        ancestors = user.get_ancestors()
        if current_user not in ancestors and user.id != current_user.id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'commission_rate' in data:
            user.commission_rate = data['commission_rate']
        
        # Only allow role change if user can create that role
        if 'role' in data:
            new_role = data['role']
            if current_user.can_create_user(new_role):
                user.role = new_role
            else:
                return jsonify({'error': f'You cannot assign role: {new_role}'}), 403
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@hierarchy_bp.route('/tree', methods=['GET'])
@token_required
def get_hierarchy_tree():
    """Get hierarchical tree structure of downline"""
    try:
        current_user = g.current_user
        max_depth = int(request.args.get('max_depth', 5))
        
        def build_tree(user, current_depth=0):
            """Recursively build tree structure"""
            if current_depth >= max_depth:
                return None
            
            node = {
                'id': user.id,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}",
                'role': user.role,
                'level': user.level,
                'is_active': user.is_active,
                'children_count': len(user.children),
                'children': []
            }
            
            for child in user.children:
                child_node = build_tree(child, current_depth + 1)
                if child_node:
                    node['children'].append(child_node)
            
            return node
        
        tree = build_tree(current_user)
        
        return jsonify({
            'tree': tree,
            'total_downline': current_user.get_downline_count()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hierarchy_bp.route('/stats', methods=['GET'])
@token_required
def get_hierarchy_stats():
    """Get statistics about downline"""
    try:
        current_user = g.current_user
        
        # Get all descendants
        descendants = current_user.get_all_descendants()
        
        # Count by role
        role_counts = {}
        for user in descendants:
            role_counts[user.role] = role_counts.get(user.role, 0) + 1
        
        # Count by level
        level_counts = {}
        for user in descendants:
            level_diff = user.level - current_user.level
            level_counts[level_diff] = level_counts.get(level_diff, 0) + 1
        
        # Count active vs inactive
        active_count = sum(1 for u in descendants if u.is_active)
        inactive_count = len(descendants) - active_count
        
        return jsonify({
            'total_downline': len(descendants),
            'direct_children': len(current_user.children),
            'by_role': role_counts,
            'by_level': level_counts,
            'active': active_count,
            'inactive': inactive_count,
            'max_depth': max(level_counts.keys()) if level_counts else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

