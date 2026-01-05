"""
Payment Approval Request model for cash/free payment approvals
"""
from datetime import datetime
from src.database import db


class PaymentApprovalRequest(db.Model):
    """Payment approval requests for cash/free payments"""
    
    __tablename__ = 'payment_approval_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id', ondelete='CASCADE'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id', ondelete='CASCADE'))
    
    # Request details
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    requested_for = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # The trader/user
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)  # cash, free
    
    # Status
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, approved, rejected
    
    # Approval/Rejection
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    admin_notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    challenge = db.relationship('Challenge', foreign_keys=[challenge_id])
    payment = db.relationship('Payment', foreign_keys=[payment_id])
    requester = db.relationship('User', foreign_keys=[requested_by])
    trader = db.relationship('User', foreign_keys=[requested_for])
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    
    def __repr__(self):
        return f'<PaymentApprovalRequest {self.id} - {self.payment_type} - {self.status}>'
    
    def to_dict(self):
        """Convert approval request to dictionary"""
        return {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'payment_id': self.payment_id,
            'requested_by': self.requested_by,
            'requested_for': self.requested_for,
            'amount': float(self.amount) if self.amount else None,
            'payment_type': self.payment_type,
            'status': self.status,
            'reviewed_by': self.reviewed_by,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'rejection_reason': self.rejection_reason,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

