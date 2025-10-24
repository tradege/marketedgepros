from datetime import datetime
from src.database import db, TimestampMixin
from sqlalchemy import Index

class Notification(db.Model, TimestampMixin):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # withdrawal, commission, kyc, system, payment, challenge
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    data = db.Column(db.JSON, nullable=True)  # Additional data
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))
    
    # Indexes
    __table_args__ = (
        Index('idx_notifications_user_id', 'user_id'),
        Index('idx_notifications_type', 'type'),
        Index('idx_notifications_is_read', 'is_read'),
        Index('idx_notifications_created_at', 'created_at'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'data': self.data,
            'priority': self.priority,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()
            db.session.commit()
    
    def soft_delete(self):
        """Soft delete notification"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications for user"""
        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False,
            is_deleted=False
        ).count()
    
    @staticmethod
    def get_user_notifications(user_id, filters=None, page=1, per_page=50):
        """Get notifications for user with optional filters"""
        query = Notification.query.filter_by(user_id=user_id, is_deleted=False)
        
        if filters:
            if filters.get('type'):
                query = query.filter_by(type=filters['type'])
            if filters.get('is_read') is not None:
                query = query.filter_by(is_read=filters['is_read'])
            if filters.get('priority'):
                query = query.filter_by(priority=filters['priority'])
        
        query = query.order_by(Notification.created_at.desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'notifications': [n.to_dict() for n in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }


class NotificationPreference(db.Model, TimestampMixin):
    __tablename__ = 'notification_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    # In-App Notifications
    in_app_withdrawal = db.Column(db.Boolean, default=True)
    in_app_commission = db.Column(db.Boolean, default=True)
    in_app_kyc = db.Column(db.Boolean, default=True)
    in_app_system = db.Column(db.Boolean, default=True)
    in_app_payment = db.Column(db.Boolean, default=True)
    in_app_challenge = db.Column(db.Boolean, default=True)
    
    # Email Notifications
    email_withdrawal = db.Column(db.Boolean, default=True)
    email_commission = db.Column(db.Boolean, default=True)
    email_kyc = db.Column(db.Boolean, default=True)
    email_system = db.Column(db.Boolean, default=False)
    email_payment = db.Column(db.Boolean, default=True)
    email_challenge = db.Column(db.Boolean, default=True)
    
    # General Settings
    email_enabled = db.Column(db.Boolean, default=True)
    email_frequency = db.Column(db.String(20), default='instant')  # instant, daily, weekly
    
    # Relationships
    user = db.relationship('User', backref=db.backref('notification_preferences', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'in_app': {
                'withdrawal': self.in_app_withdrawal,
                'commission': self.in_app_commission,
                'kyc': self.in_app_kyc,
                'system': self.in_app_system,
                'payment': self.in_app_payment,
                'challenge': self.in_app_challenge,
            },
            'email': {
                'withdrawal': self.email_withdrawal,
                'commission': self.email_commission,
                'kyc': self.email_kyc,
                'system': self.email_system,
                'payment': self.email_payment,
                'challenge': self.email_challenge,
            },
            'settings': {
                'email_enabled': self.email_enabled,
                'email_frequency': self.email_frequency,
            }
        }
    
    @staticmethod
    def get_or_create(user_id):
        """Get or create preferences for user"""
        prefs = NotificationPreference.query.filter_by(user_id=user_id).first()
        if not prefs:
            prefs = NotificationPreference(user_id=user_id)
            db.session.add(prefs)
            db.session.commit()
        return prefs
    
    def should_send_in_app(self, notification_type):
        """Check if in-app notification should be sent for this type"""
        attr = f'in_app_{notification_type}'
        return getattr(self, attr, True)
    
    def should_send_email(self, notification_type):
        """Check if email notification should be sent for this type"""
        if not self.email_enabled:
            return False
        attr = f'email_{notification_type}'
        return getattr(self, attr, True)


class EmailQueue(db.Model, TimestampMixin):
    __tablename__ = 'email_queue'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    to_email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    html_body = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed
    attempts = db.Column(db.Integer, default=0)
    max_attempts = db.Column(db.Integer, default=3)
    error_message = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('email_queue', lazy='dynamic'))
    
    # Indexes
    __table_args__ = (
        Index('idx_email_queue_status', 'status'),
        Index('idx_email_queue_created_at', 'created_at'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'to_email': self.to_email,
            'subject': self.subject,
            'status': self.status,
            'attempts': self.attempts,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def mark_as_sent(self):
        """Mark email as sent"""
        self.status = 'sent'
        self.sent_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_failed(self, error_message):
        """Mark email as failed"""
        self.status = 'failed'
        self.attempts += 1
        self.error_message = error_message
        db.session.commit()

