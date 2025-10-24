"""
Wallet routes for balance management
"""
from flask import Blueprint, request, jsonify, g
from src.database import db
from src.models.wallet import Wallet, Transaction
from src.models.withdrawal import Withdrawal
from src.services.wallet_service import WalletService
from src.middleware.auth import jwt_required, admin_required, get_current_user
from datetime import datetime

wallet_bp = Blueprint('wallet', __name__)


@wallet_bp.route('/balance', methods=['GET'])
@jwt_required
def get_balance():
    """Get user wallet balance"""
    try:
        user_id = get_current_user().id
        wallet = WalletService.get_or_create_wallet(user_id)
        
        return jsonify({
            'wallet': wallet.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@wallet_bp.route('/transactions', methods=['GET'])
@jwt_required
def get_transactions():
    """Get transaction history"""
    try:
        user_id = get_current_user().id
        
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        balance_type = request.args.get('balance_type')
        
        offset = (page - 1) * per_page
        
        transactions = WalletService.get_transaction_history(
            user_id, 
            limit=per_page, 
            offset=offset,
            balance_type=balance_type
        )
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(transactions)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@wallet_bp.route('/admin/wallets', methods=['GET'])
@admin_required
def get_all_wallets():
    """Get all wallets (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        pagination = Wallet.query.order_by(Wallet.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        wallets = []
        for wallet in pagination.items:
            wallet_data = wallet.to_dict()
            wallet_data['user'] = {
                'id': wallet.user.id,
                'name': wallet.user.name,
                'email': wallet.user.email,
                'role': wallet.user.role
            }
            wallets.append(wallet_data)
        
        return jsonify({
            'wallets': wallets,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@wallet_bp.route('/admin/adjust', methods=['POST'])
@admin_required
def adjust_balance():
    """Adjust user balance (admin only)"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        amount = float(data.get('amount', 0))
        balance_type = data.get('balance_type', 'main')
        description = data.get('description')
        
        if not user_id or amount == 0:
            return jsonify({'error': 'User ID and amount are required'}), 400
        
        admin_id = get_current_user().id
        
        wallet, transaction = WalletService.adjust_balance(
            user_id, amount, balance_type, description, admin_id
        )
        
        return jsonify({
            'message': 'Balance adjusted successfully',
            'wallet': wallet.to_dict(),
            'transaction': transaction.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@wallet_bp.route('/admin/withdrawals', methods=['GET'])
@admin_required
def get_all_withdrawals():
    """Get all withdrawal requests (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        status = request.args.get('status')
        
        query = Withdrawal.query
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(Withdrawal.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        withdrawals = []
        for withdrawal in pagination.items:
            withdrawal_data = withdrawal.to_dict()
            
            # Add user info
            if hasattr(withdrawal, 'agent') and withdrawal.agent:
                withdrawal_data['user'] = {
                    'id': withdrawal.agent.user_id,
                    'name': withdrawal.agent.user.name,
                    'email': withdrawal.agent.user.email
                }
            
            withdrawals.append(withdrawal_data)
        
        return jsonify({
            'withdrawals': withdrawals,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@wallet_bp.route('/admin/withdrawals/<int:withdrawal_id>/approve', methods=['POST'])
@admin_required
def approve_withdrawal(withdrawal_id):
    """Approve withdrawal request (admin only)"""
    try:
        withdrawal = Withdrawal.query.get(withdrawal_id)
        
        if not withdrawal:
            return jsonify({'error': 'Withdrawal not found'}), 404
        
        if withdrawal.status != 'pending':
            return jsonify({'error': 'Withdrawal is not pending'}), 400
        
        admin_id = get_current_user().id
        
        # Update withdrawal status
        withdrawal.status = 'approved'
        withdrawal.approved_by = admin_id
        withdrawal.approved_at = datetime.utcnow()
        
        # Deduct from wallet
        WalletService.deduct_funds(
            withdrawal.agent.user_id,
            float(withdrawal.net_amount),
            balance_type='commission',
            description=f"Withdrawal approved: {withdrawal.id}",
            reference_type='withdrawal',
            reference_id=withdrawal.id,
            created_by=admin_id
        )
        
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal approved successfully',
            'withdrawal': withdrawal.to_dict()
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@wallet_bp.route('/admin/withdrawals/<int:withdrawal_id>/reject', methods=['POST'])
@admin_required
def reject_withdrawal(withdrawal_id):
    """Reject withdrawal request (admin only)"""
    try:
        data = request.get_json()
        reason = data.get('reason', 'No reason provided')
        
        withdrawal = Withdrawal.query.get(withdrawal_id)
        
        if not withdrawal:
            return jsonify({'error': 'Withdrawal not found'}), 404
        
        if withdrawal.status != 'pending':
            return jsonify({'error': 'Withdrawal is not pending'}), 400
        
        admin_id = get_current_user().id
        
        # Update withdrawal status
        withdrawal.status = 'rejected'
        withdrawal.approved_by = admin_id
        withdrawal.approved_at = datetime.utcnow()
        withdrawal.rejection_reason = reason
        
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal rejected successfully',
            'withdrawal': withdrawal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@wallet_bp.route('/admin/withdrawals/<int:withdrawal_id>/complete', methods=['POST'])
@admin_required
def complete_withdrawal(withdrawal_id):
    """Mark withdrawal as completed (admin only)"""
    try:
        data = request.get_json()
        transaction_id = data.get('transaction_id')
        
        withdrawal = Withdrawal.query.get(withdrawal_id)
        
        if not withdrawal:
            return jsonify({'error': 'Withdrawal not found'}), 404
        
        if withdrawal.status not in ['approved', 'processing']:
            return jsonify({'error': 'Withdrawal must be approved first'}), 400
        
        # Update withdrawal status
        withdrawal.status = 'completed'
        withdrawal.completed_at = datetime.utcnow()
        withdrawal.transaction_id = transaction_id
        
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal marked as completed',
            'withdrawal': withdrawal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

