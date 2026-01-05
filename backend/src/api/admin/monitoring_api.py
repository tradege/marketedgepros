"""
Monitoring Dashboard API Endpoints
Real-time monitoring and management for admins
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database import db
from src.models.trading_program import Challenge
from src.models.mt5_account import MT5Account
from src.models.monitoring import MonitoringEvent, ViolationLog, MonitoringAlert
from src.models.user import User
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
import logging

logger = logging.getLogger(__name__)

# Create blueprint
monitoring_api_bp = Blueprint('monitoring_api', __name__, url_prefix='/api/admin/monitoring')


def require_admin():
    """Decorator to require admin role"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role not in ['admin', 'supermaster']:
        return jsonify({'error': 'Admin access required'}), 403
    return None


@monitoring_api_bp.route('/challenges', methods=['GET'])
@jwt_required()
def get_monitored_challenges():
    """
    Get all active challenges with real-time monitoring data
    """
    # Check admin
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    try:
        # Get filters
        status = request.args.get('status', 'active')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        # Query challenges
        query = Challenge.query
        
        if status == 'active':
            query = query.filter(Challenge.status.in_(['active', 'in_progress']))
        elif status == 'at_risk':
            # Challenges approaching limits (>80% of threshold)
            query = query.filter(Challenge.status.in_(['active', 'in_progress']))
        elif status == 'violated':
            query = query.filter(Challenge.status == 'failed')
        
        # Paginate
        pagination = query.order_by(Challenge.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Build response
        challenges = []
        for challenge in pagination.items:
            daily_stats = challenge.get_daily_stats()
            
            # Calculate risk level
            risk_level = 'low'
            if daily_stats:
                threshold = daily_stats.get('threshold', 0)
                current_equity = daily_stats.get('current_equity', 0)
                remaining_room = daily_stats.get('remaining_room', 0)
                
                if threshold > 0:
                    usage_pct = (1 - remaining_room / (current_equity - threshold + remaining_room)) * 100
                    if usage_pct > 90:
                        risk_level = 'critical'
                    elif usage_pct > 80:
                        risk_level = 'high'
                    elif usage_pct > 60:
                        risk_level = 'medium'
            
            challenges.append({
                'id': challenge.id,
                'user_id': challenge.user_id,
                'user_email': challenge.user.email if challenge.user else None,
                'program_name': challenge.program.name if challenge.program else None,
                'status': challenge.status,
                'account_number': challenge.account_number,
                'initial_balance': float(challenge.initial_balance) if challenge.initial_balance else 0,
                'current_balance': float(challenge.current_balance) if challenge.current_balance else 0,
                'daily_stats': daily_stats,
                'risk_level': risk_level,
                'created_at': challenge.created_at.isoformat() if challenge.created_at else None
            })
        
        return jsonify({
            'challenges': challenges,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting monitored challenges: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@monitoring_api_bp.route('/challenges/<int:challenge_id>', methods=['GET'])
@jwt_required()
def get_challenge_details(challenge_id):
    """
    Get detailed monitoring data for a specific challenge
    """
    # Check admin
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    try:
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        # Get daily stats
        daily_stats = challenge.get_daily_stats()
        
        # Get recent monitoring events
        recent_events = MonitoringEvent.query.filter_by(
            challenge_id=challenge_id
        ).order_by(MonitoringEvent.created_at.desc()).limit(50).all()
        
        # Get violation logs
        violations = ViolationLog.query.filter_by(
            challenge_id=challenge_id
        ).order_by(ViolationLog.created_at.desc()).all()
        
        # Get MT5 account
        mt5_account = MT5Account.query.filter_by(challenge_id=challenge_id).first()
        
        return jsonify({
            'challenge': challenge.to_dict(),
            'daily_stats': daily_stats,
            'mt5_account': mt5_account.to_dict() if mt5_account else None,
            'recent_events': [e.to_dict() for e in recent_events],
            'violations': [v.to_dict() for v in violations]
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting challenge details: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@monitoring_api_bp.route('/violations', methods=['GET'])
@jwt_required()
def get_violations():
    """
    Get recent violations across all challenges
    """
    # Check admin
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    try:
        # Get filters
        days = int(request.args.get('days', 7))
        violation_type = request.args.get('type')
        resolved = request.args.get('resolved')
        
        # Query violations
        query = ViolationLog.query
        
        # Filter by date
        since = datetime.utcnow() - timedelta(days=days)
        query = query.filter(ViolationLog.created_at >= since)
        
        # Filter by type
        if violation_type:
            query = query.filter(ViolationLog.violation_type == violation_type)
        
        # Filter by resolved status
        if resolved is not None:
            query = query.filter(ViolationLog.resolved == (resolved.lower() == 'true'))
        
        # Get violations
        violations = query.order_by(ViolationLog.created_at.desc()).limit(100).all()
        
        # Build response
        result = []
        for violation in violations:
            challenge = Challenge.query.get(violation.challenge_id)
            result.append({
                **violation.to_dict(),
                'challenge': {
                    'id': challenge.id,
                    'user_email': challenge.user.email if challenge.user else None,
                    'program_name': challenge.program.name if challenge.program else None
                } if challenge else None
            })
        
        return jsonify({
            'violations': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting violations: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@monitoring_api_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_monitoring_stats():
    """
    Get monitoring system statistics
    """
    # Check admin
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    try:
        # Active challenges
        active_count = Challenge.query.filter(
            Challenge.status.in_(['active', 'in_progress'])
        ).count()
        
        # Violations today
        today = datetime.utcnow().date()
        violations_today = ViolationLog.query.filter(
            func.date(ViolationLog.created_at) == today
        ).count()
        
        # Violations this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        violations_week = ViolationLog.query.filter(
            ViolationLog.created_at >= week_ago
        ).count()
        
        # At-risk challenges (>80% of limit used)
        at_risk_count = 0
        active_challenges = Challenge.query.filter(
            Challenge.status.in_(['active', 'in_progress'])
        ).all()
        
        for challenge in active_challenges:
            daily_stats = challenge.get_daily_stats()
            if daily_stats:
                threshold = daily_stats.get('threshold', 0)
                current_equity = daily_stats.get('current_equity', 0)
                remaining_room = daily_stats.get('remaining_room', 0)
                
                if threshold > 0:
                    usage_pct = (1 - remaining_room / (current_equity - threshold + remaining_room)) * 100
                    if usage_pct > 80:
                        at_risk_count += 1
        
        # Recent events
        recent_events_count = MonitoringEvent.query.filter(
            MonitoringEvent.created_at >= datetime.utcnow() - timedelta(hours=1)
        ).count()
        
        # System health
        last_sync = MonitoringEvent.query.filter_by(
            event_type='sync'
        ).order_by(MonitoringEvent.created_at.desc()).first()
        
        system_healthy = True
        if last_sync:
            time_since_sync = (datetime.utcnow() - last_sync.created_at).total_seconds()
            if time_since_sync > 120:  # No sync in 2 minutes
                system_healthy = False
        
        return jsonify({
            'active_challenges': active_count,
            'at_risk_challenges': at_risk_count,
            'violations_today': violations_today,
            'violations_week': violations_week,
            'recent_events_hour': recent_events_count,
            'system_healthy': system_healthy,
            'last_sync': last_sync.created_at.isoformat() if last_sync else None
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting monitoring stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@monitoring_api_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    """
    Get recent alerts
    """
    # Check admin
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    try:
        # Get filters
        acknowledged = request.args.get('acknowledged')
        alert_level = request.args.get('level')
        
        # Query alerts
        query = MonitoringAlert.query
        
        # Filter by acknowledged status
        if acknowledged is not None:
            query = query.filter(MonitoringAlert.acknowledged == (acknowledged.lower() == 'true'))
        
        # Filter by level
        if alert_level:
            query = query.filter(MonitoringAlert.alert_level == alert_level)
        
        # Get alerts
        alerts = query.order_by(MonitoringAlert.sent_at.desc()).limit(50).all()
        
        return jsonify({
            'alerts': [a.to_dict() for a in alerts],
            'count': len(alerts)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting alerts: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@monitoring_api_bp.route('/alerts/<int:alert_id>/acknowledge', methods=['POST'])
@jwt_required()
def acknowledge_alert(alert_id):
    """
    Acknowledge an alert
    """
    # Check admin
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    try:
        current_user_id = get_jwt_identity()
        
        alert = MonitoringAlert.query.get(alert_id)
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        alert.acknowledged = True
        alert.acknowledged_at = datetime.utcnow()
        alert.acknowledged_by = current_user_id
        
        db.session.commit()
        
        return jsonify({
            'message': 'Alert acknowledged',
            'alert': alert.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error acknowledging alert: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# Register blueprint in app.py:
"""
from src.api.monitoring_api import monitoring_api_bp
app.register_blueprint(monitoring_api_bp)
"""
