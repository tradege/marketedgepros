"""
Affiliate Program Routes
Handles affiliate registration, tracking, commissions, and payouts
"""
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from sqlalchemy import func
import secrets
import string

from src.database import db
from src.models.affiliate import (
    AffiliateLink, AffiliateReferral, AffiliateCommission,
    AffiliatePayout, AffiliateSettings
)
from src.models.user import User
from src.utils.decorators import token_required, admin_required

affiliate_bp = Blueprint('affiliate', __name__)


def generate_affiliate_code(length=8):
    """Generate unique affiliate code"""
    while True:
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))
        if not AffiliateLink.query.filter_by(code=code).first():
            return code


# ============================================================================
# PUBLIC ROUTES
# ============================================================================

@affiliate_bp.route('/info', methods=['GET'])
def get_affiliate_info():
    """Get affiliate program information"""
    try:
        settings = AffiliateSettings.query.first()
        
        if not settings or not settings.is_active:
            return jsonify({'error': 'Affiliate program is not active'}), 404
        
        return jsonify({
            'program': {
                'is_active': settings.is_active,
                'commission_rate': float(settings.default_commission_rate),
                'min_payout': float(settings.min_payout_amount),
                'cookie_duration_days': settings.cookie_duration_days,
                'terms': settings.terms_and_conditions
            },
            'benefits': [
                f'{float(settings.default_commission_rate)}% commission on all sales',
                f'${float(settings.min_payout_amount)} minimum payout',
                f'{settings.cookie_duration_days}-day cookie duration',
                'Real-time tracking dashboard',
                'Monthly payouts',
                'Dedicated affiliate support'
            ]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get affiliate info error: {str(e)}')
        return jsonify({'error': 'Failed to get affiliate info'}), 500


@affiliate_bp.route('/register', methods=['POST'])
@token_required
def register_affiliate(current_user):
    """Register as an affiliate"""
    try:
        settings = AffiliateSettings.query.first()
        
        if not settings or not settings.is_active:
            return jsonify({'error': 'Affiliate program is not active'}), 400
        
        # Check if user already has an affiliate link
        existing_link = AffiliateLink.query.filter_by(user_id=current_user.id).first()
        if existing_link:
            return jsonify({
                'message': 'You are already registered as an affiliate',
                'link': existing_link.to_dict()
            }), 200
        
        # Create affiliate link
        code = generate_affiliate_code()
        affiliate_link = AffiliateLink(
            user_id=current_user.id,
            code=code,
            name='Default Link',
            commission_rate=settings.default_commission_rate
        )
        
        db.session.add(affiliate_link)
        db.session.commit()
        
        return jsonify({
            'message': 'Successfully registered as affiliate',
            'link': affiliate_link.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Affiliate registration error: {str(e)}')
        return jsonify({'error': 'Failed to register as affiliate'}), 500


# ============================================================================
# AFFILIATE ROUTES (Authenticated Users)
# ============================================================================

@affiliate_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard(current_user):
    """Get affiliate dashboard statistics"""
    try:
        # Get all affiliate links for user
        links = AffiliateLink.query.filter_by(user_id=current_user.id).all()
        
        if not links:
            return jsonify({'error': 'Not registered as affiliate'}), 404
        
        # Calculate totals
        total_clicks = sum(link.clicks for link in links)
        total_conversions = sum(link.conversions for link in links)
        total_revenue = sum(link.total_revenue for link in links)
        total_commission = sum(link.total_commission for link in links)
        
        # Get commission breakdown
        commissions = AffiliateCommission.query.filter_by(affiliate_user_id=current_user.id).all()
        pending_commission = sum(c.amount for c in commissions if c.status == 'pending')
        approved_commission = sum(c.amount for c in commissions if c.status == 'approved')
        paid_commission = sum(c.amount for c in commissions if c.status == 'paid')
        
        # Get recent referrals
        recent_referrals = AffiliateReferral.query.filter_by(
            affiliate_user_id=current_user.id
        ).order_by(AffiliateReferral.click_date.desc()).limit(10).all()
        
        return jsonify({
            'stats': {
                'total_clicks': total_clicks,
                'total_conversions': total_conversions,
                'total_revenue': float(total_revenue),
                'total_commission': float(total_commission),
                'conversion_rate': round((total_conversions / total_clicks * 100) if total_clicks > 0 else 0, 2),
                'pending_commission': float(pending_commission),
                'approved_commission': float(approved_commission),
                'paid_commission': float(paid_commission)
            },
            'links': [link.to_dict() for link in links],
            'recent_referrals': [ref.to_dict() for ref in recent_referrals]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get affiliate dashboard error: {str(e)}')
        return jsonify({'error': 'Failed to get dashboard'}), 500


@affiliate_bp.route('/links', methods=['GET'])
@token_required
def get_affiliate_links(current_user):
    """Get all affiliate links for current user"""
    try:
        links = AffiliateLink.query.filter_by(user_id=current_user.id).all()
        return jsonify({'links': [link.to_dict() for link in links]}), 200
        
    except Exception as e:
        current_app.logger.error(f'Get affiliate links error: {str(e)}')
        return jsonify({'error': 'Failed to get links'}), 500


@affiliate_bp.route('/links', methods=['POST'])
@token_required
def create_affiliate_link(current_user):
    """Create new affiliate link"""
    try:
        data = request.get_json()
        name = data.get('name', 'Custom Link')
        
        # Generate unique code
        code = generate_affiliate_code()
        
        # Get default commission rate
        settings = AffiliateSettings.query.first()
        
        affiliate_link = AffiliateLink(
            user_id=current_user.id,
            code=code,
            name=name,
            commission_rate=settings.default_commission_rate if settings else 10.00
        )
        
        db.session.add(affiliate_link)
        db.session.commit()
        
        return jsonify({
            'message': 'Affiliate link created',
            'link': affiliate_link.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Create affiliate link error: {str(e)}')
        return jsonify({'error': 'Failed to create link'}), 500


@affiliate_bp.route('/referrals', methods=['GET'])
@token_required
def get_referrals(current_user):
    """Get all referrals for current user"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        query = AffiliateReferral.query.filter_by(affiliate_user_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        referrals = query.order_by(AffiliateReferral.click_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'referrals': [ref.to_dict() for ref in referrals.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': referrals.total,
                'pages': referrals.pages
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get referrals error: {str(e)}')
        return jsonify({'error': 'Failed to get referrals'}), 500


@affiliate_bp.route('/commissions', methods=['GET'])
@token_required
def get_commissions(current_user):
    """Get all commissions for current user"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        query = AffiliateCommission.query.filter_by(affiliate_user_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        commissions = query.order_by(AffiliateCommission.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'commissions': [comm.to_dict() for comm in commissions.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': commissions.total,
                'pages': commissions.pages
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get commissions error: {str(e)}')
        return jsonify({'error': 'Failed to get commissions'}), 500


@affiliate_bp.route('/payout', methods=['POST'])
@token_required
def request_payout(current_user):
    """Request payout"""
    try:
        data = request.get_json()
        method = data.get('method')
        payment_details = data.get('payment_details')
        
        if not method or not payment_details:
            return jsonify({'error': 'Method and payment details required'}), 400
        
        # Get approved commissions
        approved_commissions = AffiliateCommission.query.filter_by(
            affiliate_user_id=current_user.id,
            status='approved',
            payout_id=None
        ).all()
        
        if not approved_commissions:
            return jsonify({'error': 'No approved commissions available'}), 400
        
        total_amount = sum(c.amount for c in approved_commissions)
        
        # Check minimum payout
        settings = AffiliateSettings.query.first()
        if settings and total_amount < settings.min_payout_amount:
            return jsonify({
                'error': f'Minimum payout amount is ${float(settings.min_payout_amount)}'
            }), 400
        
        # Check minimum unique customers (10 required)
        from sqlalchemy import func
        unique_customers = db.session.query(
            func.count(func.distinct(AffiliateReferral.referred_user_id))
        ).filter(
            AffiliateReferral.affiliate_user_id == current_user.id,
            AffiliateReferral.status == 'converted'
        ).scalar() or 0
        
        if unique_customers < 10:
            return jsonify({
                'error': f'You need {10 - unique_customers} more unique customers to request payout. Current: {unique_customers}/10'
            }), 400
        
        
        # Create payout request
        payout = AffiliatePayout(
            affiliate_user_id=current_user.id,
            amount=total_amount,
            method=method,
            payment_details=payment_details
        )
        
        db.session.add(payout)
        db.session.flush()
        
        # Link commissions to payout
        for commission in approved_commissions:
            commission.payout_id = payout.id
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payout requested successfully',
            'payout': payout.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Request payout error: {str(e)}')
        return jsonify({'error': 'Failed to request payout'}), 500


@affiliate_bp.route('/payouts', methods=['GET'])
@token_required
def get_payouts(current_user):
    """Get all payouts for current user"""
    try:
        payouts = AffiliatePayout.query.filter_by(
            affiliate_user_id=current_user.id
        ).order_by(AffiliatePayout.requested_at.desc()).all()
        
        return jsonify({'payouts': [p.to_dict() for p in payouts]}), 200
        
    except Exception as e:
        current_app.logger.error(f'Get payouts error: {str(e)}')
        return jsonify({'error': 'Failed to get payouts'}), 500


# ============================================================================
# ADMIN ROUTES
# ============================================================================

@affiliate_bp.route('/admin/affiliates', methods=['GET'])
@admin_required
def get_all_affiliates(current_user):
    """Get all affiliates (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Get all users with affiliate links
        affiliates = db.session.query(User, AffiliateLink).join(
            AffiliateLink, User.id == AffiliateLink.user_id
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        result = []
        for user, link in affiliates.items:
            result.append({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': f'{user.first_name} {user.last_name}'
                },
                'link': link.to_dict()
            })
        
        return jsonify({
            'affiliates': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': affiliates.total,
                'pages': affiliates.pages
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get all affiliates error: {str(e)}')
        return jsonify({'error': 'Failed to get affiliates'}), 500


@affiliate_bp.route('/admin/payouts', methods=['GET'])
@admin_required
def get_all_payouts(current_user):
    """Get all payout requests (admin only)"""
    try:
        status = request.args.get('status')
        
        query = AffiliatePayout.query
        
        if status:
            query = query.filter_by(status=status)
        
        payouts = query.order_by(AffiliatePayout.requested_at.desc()).all()
        
        result = []
        for payout in payouts:
            result.append({
                **payout.to_dict(),
                'affiliate': {
                    'id': payout.affiliate_user.id,
                    'email': payout.affiliate_user.email,
                    'name': f'{payout.affiliate_user.first_name} {payout.affiliate_user.last_name}'
                }
            })
        
        return jsonify({'payouts': result}), 200
        
    except Exception as e:
        current_app.logger.error(f'Get all payouts error: {str(e)}')
        return jsonify({'error': 'Failed to get payouts'}), 500


@affiliate_bp.route('/admin/payout/<int:payout_id>/process', methods=['POST'])
@admin_required
def process_payout(current_user, payout_id):
    """Process payout (admin only)"""
    try:
        data = request.get_json()
        status = data.get('status')  # completed or failed
        transaction_id = data.get('transaction_id')
        notes = data.get('notes')
        
        payout = AffiliatePayout.query.get(payout_id)
        
        if not payout:
            return jsonify({'error': 'Payout not found'}), 404
        
        payout.status = status
        payout.transaction_id = transaction_id
        payout.notes = notes
        payout.processed_at = datetime.utcnow()
        
        if status == 'completed':
            payout.completed_at = datetime.utcnow()
            # Mark commissions as paid
            for commission in payout.commissions:
                commission.status = 'paid'
                commission.paid_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payout processed successfully',
            'payout': payout.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Process payout error: {str(e)}')
        return jsonify({'error': 'Failed to process payout'}), 500


@affiliate_bp.route('/admin/settings', methods=['GET', 'PUT'])
@admin_required
def manage_settings(current_user):
    """Get or update affiliate settings (admin only)"""
    try:
        settings = AffiliateSettings.query.first()
        
        if not settings:
            settings = AffiliateSettings()
            db.session.add(settings)
            db.session.commit()
        
        if request.method == 'GET':
            return jsonify({'settings': settings.to_dict()}), 200
        
        # PUT - Update settings
        data = request.get_json()
        
        if 'default_commission_rate' in data:
            settings.default_commission_rate = data['default_commission_rate']
        if 'min_payout_amount' in data:
            settings.min_payout_amount = data['min_payout_amount']
        if 'cookie_duration_days' in data:
            settings.cookie_duration_days = data['cookie_duration_days']
        if 'is_active' in data:
            settings.is_active = data['is_active']
        if 'auto_approve_affiliates' in data:
            settings.auto_approve_affiliates = data['auto_approve_affiliates']
        if 'auto_approve_commissions' in data:
            settings.auto_approve_commissions = data['auto_approve_commissions']
        if 'terms_and_conditions' in data:
            settings.terms_and_conditions = data['terms_and_conditions']
        
        settings.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Settings updated successfully',
            'settings': settings.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Manage settings error: {str(e)}')
        return jsonify({'error': 'Failed to manage settings'}), 500

