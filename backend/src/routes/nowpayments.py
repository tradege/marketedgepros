from flask import Blueprint, request, jsonify
import requests
import os
import logging
from src.middleware.auth import jwt_required, get_current_user

nowpayments_bp = Blueprint('nowpayments', __name__)

# NOWPayments API Configuration
# SECURITY: API key moved to environment variable
NOWPAYMENTS_API_KEY = os.getenv('NOWPAYMENTS_API_KEY')
NOWPAYMENTS_API_URL = os.getenv('NOWPAYMENTS_API_URL', 'https://api.nowpayments.io/v1')

# Validate API key is set
if not NOWPAYMENTS_API_KEY:
    logger.error('NOWPAYMENTS_API_KEY environment variable is not set!')
    raise ValueError('NOWPAYMENTS_API_KEY must be set in environment variables')

logger = logging.getLogger(__name__)

@nowpayments_bp.route('/api/crypto/create-payment', methods=['POST'])
@jwt_required
def create_crypto_payment():
    """Create a new crypto payment via NOWPayments"""
    try:
        data = request.get_json()
        
        # Extract payment details
        program_id = data.get('program_id')
        amount = data.get('amount')  # in USD
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
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            payment_info = response.json()
            return jsonify({
                'success': True,
                'payment_id': payment_info.get('payment_id'),
                'payment_url': payment_info.get('invoice_url'),
                'pay_address': payment_info.get('pay_address'),
                'pay_amount': payment_info.get('pay_amount'),
                'pay_currency': payment_info.get('pay_currency'),
                'order_id': payment_info.get('order_id')
            }), 201
        else:
            logger.error(f'NOWPayments error: {response.text}')
            return jsonify({'error': 'Failed to create payment', 'details': response.text}), 500
            
    except Exception as e:
        logger.error(f'Error creating crypto payment: {str(e)}')
        return jsonify({'error': str(e)}), 500


@nowpayments_bp.route('/api/crypto/payment-status/<payment_id>', methods=['GET'])
@jwt_required
def get_payment_status(payment_id):
    """Get payment status from NOWPayments"""
    try:
        headers = {
            'x-api-key': NOWPAYMENTS_API_KEY
        }
        
        response = requests.get(
            f'{NOWPAYMENTS_API_URL}/payment/{payment_id}',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            payment_info = response.json()
            return jsonify({
                'success': True,
                'status': payment_info.get('payment_status'),
                'pay_amount': payment_info.get('pay_amount'),
                'actually_paid': payment_info.get('actually_paid'),
                'outcome_amount': payment_info.get('outcome_amount')
            }), 200
        else:
            return jsonify({'error': 'Payment not found'}), 404
            
    except Exception as e:
        logger.error(f'Error getting payment status: {str(e)}')
        return jsonify({'error': str(e)}), 500


@nowpayments_bp.route('/api/crypto/webhook', methods=['POST'])
def payment_webhook():
    """Handle NOWPayments IPN webhook"""
    try:
        data = request.get_json()
        
        payment_id = data.get('payment_id')
        payment_status = data.get('payment_status')
        order_id = data.get('order_id')
        
        logger.info(f'Received webhook for payment {payment_id}: {payment_status}')
        
        # Handle different payment statuses
        if payment_status == 'finished':
            # Payment completed successfully
            # TODO: Update database, activate user account, send confirmation email
            logger.info(f'Payment {payment_id} completed successfully')
            
        elif payment_status == 'failed':
            # Payment failed
            logger.warning(f'Payment {payment_id} failed')
            
        elif payment_status == 'expired':
            # Payment expired
            logger.warning(f'Payment {payment_id} expired')
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        logger.error(f'Error processing webhook: {str(e)}')
        return jsonify({'error': str(e)}), 500


@nowpayments_bp.route('/api/crypto/currencies', methods=['GET'])
@jwt_required
def get_available_currencies():
    """Get list of available cryptocurrencies"""
    try:
        headers = {
            'x-api-key': NOWPAYMENTS_API_KEY
        }
        
        response = requests.get(
            f'{NOWPAYMENTS_API_URL}/currencies',
            headers=headers,
            timeout=10
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
        logger.error(f'Error getting currencies: {str(e)}')
        return jsonify({'error': str(e)}), 500

