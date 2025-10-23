from datetime import datetime
from src.database import db

class Payment(db.Model):
    """Payment transactions"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Payment details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_method = db.Column(db.String(50))  # stripe, paypal, crypto
    payment_type = db.Column(db.String(20), default='credit_card', nullable=False)  # credit_card, cash, free
    
    # Transaction details
    transaction_id = db.Column(db.String(255), unique=True)
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed, refunded
    
    # Approval system (for cash/free payments)
    approval_status = db.Column(db.String(20), default='approved', nullable=False)  # pending, approved, rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    admin_notes = db.Column(db.Text)
    
    # Purpose
    purpose = db.Column(db.String(100))  # challenge_purchase, withdrawal
    reference_id = db.Column(db.Integer)  # Challenge ID or Withdrawal ID
    
    # Provider details
    provider_response = db.Column(db.Text)  # JSON response from payment provider
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship("User", foreign_keys=[user_id], backref="payments")
    approver = db.relationship("User", foreign_keys=[approved_by])

    # Add indexes for performance
    __table_args__ = (db.Index("ix_payment_user_id", "user_id"), db.Index("ix_payment_status", "status"))

    # Note: payment_id in Challenge is a string (Stripe payment intent ID), not a foreign key
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': float(self.amount) if self.amount else None,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'payment_type': self.payment_type,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'approval_status': self.approval_status,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'rejection_reason': self.rejection_reason,
            'purpose': self.purpose,
            'reference_id': self.reference_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }

