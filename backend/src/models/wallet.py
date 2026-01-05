"""
Wallet model for managing user balances
"""
from datetime import datetime
from src.database import db, TimestampMixin


class Wallet(db.Model, TimestampMixin):
    """User wallet for managing balances"""
    
    __tablename__ = 'wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Balance types
    main_balance = db.Column(db.Numeric(12, 2), default=0.0, nullable=False)  # Main trading balance
    commission_balance = db.Column(db.Numeric(12, 2), default=0.0, nullable=False)  # Agent commissions
    bonus_balance = db.Column(db.Numeric(12, 2), default=0.0, nullable=False)  # Bonus/promo balance
    
    # Total available for withdrawal
    @property
    def total_balance(self):
        return float(self.main_balance) + float(self.commission_balance)
    
    # Metadata
    last_transaction_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('wallet', uselist=False))
    
    # Indexes
    __table_args__ = (
        db.Index('ix_wallet_user_id', 'user_id'),
    )
    
    def add_funds(self, amount, balance_type='main', description=None, reference_type=None, reference_id=None, created_by=None):
        """Add funds to wallet with race condition protection"""
        if amount <= 0:
            raise ValueError('Amount must be positive')
        
        if balance_type not in ['main', 'commission', 'bonus']:
            raise ValueError('Invalid balance type')
        
        # Use SELECT FOR UPDATE to lock the row
        wallet = db.session.query(Wallet).with_for_update().filter_by(id=self.id).first()
        
        # Get current balance
        if balance_type == 'main':
            balance_before = float(wallet.main_balance)
            wallet.main_balance = float(wallet.main_balance) + amount
            balance_after = float(wallet.main_balance)
        elif balance_type == 'commission':
            balance_before = float(wallet.commission_balance)
            wallet.commission_balance = float(wallet.commission_balance) + amount
            balance_after = float(wallet.commission_balance)
        else:  # bonus
            balance_before = float(wallet.bonus_balance)
            wallet.bonus_balance = float(wallet.bonus_balance) + amount
            balance_after = float(wallet.bonus_balance)
        
        wallet.last_transaction_at = datetime.utcnow()
        
        # Create transaction record
        transaction = Transaction(
            wallet_id=self.id,
            type='deposit',
            amount=amount,
            balance_type=balance_type,
            balance_before=balance_before,
            balance_after=balance_after,
            reference_type=reference_type,
            reference_id=reference_id,
            description=description,
            created_by=created_by
        )
        db.session.add(transaction)
        
        return transaction
    
    def deduct_funds(self, amount, balance_type='main', description=None, reference_type=None, reference_id=None, created_by=None):
        """Deduct funds from wallet with race condition protection and validation"""
        if amount <= 0:
            raise ValueError('Amount must be positive')
        
        if balance_type not in ['main', 'commission', 'bonus']:
            raise ValueError('Invalid balance type')
        
        # Use SELECT FOR UPDATE to lock the row
        wallet = db.session.query(Wallet).with_for_update().filter_by(id=self.id).first()
        
        # Get current balance and validate
        if balance_type == 'main':
            balance_before = float(wallet.main_balance)
            if balance_before < amount:
                raise ValueError(f'Insufficient main balance. Available: {balance_before}, Required: {amount}')
            wallet.main_balance = float(wallet.main_balance) - amount
            balance_after = float(wallet.main_balance)
        elif balance_type == 'commission':
            balance_before = float(wallet.commission_balance)
            if balance_before < amount:
                raise ValueError(f'Insufficient commission balance. Available: {balance_before}, Required: {amount}')
            wallet.commission_balance = float(wallet.commission_balance) - amount
            balance_after = float(wallet.commission_balance)
        else:  # bonus
            balance_before = float(wallet.bonus_balance)
            if balance_before < amount:
                raise ValueError(f'Insufficient bonus balance. Available: {balance_before}, Required: {amount}')
            wallet.bonus_balance = float(wallet.bonus_balance) - amount
            balance_after = float(wallet.bonus_balance)
        
        wallet.last_transaction_at = datetime.utcnow()
        
        # Create transaction record
        transaction = Transaction(
            wallet_id=self.id,
            type='withdrawal',
            amount=amount,
            balance_type=balance_type,
            balance_before=balance_before,
            balance_after=balance_after,
            reference_type=reference_type,
            reference_id=reference_id,
            description=description,
            created_by=created_by
        )
        db.session.add(transaction)
        
        return transaction
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'main_balance': float(self.main_balance),
            'commission_balance': float(self.commission_balance),
            'bonus_balance': float(self.bonus_balance),
            'total_balance': self.total_balance,
            'is_active': self.is_active,
            'last_transaction_at': self.last_transaction_at.isoformat() if self.last_transaction_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Transaction(db.Model, TimestampMixin):
    """Transaction history for wallet operations"""
    
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    
    # Transaction details
    type = db.Column(db.String(50), nullable=False)  # deposit, withdrawal, commission, bonus, adjustment
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    balance_type = db.Column(db.String(20), default='main', nullable=False)  # main, commission, bonus
    
    # Balance before/after
    balance_before = db.Column(db.Numeric(12, 2), nullable=False)
    balance_after = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Reference
    reference_type = db.Column(db.String(50))  # withdrawal, commission, challenge, etc.
    reference_id = db.Column(db.Integer)
    
    # Metadata
    description = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    wallet = db.relationship('Wallet', backref='transactions')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    # Indexes
    __table_args__ = (
        db.Index('ix_transaction_wallet_id', 'wallet_id'),
        db.Index('ix_transaction_type', 'type'),
        db.Index('ix_transaction_created_at', 'created_at'),
    )
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'type': self.type,
            'amount': float(self.amount),
            'balance_type': self.balance_type,
            'balance_before': float(self.balance_before),
            'balance_after': float(self.balance_after),
            'reference_type': self.reference_type,
            'reference_id': self.reference_id,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

