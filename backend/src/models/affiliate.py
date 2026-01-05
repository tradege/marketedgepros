"""
Affiliate Program Models
Handles affiliate links, referrals, commissions, and payouts
"""
from datetime import datetime
from src.database import db

class AffiliateLink(db.Model):
    """Affiliate referral links"""
    __tablename__ = 'affiliate_links'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Link details
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100))  # Custom name for tracking
    
    # Tracking
    clicks = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Numeric(10, 2), default=0)
    total_commission = db.Column(db.Numeric(10, 2), default=0)
    
    # Settings
    commission_rate = db.Column(db.Numeric(5, 2), default=10.00)  # Percentage
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_click_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='affiliate_links')
    referrals = db.relationship('AffiliateReferral', backref='affiliate_link', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'clicks': self.clicks,
            'conversions': self.conversions,
            'total_revenue': float(self.total_revenue) if self.total_revenue else 0,
            'total_commission': float(self.total_commission) if self.total_commission else 0,
            'commission_rate': float(self.commission_rate) if self.commission_rate else 0,
            'conversion_rate': round((self.conversions / self.clicks * 100) if self.clicks > 0 else 0, 2),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_click_at': self.last_click_at.isoformat() if self.last_click_at else None,
            'url': f'https://marketedgepros.com/?ref={self.code}'
        }


class AffiliateReferral(db.Model):
    """Affiliate referrals - tracks who was referred by whom"""
    __tablename__ = 'affiliate_referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    affiliate_link_id = db.Column(db.Integer, db.ForeignKey('affiliate_links.id'), nullable=False)
    affiliate_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Referral details
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    landing_page = db.Column(db.String(500))
    
    # Conversion tracking
    status = db.Column(db.String(20), default='pending')  # pending, converted, cancelled
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    purchase_amount = db.Column(db.Numeric(10, 2))
    commission_amount = db.Column(db.Numeric(10, 2))
    
    # Timestamps
    click_date = db.Column(db.DateTime, default=datetime.utcnow)
    conversion_date = db.Column(db.DateTime)
    
    # Relationships
    affiliate_user = db.relationship('User', foreign_keys=[affiliate_user_id], backref='affiliate_referrals_made')
    referred_user = db.relationship('User', foreign_keys=[referred_user_id], backref='affiliate_referral_source')
    
    def to_dict(self):
        return {
            'id': self.id,
            'affiliate_link_id': self.affiliate_link_id,
            'referred_user': {
                'id': self.referred_user.id,
                'email': self.referred_user.email,
                'name': f'{self.referred_user.first_name} {self.referred_user.last_name}'
            } if self.referred_user else None,
            'status': self.status,
            'purchase_amount': float(self.purchase_amount) if self.purchase_amount else 0,
            'commission_amount': float(self.commission_amount) if self.commission_amount else 0,
            'click_date': self.click_date.isoformat() if self.click_date else None,
            'conversion_date': self.conversion_date.isoformat() if self.conversion_date else None
        }


class AffiliateCommission(db.Model):
    """Affiliate commissions - tracks earnings"""
    __tablename__ = 'affiliate_commissions'
    
    id = db.Column(db.Integer, primary_key=True)
    affiliate_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referral_id = db.Column(db.Integer, db.ForeignKey('affiliate_referrals.id'))
    
    # Commission details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(20), default='one_time')  # one_time, recurring, lifetime
    status = db.Column(db.String(20), default='pending')  # pending, approved, paid, cancelled
    
    # Description
    description = db.Column(db.String(500))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    paid_at = db.Column(db.DateTime)
    
    # Payout reference
    payout_id = db.Column(db.Integer, db.ForeignKey('affiliate_payouts.id'))
    
    # Relationships
    affiliate_user = db.relationship('User', backref='affiliate_commissions')
    referral = db.relationship('AffiliateReferral', backref='commissions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount) if self.amount else 0,
            'type': self.type,
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'payout_id': self.payout_id
        }


class AffiliatePayout(db.Model):
    """Affiliate payouts - tracks payment requests and disbursements"""
    __tablename__ = 'affiliate_payouts'
    
    id = db.Column(db.Integer, primary_key=True)
    affiliate_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Payout details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(50))  # paypal, bank_transfer, crypto, etc.
    payment_details = db.Column(db.JSON)  # Email, account number, wallet address, etc.
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    
    # Admin notes
    notes = db.Column(db.Text)
    transaction_id = db.Column(db.String(100))
    
    # Timestamps
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    affiliate_user = db.relationship('User', backref='affiliate_payouts')
    commissions = db.relationship('AffiliateCommission', backref='payout')
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount) if self.amount else 0,
            'method': self.method,
            'status': self.status,
            'notes': self.notes,
            'transaction_id': self.transaction_id,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'commission_count': len(self.commissions) if self.commissions else 0
        }


class AffiliateSettings(db.Model):
    """Global affiliate program settings"""
    __tablename__ = 'affiliate_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Commission rates
    default_commission_rate = db.Column(db.Numeric(5, 2), default=10.00)
    min_payout_amount = db.Column(db.Numeric(10, 2), default=50.00)
    
    # Cookie settings
    cookie_duration_days = db.Column(db.Integer, default=30)
    
    # Program status
    is_active = db.Column(db.Boolean, default=True)
    auto_approve_affiliates = db.Column(db.Boolean, default=False)
    auto_approve_commissions = db.Column(db.Boolean, default=False)
    
    # Terms
    terms_and_conditions = db.Column(db.Text)
    
    # Timestamps
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'default_commission_rate': float(self.default_commission_rate) if self.default_commission_rate else 0,
            'min_payout_amount': float(self.min_payout_amount) if self.min_payout_amount else 0,
            'cookie_duration_days': self.cookie_duration_days,
            'is_active': self.is_active,
            'auto_approve_affiliates': self.auto_approve_affiliates,
            'auto_approve_commissions': self.auto_approve_commissions
        }

