"""
Agent management routes
"""
from flask import Blueprint, jsonify, request
from src.database import db
from src.models import Agent, User, Referral, Commission
from src.middleware.auth import jwt_required, get_current_user
from datetime import datetime

agents_bp = Blueprint('agents', __name__)


@agents_bp.route('/', methods=['GET'])
def list_agents():
    """List all agents (public - for display purposes)"""
    agents = Agent.query.filter_by(is_active=True).all()
    return jsonify({
        'agents': [agent.to_dict() for agent in agents]
    }), 200


@agents_bp.route('/', methods=['POST'])
@jwt_required
def create_agent():
    """Create new agent (admin only)"""
    current_user = get_current_user()
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    
    # Check if user exists
    user = User.query.get(data.get('user_id'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if user already has agent profile
    if user.agent_profile:
        return jsonify({'error': 'User already has agent profile'}), 400
    
    # Generate unique agent code
    agent_code = Agent.generate_agent_code()
    while Agent.query.filter_by(agent_code=agent_code).first():
        agent_code = Agent.generate_agent_code()
    
    # Create agent
    agent = Agent(
        agent_code=agent_code,
        user_id=user.id,
        commission_rate=data.get('commission_rate', 10.0),
        is_active=True
    )
    
    db.session.add(agent)
    db.session.commit()
    
    return jsonify({
        'message': 'Agent created successfully',
        'agent': agent.to_dict()
    }), 201


@agents_bp.route('/<int:agent_id>', methods=['GET'])
@jwt_required
def get_agent(agent_id):
    """Get agent details"""
    current_user = get_current_user()
    
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Only agent owner or admin can view
    if current_user.id != agent.user_id and current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({
        'agent': agent.to_dict()
    }), 200


@agents_bp.route('/<int:agent_id>', methods=['PUT'])
@jwt_required
def update_agent(agent_id):
    """Update agent (admin only)"""
    current_user = get_current_user()
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'commission_rate' in data:
        agent.commission_rate = data['commission_rate']
    if 'is_active' in data:
        agent.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Agent updated successfully',
        'agent': agent.to_dict()
    }), 200


@agents_bp.route('/<int:agent_id>/dashboard', methods=['GET'])
@jwt_required
def agent_dashboard(agent_id):
    """Get agent dashboard statistics"""
    current_user = get_current_user()
    
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Only agent owner or admin can view
    if current_user.id != agent.user_id and current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    # Get statistics
    total_referrals = Referral.query.filter_by(agent_id=agent_id).count()
    active_referrals = Referral.query.filter_by(agent_id=agent_id, status='active').count()
    
    total_commissions = db.session.query(db.func.sum(Commission.commission_amount))\
        .filter_by(agent_id=agent_id).scalar() or 0
    
    pending_commissions = db.session.query(db.func.sum(Commission.commission_amount))\
        .filter_by(agent_id=agent_id, status='pending').scalar() or 0
    
    paid_commissions = db.session.query(db.func.sum(Commission.commission_amount))\
        .filter_by(agent_id=agent_id, status='paid').scalar() or 0
    
    return jsonify({
        'agent': agent.to_dict(),
        'statistics': {
            'total_referrals': total_referrals,
            'active_referrals': active_referrals,
            'total_commissions': float(total_commissions),
            'pending_commissions': float(pending_commissions),
            'paid_commissions': float(paid_commissions),
            'available_balance': agent.get_available_balance()
        }
    }), 200


@agents_bp.route('/<int:agent_id>/referrals', methods=['GET'])
@jwt_required
def list_referrals(agent_id):
    """List agent referrals"""
    current_user = get_current_user()
    
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Only agent owner or admin can view
    if current_user.id != agent.user_id and current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    referrals = Referral.query.filter_by(agent_id=agent_id).all()
    
    return jsonify({
        'referrals': [referral.to_dict() for referral in referrals]
    }), 200


@agents_bp.route('/<int:agent_id>/commissions', methods=['GET'])
@jwt_required
def list_commissions(agent_id):
    """List agent commissions"""
    current_user = get_current_user()
    
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Only agent owner or admin can view
    if current_user.id != agent.user_id and current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    commissions = Commission.query.filter_by(agent_id=agent_id).all()
    
    return jsonify({
        'commissions': [commission.to_dict() for commission in commissions]
    }), 200


@agents_bp.route('/code/<agent_code>', methods=['GET'])
def get_agent_by_code(agent_code):
    """Get agent by referral code (public)"""
    agent = Agent.query.filter_by(agent_code=agent_code, is_active=True).first()
    
    if not agent:
        return jsonify({'error': 'Invalid referral code'}), 404
    
    return jsonify({
        'agent': {
            'id': agent.id,
            'agent_code': agent.agent_code,
            'user': {
                'first_name': agent.user.first_name,
                'last_name': agent.user.last_name
            }
        }
    }), 200

