"""
Commission and Withdrawal API Routes
MarketEdgePros - Prop Trading Firm Platform
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from functools import wraps
import logging

# Import models and logic
from models_commission import User, Commission, PaymentMethod, Withdrawal
from commission_logic import (
    calculate_commission,
    get_affiliate_stats,
    can_request_withdrawal,
    get_customers_by_affiliate
)

logger = logging.getLogger(__name__)

# Create blueprint
commission_bp = Blueprint('commission', __name__, url_prefix='/api')


def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Implement actual authentication check
        # For now, assume user_id is in session or JWT token
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def super_master_required(f):
    """Decorator to require Super Master role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Implement role check
        user_id = request.headers.get('X-User-ID')
        # Check if user is Super Master
        # For now, placeholder
        return f(*args, **kwargs)
    return decorated_function


# ==================== AFFILIATE ROUTES ====================

@commission_bp.route('/affiliate/stats', methods=['GET'])
@login_required
def get_affiliate_statistics():
    """
    Get affiliate's commission statistics
    
    Returns:
        JSON with paid_customers_count, pending_commission, commission_balance,
        can_withdraw, total_earned, and list of commissions
    """
    try:
        from app import db  # Import db from main app
        user_id = int(request.headers.get('X-User-ID'))
        
        stats = get_affiliate_stats(db.session, user_id)
        
        if 'error' in stats:
            return jsonify(stats), 400
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Error getting affiliate stats: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commission_bp.route('/affiliate/commissions', methods=['GET'])
@login_required
def get_affiliate_commissions():
    """
    Get paginated list of commissions for affiliate
    
    Query params:
        page: Page number (default 1)
        per_page: Items per page (default 20)
        status: Filter by status (optional)
    """
    try:
        from app import db
        user_id = int(request.headers.get('X-User-ID'))
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status_filter = request.args.get('status', None)
        
        query = db.session.query(Commission).filter(Commission.affiliate_id == user_id)
        
        if status_filter:
            query = query.filter(Commission.status == status_filter)
        
        query = query.order_by(Commission.created_at.desc())
        
        # Paginate
        total = query.count()
        commissions = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Format results
        results = []
        for comm in commissions:
            customer = db.session.query(User).filter(User.id == comm.customer_id).first()
            results.append({
                'id': comm.id,
                'customer_name': customer.name if customer else 'Unknown',
                'customer_email': customer.email if customer else 'Unknown',
                'amount': comm.amount,
                'commission_rate': comm.commission_rate,
                'status': comm.status,
                'created_at': comm.created_at.isoformat() if comm.created_at else None,
                'released_at': comm.released_at.isoformat() if comm.released_at else None,
            })
        
        return jsonify({
            'commissions': results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting commissions: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commission_bp.route('/affiliate/customers', methods=['GET'])
@login_required
def get_affiliate_customers():
    """Get list of customers referred by affiliate"""
    try:
        from app import db
        user_id = int(request.headers.get('X-User-ID'))
        
        customers = get_customers_by_affiliate(db.session, user_id)
        
        return jsonify({'customers': customers}), 200
        
    except Exception as e:
        logger.error(f"Error getting customers: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== PAYMENT METHOD ROUTES ====================

@commission_bp.route('/payment-method', methods=['GET'])
@login_required
def get_payment_method():
    """Get active payment method for user"""
    try:
        from app import db
        user_id = int(request.headers.get('X-User-ID'))
        
        payment_method = db.session.query(PaymentMethod).filter(
            PaymentMethod.user_id == user_id,
            PaymentMethod.is_active == True
        ).first()
        
        if not payment_method:
            return jsonify({'message': 'No payment method set'}), 404
        
        return jsonify(payment_method.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error getting payment method: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commission_bp.route('/payment-method', methods=['POST'])
@login_required
def create_payment_method():
    """
    Create or update payment method
    
    Body:
        method_type: 'bank', 'paypal', 'crypto', 'wise'
        + relevant fields based on method_type
    """
    try:
        from app import db
        user_id = int(request.headers.get('X-User-ID'))
        data = request.get_json()
        
        method_type = data.get('method_type')
        if not method_type or method_type not in ['bank', 'paypal', 'crypto', 'wise']:
            return jsonify({'error': 'Invalid method_type'}), 400
        
        # Validate required fields based on method type
        if method_type == 'bank':
            required = ['bank_name', 'account_number', 'account_holder_name']
            if not all(data.get(field) for field in required):
                return jsonify({'error': f'Missing required fields: {required}'}), 400
        
        elif method_type == 'paypal':
            if not data.get('paypal_email'):
                return jsonify({'error': 'paypal_email is required'}), 400
        
        elif method_type == 'crypto':
            if not data.get('crypto_address') or not data.get('crypto_network'):
                return jsonify({'error': 'crypto_address and crypto_network are required'}), 400
        
        elif method_type == 'wise':
            if not data.get('wise_email'):
                return jsonify({'error': 'wise_email is required'}), 400
        
        # Deactivate old payment methods
        db.session.query(PaymentMethod).filter(
            PaymentMethod.user_id == user_id
        ).update({'is_active': False})
        
        # Create new payment method
        payment_method = PaymentMethod(
            user_id=user_id,
            method_type=method_type,
            is_active=True,
            bank_name=data.get('bank_name'),
            account_number=data.get('account_number'),
            branch_number=data.get('branch_number'),
            account_holder_name=data.get('account_holder_name'),
            paypal_email=data.get('paypal_email'),
            crypto_address=data.get('crypto_address'),
            crypto_network=data.get('crypto_network'),
            wise_email=data.get('wise_email'),
        )
        
        db.session.add(payment_method)
        db.session.commit()
        
        return jsonify({
            'message': 'Payment method saved successfully',
            'payment_method': payment_method.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating payment method: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== WITHDRAWAL ROUTES ====================

@commission_bp.route('/withdrawal/eligibility', methods=['GET'])
@login_required
def check_withdrawal_eligibility():
    """Check if user can request withdrawal"""
    try:
        from app import db
        user_id = int(request.headers.get('X-User-ID'))
        
        can_withdraw, reason, days_remaining = can_request_withdrawal(db.session, user_id)
        
        return jsonify({
            'can_withdraw': can_withdraw,
            'reason': reason,
            'days_remaining': days_remaining
        }), 200
        
    except Exception as e:
        logger.error(f"Error checking eligibility: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commission_bp.route('/withdrawal/request', methods=['POST'])
@login_required
def request_withdrawal():
    """
    Request a withdrawal
    
    Body:
        amount: Withdrawal amount (must be <= commission_balance)
    """
    try:
        from app import db
        user_id = int(request.headers.get('X-User-ID'))
        data = request.get_json()
        
        amount = data.get('amount')
        if not amount or amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
        
        # Get user
        user = db.session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check eligibility
        can_withdraw, reason, days_remaining = can_request_withdrawal(db.session, user_id)
        if not can_withdraw:
            return jsonify({'error': reason, 'days_remaining': days_remaining}), 400
        
        # Check balance
        if amount > user.commission_balance:
            return jsonify({'error': 'Insufficient balance'}), 400
        
        # Check payment method
        payment_method = db.session.query(PaymentMethod).filter(
            PaymentMethod.user_id == user_id,
            PaymentMethod.is_active == True
        ).first()
        
        if not payment_method:
            return jsonify({'error': 'No payment method set. Please add payment details first.'}), 400
        
        # Create withdrawal request
        withdrawal = Withdrawal(
            user_id=user_id,
            amount=amount,
            method_type=payment_method.method_type,
            payment_details=payment_method.to_dict(),
            status='pending',
            requested_at=datetime.utcnow()
        )
        
        db.session.add(withdrawal)
        
        # Deduct from balance
        user.commission_balance -= amount
        user.last_withdrawal_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal request submitted successfully',
            'withdrawal': withdrawal.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error requesting withdrawal: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commission_bp.route('/withdrawal/history', methods=['GET'])
@login_required
def get_withdrawal_history():
    """Get withdrawal history for user"""
    try:
        from app import db
        user_id = int(request.headers.get('X-User-ID'))
        
        withdrawals = db.session.query(Withdrawal).filter(
            Withdrawal.user_id == user_id
        ).order_by(Withdrawal.requested_at.desc()).all()
        
        results = [w.to_dict() for w in withdrawals]
        
        return jsonify({'withdrawals': results}), 200
        
    except Exception as e:
        logger.error(f"Error getting withdrawal history: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== ADMIN ROUTES (Super Master) ====================

@commission_bp.route('/admin/withdrawals/pending', methods=['GET'])
@super_master_required
def get_pending_withdrawals():
    """Get all pending withdrawal requests"""
    try:
        from app import db
        
        withdrawals = db.session.query(Withdrawal).filter(
            Withdrawal.status == 'pending'
        ).order_by(Withdrawal.requested_at.asc()).all()
        
        results = []
        for w in withdrawals:
            user = db.session.query(User).filter(User.id == w.user_id).first()
            result = w.to_dict()
            result['user_name'] = user.name if user else 'Unknown'
            result['user_email'] = user.email if user else 'Unknown'
            results.append(result)
        
        return jsonify({'withdrawals': results}), 200
        
    except Exception as e:
        logger.error(f"Error getting pending withdrawals: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commission_bp.route('/admin/withdrawals/<int:withdrawal_id>/approve', methods=['POST'])
@super_master_required
def approve_withdrawal(withdrawal_id):
    """Approve a withdrawal request"""
    try:
        from app import db
        admin_id = int(request.headers.get('X-User-ID'))
        
        withdrawal = db.session.query(Withdrawal).filter(
            Withdrawal.id == withdrawal_id
        ).first()
        
        if not withdrawal:
            return jsonify({'error': 'Withdrawal not found'}), 404
        
        if withdrawal.status != 'pending':
            return jsonify({'error': 'Withdrawal is not pending'}), 400
        
        withdrawal.status = 'approved'
        withdrawal.approved_at = datetime.utcnow()
        withdrawal.approved_by = admin_id
        
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal approved successfully',
            'withdrawal': withdrawal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error approving withdrawal: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commission_bp.route('/admin/withdrawals/<int:withdrawal_id>/mark-paid', methods=['POST'])
@super_master_required
def mark_withdrawal_paid(withdrawal_id):
    """Mark withdrawal as paid"""
    try:
        from app import db
        
        withdrawal = db.session.query(Withdrawal).filter(
            Withdrawal.id == withdrawal_id
        ).first()
        
        if not withdrawal:
            return jsonify({'error': 'Withdrawal not found'}), 404
        
        if withdrawal.status not in ['pending', 'approved']:
            return jsonify({'error': 'Withdrawal cannot be marked as paid'}), 400
        
        withdrawal.status = 'paid'
        withdrawal.paid_at = datetime.utcnow()
        
        # Update commission records
        db.session.query(Commission).filter(
            Commission.affiliate_id == withdrawal.user_id,
            Commission.status == 'released'
        ).update({'status': 'paid', 'paid_at': datetime.utcnow()})
        
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal marked as paid successfully',
            'withdrawal': withdrawal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking withdrawal paid: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commission_bp.route('/admin/withdrawals/<int:withdrawal_id>/reject', methods=['POST'])
@super_master_required
def reject_withdrawal(withdrawal_id):
    """
    Reject a withdrawal request
    
    Body:
        reason: Rejection reason
    """
    try:
        from app import db
        data = request.get_json()
        reason = data.get('reason', 'No reason provided')
        
        withdrawal = db.session.query(Withdrawal).filter(
            Withdrawal.id == withdrawal_id
        ).first()
        
        if not withdrawal:
            return jsonify({'error': 'Withdrawal not found'}), 404
        
        if withdrawal.status != 'pending':
            return jsonify({'error': 'Withdrawal is not pending'}), 400
        
        # Refund amount to user's balance
        user = db.session.query(User).filter(User.id == withdrawal.user_id).first()
        if user:
            user.commission_balance += withdrawal.amount
        
        withdrawal.status = 'rejected'
        withdrawal.rejected_at = datetime.utcnow()
        withdrawal.notes = reason
        
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal rejected successfully',
            'withdrawal': withdrawal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error rejecting withdrawal: {str(e)}")
        return jsonify({'error': str(e)}), 500

