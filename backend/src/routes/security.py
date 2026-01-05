"""
Security monitoring routes
"""
from flask import Blueprint, jsonify, request
from src.models.verification_attempt import VerificationAttempt
from src.services.email_service import EmailService
from src.utils.decorators import token_required
import logging

security_bp = Blueprint('security', __name__)
logger = logging.getLogger(__name__)


@security_bp.route('/verification-attempts/suspicious', methods=['GET'])
@token_required
def get_suspicious_activity():
    """Get suspicious verification activity (admin only)"""
    from flask import g
    
    # Check if user is admin
    if g.current_user.role not in ['supermaster', 'master']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get query parameters
        hours = request.args.get('hours', 24, type=int)
        threshold = request.args.get('threshold', 10, type=int)
        
        # Get suspicious activity
        suspicious = VerificationAttempt.get_suspicious_activity(hours=hours, threshold=threshold)
        
        return jsonify({
            'suspicious_activity': suspicious,
            'parameters': {
                'hours': hours,
                'threshold': threshold
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Error fetching suspicious activity: {str(e)}')
        return jsonify({'error': 'Failed to fetch suspicious activity'}), 500


@security_bp.route('/verification-attempts/stats', methods=['GET'])
@token_required
def get_verification_stats():
    """Get verification attempt statistics (admin only)"""
    from flask import g
    from datetime import datetime, timedelta
    from sqlalchemy import func
    from src.database import db
    
    # Check if user is admin
    if g.current_user.role not in ['supermaster', 'master']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get query parameters
        hours = request.args.get('hours', 24, type=int)
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Total attempts
        total_attempts = VerificationAttempt.query.filter(
            VerificationAttempt.created_at >= cutoff_time
        ).count()
        
        # Successful attempts
        successful_attempts = VerificationAttempt.query.filter(
            VerificationAttempt.created_at >= cutoff_time,
            VerificationAttempt.success == True
        ).count()
        
        # Failed attempts
        failed_attempts = total_attempts - successful_attempts
        
        # Success rate
        success_rate = (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        # Most common failure reasons
        failure_reasons = db.session.query(
            VerificationAttempt.failure_reason,
            func.count(VerificationAttempt.id).label('count')
        ).filter(
            VerificationAttempt.created_at >= cutoff_time,
            VerificationAttempt.success == False,
            VerificationAttempt.failure_reason.isnot(None)
        ).group_by(
            VerificationAttempt.failure_reason
        ).order_by(
            func.count(VerificationAttempt.id).desc()
        ).limit(10).all()
        
        # Top IPs by attempts
        top_ips = db.session.query(
            VerificationAttempt.ip_address,
            func.count(VerificationAttempt.id).label('count')
        ).filter(
            VerificationAttempt.created_at >= cutoff_time,
            VerificationAttempt.ip_address.isnot(None)
        ).group_by(
            VerificationAttempt.ip_address
        ).order_by(
            func.count(VerificationAttempt.id).desc()
        ).limit(10).all()
        
        return jsonify({
            'stats': {
                'total_attempts': total_attempts,
                'successful_attempts': successful_attempts,
                'failed_attempts': failed_attempts,
                'success_rate': round(success_rate, 2)
            },
            'failure_reasons': [
                {'reason': r[0], 'count': r[1]} 
                for r in failure_reasons
            ],
            'top_ips': [
                {'ip': ip[0], 'attempts': ip[1]} 
                for ip in top_ips
            ],
            'period_hours': hours
        }), 200
        
    except Exception as e:
        logger.error(f'Error fetching verification stats: {str(e)}')
        return jsonify({'error': 'Failed to fetch statistics'}), 500


@security_bp.route('/verification-attempts/alert', methods=['POST'])
@token_required
def send_security_alert():
    """Manually trigger security alert email (admin only)"""
    from flask import g
    
    # Check if user is admin
    if g.current_user.role not in ['supermaster', 'master']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get suspicious activity
        suspicious = VerificationAttempt.get_suspicious_activity(hours=24, threshold=10)
        
        if not suspicious['emails'] and not suspicious['ips']:
            return jsonify({
                'message': 'No suspicious activity detected'
            }), 200
        
        # Send alert email to admin
        admin_email = g.user.email
        
        # Format alert message
        alert_message = "🚨 Security Alert: Suspicious Email Verification Activity\n\n"
        
        if suspicious['emails']:
            alert_message += "Suspicious Emails (10+ failures in 24h):\n"
            for item in suspicious['emails'][:10]:
                alert_message += f"  • {item['email']}: {item['failures']} failures\n"
            alert_message += "\n"
        
        if suspicious['ips']:
            alert_message += "Suspicious IPs (10+ failures in 24h):\n"
            for item in suspicious['ips'][:10]:
                alert_message += f"  • {item['ip']}: {item['failures']} failures\n"
        
        # Send email (you can implement this in EmailService)
        admin_email = g.current_user.email
        logger.warning(f'Security alert triggered by admin {admin_email}')
        logger.warning(alert_message)
        
        # TODO: Implement EmailService.send_security_alert(admin_email, alert_message)
        
        return jsonify({
            'message': 'Security alert logged',
            'suspicious_activity': suspicious
        }), 200
        
    except Exception as e:
        logger.error(f'Error sending security alert: {str(e)}')
        return jsonify({'error': 'Failed to send alert'}), 500


@security_bp.route('/verification-attempts/recent', methods=['GET'])
@token_required
def get_recent_attempts():
    """Get recent verification attempts (admin only)"""
    from flask import g
    
    # Check if user is admin
    if g.current_user.role not in ['supermaster', 'master']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        email = request.args.get('email')
        ip = request.args.get('ip')
        success = request.args.get('success')
        
        # Build query
        query = VerificationAttempt.query
        
        if email:
            query = query.filter(VerificationAttempt.email.like(f'%{email}%'))
        
        if ip:
            query = query.filter(VerificationAttempt.ip_address == ip)
        
        if success is not None:
            success_bool = success.lower() in ['true', '1', 'yes']
            query = query.filter(VerificationAttempt.success == success_bool)
        
        # Get attempts
        attempts = query.order_by(
            VerificationAttempt.created_at.desc()
        ).limit(limit).all()
        
        return jsonify({
            'attempts': [
                {
                    'id': a.id,
                    'email': a.email,
                    'code_entered': a.code_entered,
                    'success': a.success,
                    'ip_address': a.ip_address,
                    'user_agent': a.user_agent[:100] if a.user_agent else None,  # Truncate for display
                    'failure_reason': a.failure_reason,
                    'created_at': a.created_at.isoformat() if a.created_at else None
                }
                for a in attempts
            ],
            'count': len(attempts),
            'filters': {
                'email': email,
                'ip': ip,
                'success': success
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Error fetching recent attempts: {str(e)}')
        return jsonify({'error': 'Failed to fetch attempts'}), 500

