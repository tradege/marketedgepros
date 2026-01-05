"""
Agent model for referral/affiliate system
"""
from src.database import db, TimestampMixin
import secrets
import string


class Agent(db.Model, TimestampMixin):
    """Agent/Affiliate model for referral system"""
    
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Commission settings
    commission_rate = db.Column(db.Numeric(5, 2), nullable=False, default=10.0)  # Percentage
    
    # Financial tracking
    total_earned = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)
    total_withdrawn = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)
    pending_balance = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)
    
    # Statistics
    referral_count = db.Column(db.Integer, nullable=False, default=0)
    active_referrals = db.Column(db.Integer, nullable=False, default=0)
    total_sales = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)
    
    # Status
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('agent_profile', uselist=False))
    referrals = db.relationship('Referral', backref='agent', lazy='dynamic')
    commissions = db.relationship('Commission', backref='agent', lazy='dynamic')
    
    @staticmethod
    def generate_agent_code(length=8):
        """Generate unique agent code"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    def get_available_balance(self):
        """Get available balance for withdrawal"""
        return float(self.pending_balance)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'agent_code': self.agent_code,
            'user_id': self.user_id,
            'commission_rate': float(self.commission_rate),
            'total_earned': float(self.total_earned),
            'total_withdrawn': float(self.total_withdrawn),
            'pending_balance': float(self.pending_balance),
            'referral_count': self.referral_count,
            'active_referrals': self.active_referrals,
            'total_sales': float(self.total_sales),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

