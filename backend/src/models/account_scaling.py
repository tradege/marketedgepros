"""
Account Scaling Model
Tracks trader progression through account size tiers
"""
from datetime import datetime
from src.database import db, TimestampMixin


class AccountScaling(db.Model, TimestampMixin):
    """
    Tracks a trader's progression through account size tiers.
    When a trader consistently meets profit targets, they can scale up to larger accounts.
    """
    
    __tablename__ = 'account_scaling'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Current tier information
    current_tier = db.Column(db.Integer, default=1, nullable=False)  # 1, 2, 3, 4, 5
    current_account_size = db.Column(db.Numeric(12, 2), nullable=False)  # e.g., 10000, 25000, 50000
    
    # Next tier information
    next_tier = db.Column(db.Integer)  # null if at max tier
    next_account_size = db.Column(db.Numeric(12, 2))  # null if at max tier
    
    # Progress tracking
    total_profit = db.Column(db.Numeric(12, 2), default=0, nullable=False)  # Total profit earned at current tier
    target_profit = db.Column(db.Numeric(12, 2), nullable=False)  # Profit needed to scale up
    progress_percentage = db.Column(db.Numeric(5, 2), default=0)  # 0-100
    
    # Scaling history
    times_scaled = db.Column(db.Integer, default=0, nullable=False)  # How many times user has scaled up
    last_scaled_at = db.Column(db.DateTime)  # When they last scaled up
    
    # Eligibility
    is_eligible_for_scaling = db.Column(db.Boolean, default=False, nullable=False)
    eligibility_checked_at = db.Column(db.DateTime)
    
    # Status
    status = db.Column(db.String(20), default='active', nullable=False)  # active, paused, completed (max tier reached)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('scaling_plan', uselist=False))
    
    # Indexes
    __table_args__ = (
        db.Index('ix_account_scaling_user_id', 'user_id'),
        db.Index('ix_account_scaling_status', 'status'),
        db.Index('ix_account_scaling_eligible', 'is_eligible_for_scaling'),
    )
    
    def __repr__(self):
        return f'<AccountScaling User:{self.user_id} Tier:{self.current_tier} Progress:{self.progress_percentage}%>'
    
    def calculate_progress(self):
        """Calculate current progress percentage towards next tier"""
        if self.target_profit == 0:
            return 0
        
        progress = (self.total_profit / self.target_profit) * 100
        return min(progress, 100)
    
    def update_progress(self, new_profit):
        """Update total profit and recalculate progress"""
        self.total_profit += new_profit
        self.progress_percentage = self.calculate_progress()
        
        # Check if eligible for scaling
        if self.progress_percentage >= 100 and self.next_tier is not None:
            self.is_eligible_for_scaling = True
            self.eligibility_checked_at = datetime.utcnow()
        
        return self.progress_percentage
    
    def scale_up(self, new_account_size, new_target_profit):
        """
        Scale user up to next tier
        Resets progress and updates tier information
        """
        self.current_tier = self.next_tier
        self.current_account_size = new_account_size
        self.total_profit = 0
        self.progress_percentage = 0
        self.target_profit = new_target_profit
        
        # Update next tier (or set to None if max tier reached)
        if self.current_tier >= 5:  # Assuming 5 tiers max
            self.next_tier = None
            self.next_account_size = None
            self.status = 'completed'
        else:
            self.next_tier = self.current_tier + 1
            # next_account_size will be set by the service
        
        self.times_scaled += 1
        self.last_scaled_at = datetime.utcnow()
        self.is_eligible_for_scaling = False
        
        return True
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'current_tier': self.current_tier,
            'current_account_size': float(self.current_account_size),
            'next_tier': self.next_tier,
            'next_account_size': float(self.next_account_size) if self.next_account_size else None,
            'total_profit': float(self.total_profit),
            'target_profit': float(self.target_profit),
            'progress_percentage': float(self.progress_percentage),
            'times_scaled': self.times_scaled,
            'last_scaled_at': self.last_scaled_at.isoformat() if self.last_scaled_at else None,
            'is_eligible_for_scaling': self.is_eligible_for_scaling,
            'eligibility_checked_at': self.eligibility_checked_at.isoformat() if self.eligibility_checked_at else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ScalingTier(db.Model, TimestampMixin):
    """
    Defines the scaling tiers and requirements
    Can be customized per tenant
    """
    
    __tablename__ = 'scaling_tiers'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    
    tier_number = db.Column(db.Integer, nullable=False)  # 1, 2, 3, 4, 5
    account_size = db.Column(db.Numeric(12, 2), nullable=False)  # e.g., 10000, 25000, 50000
    profit_target = db.Column(db.Numeric(12, 2), nullable=False)  # Profit needed to reach this tier
    
    # Requirements
    minimum_trading_days = db.Column(db.Integer, default=0)  # Minimum days of trading required
    minimum_trades = db.Column(db.Integer, default=0)  # Minimum number of trades required
    
    # Benefits
    profit_split = db.Column(db.Numeric(5, 2))  # Profit split at this tier (optional, can inherit from program)
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    tenant = db.relationship('Tenant', backref='scaling_tiers')
    
    # Indexes
    __table_args__ = (
        db.Index('ix_scaling_tier_tenant_tier', 'tenant_id', 'tier_number'),
        db.UniqueConstraint('tenant_id', 'tier_number', name='uq_tenant_tier'),
    )
    
    def __repr__(self):
        return f'<ScalingTier {self.tier_number}: ${self.account_size}>'
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'tier_number': self.tier_number,
            'account_size': float(self.account_size),
            'profit_target': float(self.profit_target),
            'minimum_trading_days': self.minimum_trading_days,
            'minimum_trades': self.minimum_trades,
            'profit_split': float(self.profit_split) if self.profit_split else None,
            'is_active': self.is_active
        }
