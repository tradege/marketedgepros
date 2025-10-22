"""
Roles API Routes
"""
from flask import Blueprint, jsonify, request, g
from src.models.role import Role
from src.database import db
from src.utils.decorators import token_required, admin_required
from datetime import datetime


roles_bp = Blueprint('roles', __name__)


@roles_bp.route('/roles', methods=['GET'])
@token_required
def get_roles():
    """Get all active roles"""
    try:
        roles = Role.query.filter_by(is_active=True).order_by(Role.hierarchy).all()
        return jsonify({
            'roles': [role.to_dict() for role in roles]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@roles_bp.route('/roles/<int:role_id>', methods=['GET'])
@token_required
@admin_required
def get_role(role_id):
    """Get role by ID"""
    try:
        role = Role.query.get_or_404(role_id)
        return jsonify(role.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@roles_bp.route('/roles', methods=['POST'])
@token_required
@admin_required
def create_role():
    """Create new role (Super Master only)"""
    try:
        # Only supermaster can create roles
        if g.current_user.role not in ['supermaster', 'super_admin']:
            return jsonify({'error': 'Only Super Master can create roles'}), 403
        
        data = request.get_json()
        
        # Check if role name already exists
        existing_role = Role.query.filter_by(name=data['name']).first()
        if existing_role:
            return jsonify({'error': 'Role name already exists'}), 400
        
        role = Role(
            name=data['name'],
            label=data['label'],
            label_he=data.get('label_he'),
            color=data.get('color', 'bg-gray-100 text-gray-800'),
            icon=data.get('icon', '📊'),
            hierarchy=data['hierarchy'],
            permissions=data.get('permissions', {})
        )
        
        db.session.add(role)
        db.session.commit()
        
        return jsonify({
            'message': 'Role created successfully',
            'role': role.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roles_bp.route('/roles/<int:role_id>', methods=['PUT'])
@token_required
@admin_required
def update_role(role_id):
    """Update role (Super Master only)"""
    try:
        # Only supermaster can update roles
        if g.current_user.role not in ['supermaster', 'super_admin']:
            return jsonify({'error': 'Only Super Master can update roles'}), 403
        
        role = Role.query.get_or_404(role_id)
        data = request.get_json()
        
        # Update fields
        if 'label' in data:
            role.label = data['label']
        if 'label_he' in data:
            role.label_he = data['label_he']
        if 'color' in data:
            role.color = data['color']
        if 'icon' in data:
            role.icon = data['icon']
        if 'hierarchy' in data:
            role.hierarchy = data['hierarchy']
        if 'permissions' in data:
            role.permissions = data['permissions']
        if 'is_active' in data:
            role.is_active = data['is_active']
        
        role.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Role updated successfully',
            'role': role.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roles_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_role(role_id):
    """Delete role (soft delete) (Super Master only)"""
    try:
        # Only supermaster can delete roles
        if g.current_user.role not in ['supermaster', 'super_admin']:
            return jsonify({'error': 'Only Super Master can delete roles'}), 403
        
        role = Role.query.get_or_404(role_id)
        
        # Prevent deletion of default roles
        if role.name in ['supermaster', 'super_admin', 'admin', 'agent', 'trader']:
            return jsonify({'error': 'Cannot delete default roles'}), 400
        
        # Soft delete
        role.is_active = False
        role.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Role deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roles_bp.route('/roles/seed', methods=['POST'])
@token_required
@admin_required
def seed_roles():
    """Seed default roles (Super Master only)"""
    try:
        # Only supermaster can seed roles
        if g.current_user.role not in ['supermaster', 'super_admin']:
            return jsonify({'error': 'Only Super Master can seed roles'}), 403
        
        Role.seed_default_roles()
        
        return jsonify({'message': 'Default roles seeded successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

