"""
Commission model for tracking agent earnings
"""
from decimal import Decimal
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
        db.Index('ix_commission_agent_status', 'agent_id', 'status'),  # Composite index
        db.Index('ix_commission_created_at', 'created_at'),  # For date queries
    )
    
    @staticmethod
    def calculate_commission(sale_amount, commission_rate):
        """
        Calculate commission amount from sale amount and rate
        
        Args:
            sale_amount: Sale amount (Decimal, float, or int)
            commission_rate: Commission rate percentage (Decimal, float, or int)
        
        Returns:
            Decimal: Calculated commission amount
        
        Raises:
            ValueError: If commission_rate is invalid
        """
        if not sale_amount or not commission_rate:
            return Decimal('0')
        
        # Convert to Decimal for precise calculations
        sale_decimal = Decimal(str(sale_amount))
        rate_decimal = Decimal(str(commission_rate))
        
        # Validate rate
        if rate_decimal < 0 or rate_decimal > 100:
            raise ValueError('Commission rate must be between 0 and 100')
        
        # Check for zero to avoid division issues
        if rate_decimal == 0:
            return Decimal('0')
        
        # Calculate: (sale_amount * commission_rate) / 100
        commission = (sale_decimal * rate_decimal) / Decimal('100')
        
        # Round to 2 decimal places for currency
        return commission.quantize(Decimal('0.01'))
    
    def validate_commission(self):
        """
        Validate that commission amount matches calculation
        
        Returns:
            bool: True if commission is valid, False otherwise
        """
        expected = self.calculate_commission(self.sale_amount, self.commission_rate)
        actual = Decimal(str(self.commission_amount))
        
        # Allow small differences (0.01) for rounding
        difference = abs(expected - actual)
        return difference <= Decimal('0.01')
    
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

