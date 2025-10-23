"""
Analytics routes for advanced dashboard data
"""
from flask import Blueprint, request, jsonify, g
from src.services.analytics_service import AnalyticsService
from src.utils.decorators import token_required, admin_required
from src import cache
import logging

logger = logging.getLogger(__name__)

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/revenue-over-time', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
@token_required
@admin_required
def get_revenue_over_time():
    """Get revenue data over time"""
    try:
        days = request.args.get('days', 30, type=int)
        
        if days < 1 or days > 365:
            return jsonify({'error': 'Days must be between 1 and 365'}), 400
        
        data = AnalyticsService.get_revenue_over_time(days)
        
        return jsonify({
            'data': data,
            'period': f'Last {days} days'
        }), 200
        
    except Exception as e:
        logger.error(f'Error in revenue-over-time endpoint: {str(e)}')
        return jsonify({'error': 'Failed to fetch revenue data'}), 500


@analytics_bp.route('/user-growth', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
@token_required
@admin_required
def get_user_growth():
    """Get user registration growth over time"""
    try:
        days = request.args.get('days', 30, type=int)
        
        if days < 1 or days > 365:
            return jsonify({'error': 'Days must be between 1 and 365'}), 400
        
        data = AnalyticsService.get_user_growth(days)
        
        return jsonify({
            'data': data,
            'period': f'Last {days} days'
        }), 200
        
    except Exception as e:
        logger.error(f'Error in user-growth endpoint: {str(e)}')
        return jsonify({'error': 'Failed to fetch user growth data'}), 500


@analytics_bp.route('/challenge-statistics', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
@token_required
@admin_required
def get_challenge_statistics():
    """Get challenge statistics"""
    try:
        days = request.args.get('days', 30, type=int)
        
        if days < 1 or days > 365:
            return jsonify({'error': 'Days must be between 1 and 365'}), 400
        
        data = AnalyticsService.get_challenge_statistics(days)
        
        return jsonify({
            'data': data,
            'period': f'Last {days} days'
        }), 200
        
    except Exception as e:
        logger.error(f'Error in challenge-statistics endpoint: {str(e)}')
        return jsonify({'error': 'Failed to fetch challenge statistics'}), 500


@analytics_bp.route('/kyc-statistics', methods=['GET'])
@cache.cached(timeout=300)
@token_required
@admin_required
def get_kyc_statistics():
    """Get KYC verification statistics"""
    try:
        data = AnalyticsService.get_kyc_statistics()
        
        return jsonify({
            'data': data
        }), 200
        
    except Exception as e:
        logger.error(f'Error in kyc-statistics endpoint: {str(e)}')
        return jsonify({'error': 'Failed to fetch KYC statistics'}), 500


@analytics_bp.route('/referral-statistics', methods=['GET'])
@cache.cached(timeout=300)
@token_required
@admin_required
def get_referral_statistics():
    """Get referral and MLM statistics"""
    try:
        data = AnalyticsService.get_referral_statistics()
        
        return jsonify({
            'data': data
        }), 200
        
    except Exception as e:
        logger.error(f'Error in referral-statistics endpoint: {str(e)}')
        return jsonify({'error': 'Failed to fetch referral statistics'}), 500


@analytics_bp.route('/payment-statistics', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
@token_required
@admin_required
def get_payment_statistics():
    """Get payment method and status statistics"""
    try:
        days = request.args.get('days', 30, type=int)
        
        if days < 1 or days > 365:
            return jsonify({'error': 'Days must be between 1 and 365'}), 400
        
        data = AnalyticsService.get_payment_statistics(days)
        
        return jsonify({
            'data': data,
            'period': f'Last {days} days'
        }), 200
        
    except Exception as e:
        logger.error(f'Error in payment-statistics endpoint: {str(e)}')
        return jsonify({'error': 'Failed to fetch payment statistics'}), 500


@analytics_bp.route('/comprehensive', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
@token_required
@admin_required
def get_comprehensive_analytics():
    """Get comprehensive analytics data for dashboard"""
    try:
        days = request.args.get('days', 30, type=int)
        
        if days < 1 or days > 365:
            return jsonify({'error': 'Days must be between 1 and 365'}), 400
        
        data = AnalyticsService.get_comprehensive_analytics(days)
        
        return jsonify({
            'data': data,
            'period': f'Last {days} days',
            'generated_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f'Error in comprehensive-analytics endpoint: {str(e)}')
        return jsonify({'error': 'Failed to fetch comprehensive analytics'}), 500


# Import datetime for timestamp
from datetime import datetime

