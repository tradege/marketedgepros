"""
Commission System Database Models
MarketEdgePros - Prop Trading Firm Platform
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Extended User model with commission tracking fields
    Add these columns to existing User table
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    
    # Existing fields (reference only)
    # email, password_hash, role, etc.
    
    # NEW: Commission fields
    commission_rate = Column(Float, default=20.0, nullable=False)  # Percentage (e.g., 20 = 20%)
    paid_customers_count = Column(Integer, default=0, nullable=False)  # Count of customers who paid
    commission_balance = Column(Float, default=0.0, nullable=False)  # Available for withdrawal
    pending_commission = Column(Float, default=0.0, nullable=False)  # Waiting for 10 customers threshold
    last_withdrawal_date = Column(DateTime, nullable=True)  # Last withdrawal request date
    can_withdraw = Column(Boolean, default=False, nullable=False)  # Eligible to withdraw
    
    # Relationships
    commissions_earned = relationship('Commission', foreign_keys='Commission.affiliate_id', back_populates='affiliate')
    commissions_generated = relationship('Commission', foreign_keys='Commission.customer_id', back_populates='customer')
    payment_methods = relationship('PaymentMethod', back_populates='user', cascade='all, delete-orphan')
    withdrawals = relationship('Withdrawal', foreign_keys='Withdrawal.user_id', back_populates='user')
    approved_withdrawals = relationship('Withdrawal', foreign_keys='Withdrawal.approved_by', back_populates='approver')


class Commission(Base):
    """
    Commission records tracking affiliate earnings
    """
    __tablename__ = 'commissions'
    
    id = Column(Integer, primary_key=True)
    affiliate_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    order_id = Column(String(100), nullable=False)  # Reference to payment/order
    
    amount = Column(Float, nullable=False)  # Commission amount in USD
    commission_rate = Column(Float, nullable=False)  # Rate at time of commission (for history)
    
    status = Column(String(20), default='pending', nullable=False)  # pending, released, paid
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    released_at = Column(DateTime, nullable=True)  # When moved from pending to balance
    paid_at = Column(DateTime, nullable=True)  # When paid to affiliate
    
    # Relationships
    affiliate = relationship('User', foreign_keys=[affiliate_id], back_populates='commissions_earned')
    customer = relationship('User', foreign_keys=[customer_id], back_populates='commissions_generated')
    
    # Indexes
    __table_args__ = (
        Index('idx_affiliate_status', 'affiliate_id', 'status'),
        Index('idx_customer', 'customer_id'),
        Index('idx_order', 'order_id'),
        Index('idx_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Commission(id={self.id}, affiliate_id={self.affiliate_id}, amount=${self.amount}, status={self.status})>"


class PaymentMethod(Base):
    """
    User payment methods for withdrawals
    """
    __tablename__ = 'payment_methods'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    method_type = Column(String(20), nullable=False)  # bank, paypal, crypto, wise
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Bank transfer fields
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(100), nullable=True)
    branch_number = Column(String(20), nullable=True)
    account_holder_name = Column(String(100), nullable=True)
    
    # PayPal fields
    paypal_email = Column(String(100), nullable=True)
    
    # Cryptocurrency fields
    crypto_address = Column(String(200), nullable=True)
    crypto_network = Column(String(20), nullable=True)  # TRC20, ERC20
    
    # Wise fields
    wise_email = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='payment_methods')
    
    # Indexes
    __table_args__ = (
        Index('idx_user_active', 'user_id', 'is_active'),
    )
    
    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'method_type': self.method_type,
            'is_active': self.is_active,
            'bank_name': self.bank_name,
            'account_number': self.account_number[-4:] if self.account_number else None,  # Last 4 digits only
            'account_holder_name': self.account_holder_name,
            'paypal_email': self.paypal_email,
            'crypto_address': self.crypto_address[:10] + '...' + self.crypto_address[-10:] if self.crypto_address else None,
            'crypto_network': self.crypto_network,
            'wise_email': self.wise_email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, user_id={self.user_id}, type={self.method_type})>"


class Withdrawal(Base):
    """
    Withdrawal requests from affiliates
    """
    __tablename__ = 'withdrawals'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    amount = Column(Float, nullable=False)  # Withdrawal amount in USD
    method_type = Column(String(20), nullable=False)  # Payment method type
    payment_details = Column(JSON, nullable=False)  # Snapshot of payment details
    
    status = Column(String(20), default='pending', nullable=False)  # pending, approved, paid, rejected
    notes = Column(Text, nullable=True)  # Admin notes or rejection reason
    
    requested_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    
    approved_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    # Relationships
    user = relationship('User', foreign_keys=[user_id], back_populates='withdrawals')
    approver = relationship('User', foreign_keys=[approved_by], back_populates='approved_withdrawals')
    
    # Indexes
    __table_args__ = (
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_status', 'status'),
        Index('idx_requested_at', 'requested_at'),
    )
    
    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'method_type': self.method_type,
            'payment_details': self.payment_details,
            'status': self.status,
            'notes': self.notes,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'rejected_at': self.rejected_at.isoformat() if self.rejected_at else None,
        }
    
    def __repr__(self):
        return f"<Withdrawal(id={self.id}, user_id={self.user_id}, amount=${self.amount}, status={self.status})>"

