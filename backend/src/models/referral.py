"""
Referral model for tracking referred users
"""
from src.database import db, TimestampMixin


class Referral(db.Model, TimestampMixin):
    """Referral tracking model"""
    
    __tablename__ = 'referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    referred_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Tracking
    referral_code = db.Column(db.String(50), nullable=False, index=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    
    # Status
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, active, inactive
    first_purchase_at = db.Column(db.DateTime)
    total_purchases = db.Column(db.Integer, default=0, nullable=False)
    total_spent = db.Column(db.Numeric(12, 2), default=0.0, nullable=False)
    
    # Relationships
    referred_user = db.relationship('User', foreign_keys=[referred_user_id], backref='referral_info')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'referred_user_id': self.referred_user_id,
            'referral_code': self.referral_code,
            'status': self.status,
            'first_purchase_at': self.first_purchase_at.isoformat() if self.first_purchase_at else None,
            'total_purchases': self.total_purchases,
            'total_spent': float(self.total_spent),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

