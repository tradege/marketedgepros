"""
Payment Method model for withdrawal payments
"""
from src.database import db, TimestampMixin

class PaymentMethod(db.Model, TimestampMixin):
    """User payment methods for commission withdrawals"""
    
    __tablename__ = 'payment_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Method type and status
    method_type = db.Column(db.String(20), nullable=False)  # bank, paypal, crypto, wise
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Bank transfer fields
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(100))
    branch_number = db.Column(db.String(20))
    account_holder_name = db.Column(db.String(100))
    
    # PayPal fields
    paypal_email = db.Column(db.String(100))
    
    # Cryptocurrency fields
    crypto_address = db.Column(db.String(200))
    crypto_network = db.Column(db.String(20))  # TRC20, ERC20, BEP20
    
    # Wise fields
    wise_email = db.Column(db.String(100))
    
    # Relationships
    user = db.relationship('User', backref='payment_methods')
    
    def to_dict(self, mask_sensitive=True):
        """Convert to dictionary with optional sensitive data masking"""
        data = {
            'id': self.id,
            'method_type': self.method_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if self.method_type == 'bank':
            data.update({
                'bank_name': self.bank_name,
                'account_holder_name': self.account_holder_name,
                'account_number': self.account_number[-4:] if mask_sensitive and self.account_number else self.account_number,
                'branch_number': self.branch_number
            })
        elif self.method_type == 'paypal':
            data['paypal_email'] = self.paypal_email
        elif self.method_type == 'crypto':
            if mask_sensitive and self.crypto_address:
                data['crypto_address'] = self.crypto_address[:10] + '...'+self.crypto_address[-10:]
            else:
                data['crypto_address'] = self.crypto_address
            data['crypto_network'] = self.crypto_network
        elif self.method_type == 'wise':
            data['wise_email'] = self.wise_email
        
        return data
    
    def to_json_snapshot(self):
        """Create a JSON snapshot for withdrawal records (unmasked)"""
        return self.to_dict(mask_sensitive=False)
