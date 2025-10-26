"""
Course Enrollment Model
"""
from datetime import datetime
from ..extensions import db


class CourseEnrollment(db.Model):
    """Course enrollment tracking"""
    __tablename__ = 'course_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    name = db.Column(db.String(255))
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Drip campaign tracking
    module_1_sent = db.Column(db.Boolean, default=False)
    module_1_sent_at = db.Column(db.DateTime)
    
    module_2_sent = db.Column(db.Boolean, default=False)
    module_2_sent_at = db.Column(db.DateTime)
    
    module_3_sent = db.Column(db.Boolean, default=False)
    module_3_sent_at = db.Column(db.DateTime)
    
    module_4_sent = db.Column(db.Boolean, default=False)
    module_4_sent_at = db.Column(db.DateTime)
    
    module_5_sent = db.Column(db.Boolean, default=False)
    module_5_sent_at = db.Column(db.DateTime)
    
    # Engagement tracking
    last_email_opened_at = db.Column(db.DateTime)
    unsubscribed = db.Column(db.Boolean, default=False)
    unsubscribed_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'enrolled_at': self.enrolled_at.isoformat() if self.enrolled_at else None,
            'modules_sent': {
                'module_1': self.module_1_sent,
                'module_2': self.module_2_sent,
                'module_3': self.module_3_sent,
                'module_4': self.module_4_sent,
                'module_5': self.module_5_sent
            },
            'unsubscribed': self.unsubscribed
        }

