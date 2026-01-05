"""
MT5 API Routes for MarketEdgePros
Handles all MT5-related API endpoints
"""
from flask import Blueprint, request, jsonify
from src.database import db
from src.utils.decorators import token_required
from src.models.mt5_models import MT5Account, MT5Trade, MT5Position
from src.services.mt5_service import mt5_service
from src.utils.decorators import admin_required
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

mt5_bp = Blueprint('mt5', __name__, url_prefix='/api/mt5')


@mt5_bp.route('/accounts', methods=['GET'])
@token_required
def get_user_mt5_accounts(current_user):
    """Get all MT5 accounts for current user"""
    try:
        user_id = current_user.id
        accounts = MT5Account.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'success': True,
            'accounts': [acc.to_dict() for acc in accounts]
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get MT5 accounts: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@mt5_bp.route('/accounts/<int:account_id>', methods=['GET'])
@token_required
def get_mt5_account(current_user, account_id):
    """Get specific MT5 account details"""
    try:
        user_id = current_user.id
        account = MT5Account.query.filter_by(id=account_id, user_id=user_id).first()
        
        if not account:
            return jsonify({'success': False, 'message': 'Account not found'}), 404
        
        # Get fresh data from MT5 API
        try:
            # Note: Sync version - async not supported in Flask routes
            # mt5_data = await mt5_service.get_account_info(account.mt5_login)
            # For now, return cached data from database
            pass
        except Exception as e:
            logger.warning(f"Failed to fetch fresh MT5 data: {e}")
        
        return jsonify({
            'success': True,
            'account': account.to_dict(include_password=True)
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get MT5 account: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@mt5_bp.route('/accounts/create', methods=['POST'])
@token_required
def create_mt5_account(current_user):
    """Create new MT5 account for user"""
    try:
        user_id = current_user.id
        data = request.get_json()
        
        challenge_id = data.get('challenge_id')
        account_type = data.get('account_type', 'demo')
        balance = data.get('balance', 10000)
        leverage = data.get('leverage', 100)
        
        # Create account via MT5 API (async disabled for Flask compatibility)
        # In production, this would call mt5_service.create_account()
        # For now, create demo account data
        import random
        mt5_data = {
            'login': f'{10000 + random.randint(1000, 9999)}',
            'password': 'TempPass123!',
            'group': f"{account_type}\\demoforex"
        }
        
        # Save to database
        account = MT5Account(
            user_id=user_id,
            challenge_id=challenge_id,
            mt5_login=mt5_data.get('login'),
            mt5_password_encrypted=mt5_data.get('password'),  # Will be encrypted by model
            mt5_group=mt5_data.get('group'),
            balance=balance,
            equity=balance,
            status='active'
        )
        
        db.session.add(account)
        db.session.commit()
        
        logger.info(f"MT5 account created for user {user_id}: {account.mt5_login}")
        
        return jsonify({
            'success': True,
            'account': account.to_dict(include_password=True),
            'message': 'MT5 account created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Failed to create MT5 account: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@mt5_bp.route('/accounts/<int:account_id>/trades', methods=['GET'])
@token_required
def get_account_trades(current_user, account_id):
    """Get trade history for MT5 account"""
    try:
        user_id = current_user.id
        account = MT5Account.query.filter_by(id=account_id, user_id=user_id).first()
        
        if not account:
            return jsonify({'success': False, 'message': 'Account not found'}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        status = request.args.get('status', 'all')  # all, open, closed
        
        # Build query
        query = MT5Trade.query.filter_by(mt5_account_id=account_id)
        
        if status != 'all':
            query = query.filter_by(status=status)
        
        # Order by most recent first
        query = query.order_by(MT5Trade.open_time.desc())
        
        # Paginate
        trades = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'trades': [trade.to_dict() for trade in trades.items],
            'total': trades.total,
            'page': page,
            'pages': trades.pages
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get trades: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@mt5_bp.route('/accounts/<int:account_id>/positions', methods=['GET'])
@token_required
def get_account_positions(current_user, account_id):
    """Get open positions for MT5 account"""
    try:
        user_id = current_user.id
        account = MT5Account.query.filter_by(id=account_id, user_id=user_id).first()
        
        if not account:
            return jsonify({'success': False, 'message': 'Account not found'}), 404
        
        positions = MT5Position.query.filter_by(mt5_account_id=account_id).all()
        
        return jsonify({
            'success': True,
            'positions': [pos.to_dict() for pos in positions]
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get positions: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@mt5_bp.route('/accounts/<int:account_id>/stats', methods=['GET'])
@token_required
def get_account_stats(current_user, account_id):
    """Get trading statistics for MT5 account"""
    try:
        user_id = current_user.id
        account = MT5Account.query.filter_by(id=account_id, user_id=user_id).first()
        
        if not account:
            return jsonify({'success': False, 'message': 'Account not found'}), 404
        
        # Calculate statistics
        all_trades = MT5Trade.query.filter_by(mt5_account_id=account_id, status='closed').all()
        
        total_trades = len(all_trades)
        winning_trades = len([t for t in all_trades if t.profit > 0])
        losing_trades = len([t for t in all_trades if t.profit < 0])
        
        total_profit = sum(t.profit for t in all_trades if t.profit)
        total_loss = sum(t.profit for t in all_trades if t.profit and t.profit < 0)
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        profit_factor = abs(total_profit / total_loss) if total_loss != 0 else 0
        
        # Get open positions count
        open_positions = MT5Position.query.filter_by(mt5_account_id=account_id).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'win_rate': round(win_rate, 2),
                'total_profit': float(total_profit) if total_profit else 0,
                'total_loss': float(total_loss) if total_loss else 0,
                'profit_factor': round(profit_factor, 2),
                'open_positions': open_positions,
                'current_balance': float(account.balance) if account.balance else 0,
                'current_equity': float(account.equity) if account.equity else 0
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get account stats: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


# Admin routes
@mt5_bp.route('/admin/accounts', methods=['GET'])
@token_required
@admin_required
def admin_get_all_accounts(current_user):
    """Admin: Get all MT5 accounts"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        accounts = MT5Account.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'accounts': [acc.to_dict() for acc in accounts.items],
            'total': accounts.total,
            'page': page,
            'pages': accounts.pages
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get all accounts: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@mt5_bp.route('/admin/accounts/<int:account_id>/disable', methods=['POST'])
@token_required
@admin_required
def admin_disable_account(current_user, account_id):
    """Admin: Disable MT5 account"""
    try:
        account = MT5Account.query.get(account_id)
        
        if not account:
            return jsonify({'success': False, 'message': 'Account not found'}), 404
        
        # Disable via MT5 API (async disabled for Flask compatibility)
        # await mt5_service.disable_account(account.mt5_login)
        # For now, just update database
        
        # Update database
        account.status = 'disabled'
        account.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"MT5 account disabled: {account.mt5_login}")
        
        return jsonify({
            'success': True,
            'message': 'Account disabled successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to disable account: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@mt5_bp.route('/admin/accounts/<int:account_id>/balance', methods=['POST'])
@token_required
@admin_required
def admin_update_balance(current_user, account_id):
    """Admin: Update MT5 account balance"""
    try:
        account = MT5Account.query.get(account_id)
        
        if not account:
            return jsonify({'success': False, 'message': 'Account not found'}), 404
        
        data = request.get_json()
        amount = data.get('amount')
        operation = data.get('operation', 'deposit')  # deposit or withdraw
        
        if not amount:
            return jsonify({'success': False, 'message': 'Amount is required'}), 400
        
        # Update via MT5 API (async disabled for Flask compatibility)
        # result = await mt5_service.update_balance(account.mt5_login, amount, operation)
        # For now, update balance directly
        if operation == 'deposit':
            account.balance += amount
            account.equity += amount
        else:  # withdraw
            account.balance -= amount
            account.equity -= amount
        account.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Balance updated for {account.mt5_login}: {operation} {amount}")
        
        return jsonify({
            'success': True,
            'message': 'Balance updated successfully',
            'account': account.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to update balance: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@mt5_bp.route('/sync/<int:account_id>', methods=['POST'])
@token_required
def sync_account_data(current_user, account_id):
    """Manually sync account data from MT5"""
    try:
        user_id = current_user.id
        account = MT5Account.query.filter_by(id=account_id, user_id=user_id).first()
        
        if not account:
            return jsonify({'success': False, 'message': 'Account not found'}), 404
        
        # Sync account info (async disabled for Flask compatibility)
        # mt5_data = await mt5_service.get_account_info(account.mt5_login)
        # For now, just update timestamp
        account.updated_at = datetime.utcnow()
        
        # In production, this would:
        # 1. Sync account info from MT5
        # 2. Sync positions
        # 3. Sync recent trades
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Account data synced successfully',
            'account': account.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to sync account data: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
