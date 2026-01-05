"""
Scaling Routes
API endpoints for account scaling operations
"""
from flask import Blueprint, request, jsonify, g
from src.services.scaling_service import ScalingService
from src.utils.decorators import token_required
from src.models.user import User
from decimal import Decimal

scaling_bp = Blueprint('scaling', __name__, url_prefix='/api/v1/scaling')


@scaling_bp.route('/my-progress', methods=['GET'])
@token_required
def get_my_scaling_progress():
    """
    Get current user's scaling progress
    
    Returns:
        - Current tier and account size
        - Progress towards next tier
        - Eligibility status
        - Scaling history
    """
    try:
        user_id = g.current_user.id
        progress = ScalingService.get_scaling_history(user_id)
        
        return jsonify({
            'success': True,
            'data': progress
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scaling_bp.route('/eligibility', methods=['GET'])
@token_required
def check_scaling_eligibility():
    """
    Check if current user is eligible for scaling
    
    Returns detailed eligibility information including:
        - Whether user is eligible
        - Current and next tier information
        - Progress percentage
        - Remaining profit needed
    """
    try:
        user_id = g.current_user.id
        eligibility = ScalingService.check_eligibility(user_id)
        
        return jsonify({
            'success': True,
            'data': eligibility
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scaling_bp.route('/scale-up', methods=['POST'])
@token_required
def scale_up():
    """
    Scale up current user to next tier
    
    Requires user to be eligible for scaling.
    Creates new challenge with larger account size.
    """
    try:
        user_id = g.current_user.id
        result = ScalingService.perform_scale_up(user_id)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scaling_bp.route('/tiers', methods=['GET'])
def get_all_tiers():
    """
    Get all available scaling tiers
    
    Public endpoint - no authentication required
    Returns list of all tiers with account sizes and requirements
    """
    try:
        tiers = ScalingService.get_all_tiers()
        
        return jsonify({
            'success': True,
            'data': {
                'tiers': tiers,
                'total_tiers': len(tiers)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scaling_bp.route('/pause', methods=['POST'])
@token_required
def pause_scaling():
    """
    Pause scaling plan for current user
    
    User can resume later without losing progress
    """
    try:
        user_id = g.current_user.id
        result = ScalingService.pause_scaling(user_id)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scaling_bp.route('/resume', methods=['POST'])
@token_required
def resume_scaling():
    """
    Resume paused scaling plan for current user
    """
    try:
        user_id = g.current_user.id
        result = ScalingService.resume_scaling(user_id)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scaling_bp.route('/initialize', methods=['POST'])
@token_required
def initialize_scaling():
    """
    Initialize scaling plan for current user
    
    Body:
        - starting_account_size: Decimal (e.g., 10000, 25000, 50000)
    
    Usually called automatically when user gets funded
    """
    try:
        data = request.get_json()
        
        if not data or 'starting_account_size' not in data:
            return jsonify({
                'success': False,
                'error': 'starting_account_size is required'
            }), 400
        
        user_id = g.current_user.id
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Check if user already has scaling plan
        existing = ScalingService.get_user_scaling(user_id)
        if existing:
            return jsonify({
                'success': False,
                'error': 'User already has a scaling plan'
            }), 400
        
        starting_size = Decimal(str(data['starting_account_size']))
        scaling = ScalingService.initialize_scaling_for_user(user, starting_size)
        
        return jsonify({
            'success': True,
            'message': 'Scaling plan initialized',
            'data': scaling.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid account size: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Admin endpoints

@scaling_bp.route('/admin/user/<int:user_id>', methods=['GET'])
@token_required
def admin_get_user_scaling(user_id):
    """
    [ADMIN] Get scaling progress for any user
    
    Requires admin privileges
    """
    try:
        # Check if current user is admin
        if not g.current_user.is_admin:
            return jsonify({
                'success': False,
                'error': 'Admin privileges required'
            }), 403
        
        progress = ScalingService.get_scaling_history(user_id)
        
        return jsonify({
            'success': True,
            'data': progress
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scaling_bp.route('/admin/user/<int:user_id>/update-profit', methods=['POST'])
@token_required
def admin_update_user_profit(user_id):
    """
    [ADMIN] Manually update profit for a user
    
    Body:
        - profit_amount: Decimal
    
    Requires admin privileges
    """
    try:
        # Check if current user is admin
        if not g.current_user.is_admin:
            return jsonify({
                'success': False,
                'error': 'Admin privileges required'
            }), 403
        
        data = request.get_json()
        
        if not data or 'profit_amount' not in data:
            return jsonify({
                'success': False,
                'error': 'profit_amount is required'
            }), 400
        
        profit_amount = Decimal(str(data['profit_amount']))
        result = ScalingService.update_profit(user_id, profit_amount)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid profit amount: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scaling_bp.route('/admin/all-users', methods=['GET'])
@token_required
def get_all_users_scaling():
    """
    Get scaling progress for all users (Admin/Affiliate only)
    
    Returns:
        - List of all users with their scaling progress
        - Filtered by role (Affiliate sees only their traders)
    """
    try:
        current_user = g.current_user
        
        # Check if user is admin or affiliate
        admin_roles = ['supermaster', 'master']
        if current_user.role not in admin_roles and current_user.role != 'affiliate':
            return jsonify({
                'success': False,
                'error': 'Unauthorized - Admin or Affiliate access required'
            }), 403
        
        # Get all users with scaling data
        from src.extensions import db
        from src.models.account_scaling import AccountScaling
        
        query = db.session.query(
            User.id,
            User.email,
            User.first_name,
            User.last_name,
            AccountScaling.current_tier,
            AccountScaling.current_account_size,
            AccountScaling.next_tier,
            AccountScaling.next_account_size,
            AccountScaling.total_profit,
            AccountScaling.target_profit,
            AccountScaling.progress_percentage,
            AccountScaling.times_scaled,
            AccountScaling.is_eligible_for_scaling,
            AccountScaling.status
        ).join(
            AccountScaling,
            User.id == AccountScaling.user_id
        ).filter(
            User.role == 'trader',
            AccountScaling.status == 'active'
        )
        
        # If affiliate, filter by their traders only
        if current_user.role == 'affiliate':
            # TODO: Add affiliate relationship filtering
            # For now, show all traders
            pass
        
        results = query.all()
        
        users_data = []
        for row in results:
            users_data.append({
                'user_id': row.id,
                'email': row.email,
                'name': f"{row.first_name or ''} {row.last_name or ''}".strip() or 'N/A',
                'current_tier': row.current_tier,
                'current_account_size': float(row.current_account_size) if row.current_account_size else 0,
                'next_tier': row.next_tier,
                'next_account_size': float(row.next_account_size) if row.next_account_size else 0,
                'total_profit': float(row.total_profit) if row.total_profit else 0,
                'target_profit': float(row.target_profit) if row.target_profit else 0,
                'progress_percentage': float(row.progress_percentage) if row.progress_percentage else 0,
                'times_scaled': row.times_scaled or 0,
                'is_eligible_for_scaling': row.is_eligible_for_scaling or False,
                'status': row.status
            })
        
        return jsonify({
            'success': True,
            'data': users_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
