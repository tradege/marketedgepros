from datetime import datetime
from src.database import db
from src.models.notification import Notification, NotificationPreference
from src.services.email_service import EmailService

class NotificationService:
    """Service for managing notifications"""
    
    @staticmethod
    def create_notification(user_id, notification_type, title, message, data=None, priority='normal', send_email=True):
        """
        Create a new notification
        
        Args:
            user_id: ID of the user to notify
            notification_type: Type of notification (withdrawal, commission, kyc, etc.)
            title: Notification title
            message: Notification message
            data: Additional data (dict)
            priority: Priority level (low, normal, high, urgent)
            send_email: Whether to also send email notification
        
        Returns:
            Notification object
        """
        # Get user preferences
        prefs = NotificationPreference.get_or_create(user_id)
        
        # Check if in-app notification should be sent
        if not prefs.should_send_in_app(notification_type):
            return None
        
        # Create notification
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            data=data,
            priority=priority
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Send email if enabled
        if send_email and prefs.should_send_email(notification_type):
            EmailService.send_notification_email(notification)
        
        return notification
    
    @staticmethod
    def get_user_notifications(user_id, filters=None, page=1, per_page=50):
        """Get notifications for a user"""
        return Notification.get_user_notifications(user_id, filters, page, per_page)
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications"""
        return Notification.get_unread_count(user_id)
    
    @staticmethod
    def mark_as_read(notification_id, user_id):
        """Mark notification as read"""
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id,
            is_deleted=False
        ).first()
        
        if not notification:
            raise ValueError('Notification not found')
        
        notification.mark_as_read()
        return notification
    
    @staticmethod
    def mark_all_as_read(user_id):
        """Mark all notifications as read for a user"""
        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False,
            is_deleted=False
        ).all()
        
        for notification in notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
        
        db.session.commit()
        return len(notifications)
    
    @staticmethod
    def delete_notification(notification_id, user_id):
        """Soft delete a notification"""
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if not notification:
            raise ValueError('Notification not found')
        
        notification.soft_delete()
        return notification
    
    @staticmethod
    def broadcast_notification(notification_type, title, message, data=None, priority='normal', user_ids=None, role=None):
        """
        Broadcast notification to multiple users
        
        Args:
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            data: Additional data
            priority: Priority level
            user_ids: List of specific user IDs (optional)
            role: Send to all users with this role (optional)
        
        Returns:
            Number of notifications created
        """
        from src.models.user import User
        
        # Get target users
        if user_ids:
            users = User.query.filter(User.id.in_(user_ids)).all()
        elif role:
            users = User.query.filter_by(role=role).all()
        else:
            users = User.query.all()
        
        count = 0
        for user in users:
            notification = NotificationService.create_notification(
                user_id=user.id,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data,
                priority=priority
            )
            if notification:
                count += 1
        
        return count
    
    # Specific notification creators for common events
    
    @staticmethod
    def notify_withdrawal_submitted(user_id, withdrawal_id, amount):
        """Notify user that withdrawal was submitted"""
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type='withdrawal',
            title='Withdrawal Request Submitted',
            message=f'Your withdrawal request for ${amount:.2f} has been submitted and is pending approval.',
            data={'withdrawal_id': withdrawal_id, 'amount': amount},
            priority='normal'
        )
    
    @staticmethod
    def notify_withdrawal_approved(user_id, withdrawal_id, amount):
        """Notify user that withdrawal was approved"""
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type='withdrawal',
            title='Withdrawal Approved',
            message=f'Your withdrawal request for ${amount:.2f} has been approved and is being processed.',
            data={'withdrawal_id': withdrawal_id, 'amount': amount},
            priority='high'
        )
    
    @staticmethod
    def notify_withdrawal_rejected(user_id, withdrawal_id, amount, reason):
        """Notify user that withdrawal was rejected"""
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type='withdrawal',
            title='Withdrawal Rejected',
            message=f'Your withdrawal request for ${amount:.2f} has been rejected. Reason: {reason}',
            data={'withdrawal_id': withdrawal_id, 'amount': amount, 'reason': reason},
            priority='high'
        )
    
    @staticmethod
    def notify_withdrawal_completed(user_id, withdrawal_id, amount, transaction_id):
        """Notify user that withdrawal was completed"""
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type='withdrawal',
            title='Withdrawal Completed',
            message=f'Your withdrawal of ${amount:.2f} has been completed. Transaction ID: {transaction_id}',
            data={'withdrawal_id': withdrawal_id, 'amount': amount, 'transaction_id': transaction_id},
            priority='high'
        )
    
    @staticmethod
    def notify_commission_earned(user_id, amount, trader_name):
        """Notify agent that commission was earned"""
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type='commission',
            title='Commission Earned',
            message=f'You earned ${amount:.2f} commission from {trader_name}',
            data={'amount': amount, 'trader_name': trader_name},
            priority='normal'
        )
    
    @staticmethod
    def notify_kyc_submitted(user_id):
        """Notify user that KYC was submitted"""
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type='kyc',
            title='KYC Submitted',
            message='Your KYC documents have been submitted for review.',
            priority='normal'
        )
    
    @staticmethod
    def notify_kyc_approved(user_id):
        """Notify user that KYC was approved"""
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type='kyc',
            title='KYC Approved',
            message='Your KYC verification has been approved. You can now access all features.',
            priority='high'
        )
    
    @staticmethod
    def notify_kyc_rejected(user_id, reason):
        """Notify user that KYC was rejected"""
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type='kyc',
            title='KYC Rejected',
            message=f'Your KYC verification was rejected. Reason: {reason}',
            data={'reason': reason},
            priority='high'
        )
    
    @staticmethod
    def notify_welcome(user_id, user_name):
        """Send welcome notification to new user"""
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type='system',
            title='Welcome to MarketEdgePros',
            message=f'Welcome {user_name}! Get started by completing your profile and exploring our programs.',
            priority='normal'
        )

