"""
Commission model for tracking agent earnings
"""
from src.database import db, TimestampMixin


class Commission(db.Model, TimestampMixin):
    """Commission tracking model"""
    
    __tablename__ = 'commissions'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    referral_id = db.Column(db.Integer, db.ForeignKey('referrals.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    
    # Commission details
    sale_amount = db.Column(db.Numeric(12, 2), nullable=False)
    commission_rate = db.Column(db.Numeric(5, 2), nullable=False)
    commission_amount = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, approved, paid
    approved_at = db.Column(db.DateTime)
    paid_at = db.Column(db.DateTime)
    
    # Payment details
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    
    # Relationships
    referral = db.relationship('Referral', backref='commissions')
    challenge = db.relationship('Challenge', backref='commission_records')
    
    # Add indexes for performance
    __table_args__ = (
        db.Index('ix_commission_agent_id', 'agent_id'),
        db.Index('ix_commission_status', 'status'),
    )
    
    @staticmethod
    def calculate_commission(sale_amount, commission_rate):
        """Calculate commission amount from sale amount and rate"""
        if not sale_amount or not commission_rate:
            return 0
        if commission_rate < 0 or commission_rate > 100:
            raise ValueError('Commission rate must be between 0 and 100')
        return (sale_amount * commission_rate / 100)
    
    def validate_commission(self):
        """Validate that commission amount matches calculation"""
        expected = self.calculate_commission(float(self.sale_amount), float(self.commission_rate))
        actual = float(self.commission_amount)
        # Allow small floating point differences (0.01)
        return abs(expected - actual) < 0.01
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'referral_id': self.referral_id,
            'challenge_id': self.challenge_id,
            'sale_amount': float(self.sale_amount),
            'commission_rate': float(self.commission_rate),
            'commission_amount': float(self.commission_amount),
            'status': self.status,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

