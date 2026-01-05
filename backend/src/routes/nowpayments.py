from flask import Blueprint, request, jsonify
import requests
import os
import logging
import hmac
import hashlib

logger = logging.getLogger(__name__)

nowpayments_bp = Blueprint('nowpayments', __name__)

# NOWPayments API configuration
NOWPAYMENTS_API_KEY = os.getenv('NOWPAYMENTS_API_KEY')
NOWPAYMENTS_API_URL = 'https://api.nowpayments.io/v1'

@nowpayments_bp.route('/api/crypto/create-payment', methods=['POST'])
def create_crypto_payment():
    """Create a new crypto payment - Public API (no authentication required)"""
    try:
        data = request.get_json()
        
        program_id = data.get('program_id')
        amount = data.get('amount')
        user_email = data.get('email')
        order_id = data.get('order_id', f'order_{program_id}_{user_email}')
        
        if not all([program_id, amount, user_email]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create payment request to NOWPayments
        headers = {
            'x-api-key': NOWPAYMENTS_API_KEY,
            'Content-Type': 'application/json'
        }
        
        payment_data = {
            'price_amount': float(amount),
            'price_currency': 'usd',
            'pay_currency': 'usdttrc20',  # USDT TRC20
            'ipn_callback_url': f'https://marketedgepros.com/api/crypto/webhook',
            'order_id': order_id,
            'order_description': f'Program {program_id} Purchase'
        }
        
        # Make request to NOWPayments
        response = requests.post(
            f'{NOWPAYMENTS_API_URL}/payment',
            json=payment_data,
            headers=headers
        )
        
        if response.status_code == 200 or response.status_code == 201:
            payment_info = response.json()
            return jsonify({
                'success': True,
                'payment_id': payment_info.get('payment_id'),
                'order_id': payment_info.get('order_id'),
                'payment_url': payment_info.get('invoice_url'),
                'pay_address': payment_info.get('pay_address'),
                'pay_amount': payment_info.get('pay_amount'),
                'pay_currency': payment_info.get('pay_currency')
            }), 201
        else:
            logger.error(f"NOWPayments API error: {response.text}")
            return jsonify({'error': 'Failed to create payment'}), 500
            
    except Exception as e:
        logger.error(f"Error creating crypto payment: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@nowpayments_bp.route('/api/crypto/payment-status/<payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    """Get payment status - Public API (no authentication required)"""
    try:
        headers = {
            'x-api-key': NOWPAYMENTS_API_KEY
        }
        
        response = requests.get(
            f'{NOWPAYMENTS_API_URL}/payment/{payment_id}',
            headers=headers
        )
        
        if response.status_code == 200:
            payment_info = response.json()
            return jsonify({
                'success': True,
                'status': payment_info.get('payment_status'),
                'pay_amount': payment_info.get('pay_amount'),
                'actually_paid': payment_info.get('actually_paid'),
                'outcome_amount': payment_info.get('outcome_amount'),
                'pay_currency': payment_info.get('pay_currency')
            }), 200
        else:
            return jsonify({'error': 'Payment not found'}), 404
            
    except Exception as e:
        logger.error(f"Error getting payment status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@nowpayments_bp.route('/api/crypto/webhook', methods=['POST'])
def payment_webhook():
    """Handle NOWPayments webhook - Public API (no authentication required)"""
    try:
        data = request.get_json()
        
        # Verify webhook signature
        signature = request.headers.get('x-nowpayments-sig')
        if not verify_webhook_signature(request.data, signature):
            logger.warning("Invalid webhook signature")
            return jsonify({'error': 'Invalid signature'}), 401
        
        payment_status = data.get('payment_status')
        order_id = data.get('order_id')
        
        logger.info(f"Webhook received for order {order_id}: {payment_status}")
        
        # Handle different payment statuses
        if payment_status == 'finished':
            # Payment completed successfully
            # TODO: Create user account and send MT5 credentials
            logger.info(f"Payment completed for order {order_id}")
            
        elif payment_status == 'failed':
            logger.warning(f"Payment failed for order {order_id}")
            
        return jsonify({'success': True}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@nowpayments_bp.route('/api/crypto/currencies', methods=['GET'])
def get_available_currencies():
    """Get available cryptocurrencies - Public API (no authentication required)"""
    try:
        headers = {
            'x-api-key': NOWPAYMENTS_API_KEY
        }
        
        response = requests.get(
            f'{NOWPAYMENTS_API_URL}/currencies',
            headers=headers
        )
        
        if response.status_code == 200:
            currencies = response.json()
            return jsonify({
                'success': True,
                'currencies': currencies.get('currencies', [])
            }), 200
        else:
            return jsonify({'error': 'Failed to fetch currencies'}), 500
            
    except Exception as e:
        logger.error(f"Error getting currencies: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def verify_webhook_signature(payload, signature):
    """Verify NOWPayments webhook signature"""
    try:
        ipn_secret = os.getenv('NOWPAYMENTS_IPN_SECRET')
        if not ipn_secret:
            return True  # Skip verification if no secret configured
            
        expected_signature = hmac.new(
            ipn_secret.encode('utf-8'),
            payload,
            hashlib.sha512
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    except Exception as e:
        logger.error(f"Error verifying signature: {str(e)}")
        return False
