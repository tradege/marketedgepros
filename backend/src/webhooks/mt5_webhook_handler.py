"""
MT5 Webhook Handler
Receives real-time trade events from MT5 and triggers immediate checks
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.mt5_account import MT5Account
from src.tasks.monitoring import sync_challenge_immediate
import hmac
import hashlib
import logging

logger = logging.getLogger(__name__)

# Create blueprint
mt5_webhooks_bp = Blueprint('mt5_webhooks', __name__, url_prefix='/webhooks/mt5')


def verify_mt5_signature(data, signature, secret_key):
    """
    Verify webhook signature from MT5
    """
    try:
        # Create HMAC signature
        message = str(data).encode('utf-8')
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            message,
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        return hmac.compare_digest(expected_signature, signature)
        
    except Exception as e:
        logger.error(f"Error verifying signature: {str(e)}")
        return False


@mt5_webhooks_bp.route('/trade', methods=['POST'])
def trade_webhook():
    """
    Handle trade events from MT5
    Triggered on: trade open, trade close, trade modify
    """
    try:
        # Get data
        data = request.json
        signature = request.headers.get('X-MT5-Signature', '')
        
        # Verify signature
        secret_key = app.config.get('MT5_WEBHOOK_SECRET')
        if not verify_mt5_signature(data, signature, secret_key):
            logger.warning(f"Invalid webhook signature from {request.remote_addr}")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Extract data
        mt5_login = data.get('login')
        trade_ticket = data.get('ticket')
        trade_type = data.get('type')  # 'open', 'close', 'modify'
        
        logger.info(f"Trade webhook received: login={mt5_login}, ticket={trade_ticket}, type={trade_type}")
        
        # Find MT5 account
        mt5_account = MT5Account.query.filter_by(mt5_login=mt5_login).first()
        if not mt5_account:
            logger.warning(f"MT5 account not found: {mt5_login}")
            return jsonify({'error': 'Account not found'}), 404
        
        # Trigger immediate sync
        sync_challenge_immediate.delay(mt5_account.challenge_id)
        
        return jsonify({
            'status': 'ok',
            'message': 'Sync triggered',
            'challenge_id': mt5_account.challenge_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error handling trade webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@mt5_webhooks_bp.route('/balance', methods=['POST'])
def balance_webhook():
    """
    Handle balance update events from MT5
    Triggered on: deposit, withdrawal, balance adjustment
    """
    try:
        # Get data
        data = request.json
        signature = request.headers.get('X-MT5-Signature', '')
        
        # Verify signature
        secret_key = app.config.get('MT5_WEBHOOK_SECRET')
        if not verify_mt5_signature(data, signature, secret_key):
            logger.warning(f"Invalid webhook signature from {request.remote_addr}")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Extract data
        mt5_login = data.get('login')
        balance_change = data.get('balance_change')
        new_balance = data.get('new_balance')
        
        logger.info(f"Balance webhook received: login={mt5_login}, change={balance_change}, new={new_balance}")
        
        # Find MT5 account
        mt5_account = MT5Account.query.filter_by(mt5_login=mt5_login).first()
        if not mt5_account:
            logger.warning(f"MT5 account not found: {mt5_login}")
            return jsonify({'error': 'Account not found'}), 404
        
        # Trigger immediate sync
        sync_challenge_immediate.delay(mt5_account.challenge_id)
        
        return jsonify({
            'status': 'ok',
            'message': 'Sync triggered',
            'challenge_id': mt5_account.challenge_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error handling balance webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@mt5_webhooks_bp.route('/equity', methods=['POST'])
def equity_webhook():
    """
    Handle equity update events from MT5
    Triggered on: floating P/L changes (every tick for open positions)
    """
    try:
        # Get data
        data = request.json
        signature = request.headers.get('X-MT5-Signature', '')
        
        # Verify signature
        secret_key = app.config.get('MT5_WEBHOOK_SECRET')
        if not verify_mt5_signature(data, signature, secret_key):
            logger.warning(f"Invalid webhook signature from {request.remote_addr}")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Extract data
        mt5_login = data.get('login')
        equity = data.get('equity')
        
        # Find MT5 account
        mt5_account = MT5Account.query.filter_by(mt5_login=mt5_login).first()
        if not mt5_account:
            return jsonify({'error': 'Account not found'}), 404
        
        # Only sync if equity changed significantly (> 0.1%)
        if mt5_account.last_equity:
            change_pct = abs(equity - mt5_account.last_equity) / mt5_account.last_equity * 100
            if change_pct < 0.1:
                return jsonify({'status': 'ok', 'message': 'Change too small, skipped'}), 200
        
        # Update last equity
        mt5_account.last_equity = equity
        db.session.commit()
        
        # Trigger immediate sync
        sync_challenge_immediate.delay(mt5_account.challenge_id)
        
        return jsonify({
            'status': 'ok',
            'message': 'Sync triggered',
            'challenge_id': mt5_account.challenge_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error handling equity webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@mt5_webhooks_bp.route('/status', methods=['GET'])
def webhook_status():
    """
    Health check endpoint for webhooks
    """
    return jsonify({
        'status': 'ok',
        'service': 'MT5 Webhook Handler',
        'endpoints': [
            '/webhooks/mt5/trade',
            '/webhooks/mt5/balance',
            '/webhooks/mt5/equity'
        ]
    }), 200


# Register blueprint in app.py:
"""
from src.webhooks.mt5_webhook_handler import mt5_webhooks_bp
app.register_blueprint(mt5_webhooks_bp)
"""
