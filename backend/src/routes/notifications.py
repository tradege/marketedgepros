from flask import Blueprint, request, jsonify
from src.middleware.auth import jwt_required, admin_required, get_current_user
from src.services.notification_service import NotificationService
from src.models.notification import NotificationPreference
from src.database import db

notifications_bp = Blueprint('notifications', __name__)

# ==================== USER ENDPOINTS ====================

@notifications_bp.route('/', methods=['GET'])
@jwt_required
def get_notifications():
    """Get user notifications with optional filters"""
    try:
        current_user = get_current_user()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        notification_type = request.args.get('type')
        is_read = request.args.get('is_read')
        priority = request.args.get('priority')
        
        # Build filters
        filters = {}
        if notification_type:
            filters['type'] = notification_type
        if is_read is not None:
            filters['is_read'] = is_read.lower() == 'true'
        if priority:
            filters['priority'] = priority
        
        # Get notifications
        result = NotificationService.get_user_notifications(
            user_id=current_user.id,
            filters=filters,
            page=page,
            per_page=per_page
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/unread-count', methods=['GET'])
@jwt_required
def get_unread_count():
    """Get count of unread notifications"""
    try:
        current_user = get_current_user()
        count = NotificationService.get_unread_count(current_user.id)
        
        return jsonify({'count': count}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required
def mark_as_read(notification_id):
    """Mark notification as read"""
    try:
        current_user = get_current_user()
        notification = NotificationService.mark_as_read(notification_id, current_user.id)
        
        return jsonify({
            'message': 'Notification marked as read',
            'notification': notification.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/read-all', methods=['POST'])
@jwt_required
def mark_all_as_read():
    """Mark all notifications as read"""
    try:
        current_user = get_current_user()
        count = NotificationService.mark_all_as_read(current_user.id)
        
        return jsonify({
            'message': f'{count} notifications marked as read',
            'count': count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required
def delete_notification(notification_id):
    """Delete notification"""
    try:
        current_user = get_current_user()
        notification = NotificationService.delete_notification(notification_id, current_user.id)
        
        return jsonify({
            'message': 'Notification deleted',
            'notification': notification.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== PREFERENCE ENDPOINTS ====================

@notifications_bp.route('/preferences', methods=['GET'])
@jwt_required
def get_preferences():
    """Get user notification preferences"""
    try:
        current_user = get_current_user()
        prefs = NotificationPreference.get_or_create(current_user.id)
        
        return jsonify(prefs.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/preferences', methods=['PUT'])
@jwt_required
def update_preferences():
    """Update user notification preferences"""
    try:
        current_user = get_current_user()
        data = request.get_json()
        
        prefs = NotificationPreference.get_or_create(current_user.id)
        
        # Update in-app preferences
        if 'in_app' in data:
            for key, value in data['in_app'].items():
                attr = f'in_app_{key}'
                if hasattr(prefs, attr):
                    setattr(prefs, attr, value)
        
        # Update email preferences
        if 'email' in data:
            for key, value in data['email'].items():
                attr = f'email_{key}'
                if hasattr(prefs, attr):
                    setattr(prefs, attr, value)
        
        # Update settings
        if 'settings' in data:
            if 'email_enabled' in data['settings']:
                prefs.email_enabled = data['settings']['email_enabled']
            if 'email_frequency' in data['settings']:
                prefs.email_frequency = data['settings']['email_frequency']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': prefs.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== ADMIN ENDPOINTS ====================

@notifications_bp.route('/admin/send', methods=['POST'])
@admin_required
def admin_send_notification():
    """Send notification to specific user(s)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_ids', 'type', 'title', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        user_ids = data['user_ids']
        notification_type = data['type']
        title = data['title']
        message = data['message']
        priority = data.get('priority', 'normal')
        notification_data = data.get('data')
        
        # Create notifications for each user
        count = 0
        for user_id in user_ids:
            notification = NotificationService.create_notification(
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                data=notification_data,
                priority=priority
            )
            if notification:
                count += 1
        
        return jsonify({
            'message': f'{count} notifications sent',
            'count': count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/admin/broadcast', methods=['POST'])
@admin_required
def admin_broadcast_notification():
    """Broadcast notification to all users or users with specific role"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['type', 'title', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        notification_type = data['type']
        title = data['title']
        message = data['message']
        priority = data.get('priority', 'normal')
        notification_data = data.get('data')
        role = data.get('role')  # Optional: broadcast to specific role
        
        # Broadcast
        count = NotificationService.broadcast_notification(
            notification_type=notification_type,
            title=title,
            message=message,
            data=notification_data,
            priority=priority,
            role=role
        )
        
        return jsonify({
            'message': f'Notification broadcast to {count} users',
            'count': count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/admin/stats', methods=['GET'])
@admin_required
def admin_get_stats():
    """Get notification statistics"""
    try:
        from src.models.notification import Notification
        from sqlalchemy import func
        
        # Total notifications
        total = Notification.query.filter_by(is_deleted=False).count()
        
        # Unread notifications
        unread = Notification.query.filter_by(is_read=False, is_deleted=False).count()
        
        # Notifications by type
        by_type = db.session.query(
            Notification.type,
            func.count(Notification.id).label('count')
        ).filter_by(is_deleted=False).group_by(Notification.type).all()
        
        # Notifications by priority
        by_priority = db.session.query(
            Notification.priority,
            func.count(Notification.id).label('count')
        ).filter_by(is_deleted=False).group_by(Notification.priority).all()
        
        # Recent notifications (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent = Notification.query.filter(
            Notification.created_at >= yesterday,
            Notification.is_deleted == False
        ).count()
        
        return jsonify({
            'total': total,
            'unread': unread,
            'read': total - unread,
            'recent_24h': recent,
            'by_type': {t: c for t, c in by_type},
            'by_priority': {p: c for p, c in by_priority}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

