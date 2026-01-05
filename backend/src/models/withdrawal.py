"""
Withdrawal model for agent payouts
"""
from src.database import db, TimestampMixin


class Withdrawal(db.Model, TimestampMixin):
    """Withdrawal request model"""
    
    __tablename__ = 'withdrawals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=True)
    
    # Amount
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    fee = db.Column(db.Numeric(12, 2), default=0.0, nullable=False)
    net_amount = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Payment details
    payment_method = db.Column(db.String(50), nullable=False)  # bank_transfer, paypal, crypto
    withdrawal_method = db.Column(db.String(50))  # Alias for payment_method
    payment_details = db.Column(db.JSON)  # Account number, PayPal email, wallet address, etc.
    account_details = db.Column(db.JSON)  # Alias for payment_details
    
    # Status
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, approved, processing, completed, rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    processed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Transaction details
    transaction_id = db.Column(db.String(100))
    rejection_reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='withdrawals')
    agent = db.relationship('Agent', backref='withdrawals')
    challenge = db.relationship('Challenge', backref='withdrawals')
    approver = db.relationship('User', foreign_keys=[approved_by])
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'amount': float(self.amount),
            'fee': float(self.fee),
            'net_amount': float(self.net_amount),
            'payment_method': self.payment_method,
            'status': self.status,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'transaction_id': self.transaction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

