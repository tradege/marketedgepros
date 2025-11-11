"""
Payment routes for Stripe integration
"""
from flask import Blueprint, request, jsonify, g
from src.database import db
from src.models import Challenge
from src.services.payment_service import PaymentService
from src.services.email_service import EmailService
from src.utils.decorators import token_required
import logging

logger = logging.getLogger(__name__)

payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/create-payment-intent', methods=['POST'])
@token_required
def create_payment_intent():
    """Create payment intent for challenge purchase"""
    data = request.get_json()
    
    if 'challenge_id' not in data:
        return jsonify({'error': 'Challenge ID is required'}), 400
    
    try:
        # Get challenge
        challenge = Challenge.query.get(data['challenge_id'])
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        # Verify ownership
        if challenge.user_id != g.current_user.id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Check if already paid
        if challenge.payment_status == 'paid':
            return jsonify({'error': 'Challenge already paid'}), 400
        
        # Create payment intent
        payment_data = PaymentService.create_payment_intent(challenge, g.current_user)
        
        return jsonify({
            'message': 'Payment intent created',
            'payment': payment_data
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Payment intent creation failed: {str(e)}')
        return jsonify({'error': 'Failed to create payment'}), 500


@payments_bp.route('/confirm-payment', methods=['POST'])
@token_required
def confirm_payment():
    """Confirm payment after successful Stripe payment"""
    data = request.get_json()
    
    if 'payment_intent_id' not in data:
        return jsonify({'error': 'Payment intent ID is required'}), 400
    
    try:
        # Confirm payment
        success = PaymentService.confirm_payment(data['payment_intent_id'])
        
        if not success:
            return jsonify({'error': 'Payment confirmation failed'}), 400
        
        # Get challenge
        challenge = Challenge.query.filter_by(
            payment_id=data['payment_intent_id']
        ).first()
        
        if challenge:
            # Send confirmation email
            EmailService.send_challenge_purchased_email(
                g.current_user,
                challenge,
                challenge.program
            )
        
        return jsonify({
            'message': 'Payment confirmed successfully',
            'challenge': challenge.to_dict() if challenge else None
        }), 200
        
    except Exception as e:
        logger.error(f'Payment confirmation failed: {str(e)}')
        return jsonify({'error': 'Failed to confirm payment'}), 500


@payments_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    if not sig_header:
        return jsonify({'error': 'Missing signature'}), 400
    
    try:
        success = PaymentService.handle_webhook(payload, sig_header)
        
        if success:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'error': 'Webhook handling failed'}), 400
            
    except Exception as e:
        logger.error(f'Webhook error: {str(e)}')
        return jsonify({'error': 'Webhook processing failed'}), 500


@payments_bp.route('/refund/<int:challenge_id>', methods=['POST'])
@token_required
def refund_payment(challenge_id):
    """Request refund for a challenge"""
    try:
        challenge = Challenge.query.get_or_404(challenge_id)
        
        # Verify ownership or admin
        if challenge.user_id != g.current_user.id and g.current_user.role != 'admin':
            return jsonify({'error': 'Access denied'}), 403
        
        # Check if refundable
        if challenge.payment_status != 'paid':
            return jsonify({'error': 'Challenge is not paid'}), 400
        
        # Process refund
        data = request.get_json() or {}
        refund_data = PaymentService.refund_payment(
            challenge,
            reason=data.get('reason')
        )
        
        return jsonify({
            'message': 'Refund processed successfully',
            'refund': refund_data
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Refund failed: {str(e)}')
        return jsonify({'error': 'Failed to process refund'}), 500


@payments_bp.route('/status/<payment_intent_id>', methods=['GET'])
@token_required
def get_payment_status(payment_intent_id):
    """Get payment status"""
    try:
        status = PaymentService.get_payment_status(payment_intent_id)
        
        if not status:
            return jsonify({'error': 'Payment not found'}), 404
        
        return jsonify(status), 200
        
    except Exception as e:
        logger.error(f'Failed to get payment status: {str(e)}')
        return jsonify({'error': 'Failed to get payment status'}), 500

