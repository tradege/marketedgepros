"""
Wallet service for managing user balances and transactions
"""
from datetime import datetime
from decimal import Decimal
from src.database import db
from src.models.wallet import Wallet, Transaction
from src.models.user import User


class WalletService:
    """Service for wallet operations"""
    
    @staticmethod
    def get_or_create_wallet(user_id):
        """Get or create wallet for user"""
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        
        if not wallet:
            wallet = Wallet(user_id=user_id)
            db.session.add(wallet)
            db.session.commit()
        
        return wallet
    
    @staticmethod
    def get_balance(user_id, balance_type='main'):
        """Get user balance"""
        wallet = WalletService.get_or_create_wallet(user_id)
        
        if balance_type == 'main':
            return float(wallet.main_balance)
        elif balance_type == 'commission':
            return float(wallet.commission_balance)
        elif balance_type == 'bonus':
            return float(wallet.bonus_balance)
        elif balance_type == 'total':
            return wallet.total_balance
        
        return 0.0
    
    @staticmethod
    def add_funds(user_id, amount, balance_type='main', description=None, 
                  reference_type=None, reference_id=None, created_by=None):
        """Add funds to wallet"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        wallet = WalletService.get_or_create_wallet(user_id)
        
        # Get current balance
        if balance_type == 'main':
            balance_before = float(wallet.main_balance)
            wallet.main_balance = Decimal(str(balance_before + amount))
        elif balance_type == 'commission':
            balance_before = float(wallet.commission_balance)
            wallet.commission_balance = Decimal(str(balance_before + amount))
        elif balance_type == 'bonus':
            balance_before = float(wallet.bonus_balance)
            wallet.bonus_balance = Decimal(str(balance_before + amount))
        else:
            raise ValueError(f"Invalid balance type: {balance_type}")
        
        balance_after = balance_before + amount
        
        # Create transaction record
        transaction = Transaction(
            wallet_id=wallet.id,
            type='deposit',
            amount=Decimal(str(amount)),
            balance_type=balance_type,
            balance_before=Decimal(str(balance_before)),
            balance_after=Decimal(str(balance_after)),
            reference_type=reference_type,
            reference_id=reference_id,
            description=description or f"Added {amount} to {balance_type} balance",
            created_by=created_by
        )
        
        wallet.last_transaction_at = datetime.utcnow()
        
        db.session.add(transaction)
        db.session.commit()
        
        return wallet, transaction
    
    @staticmethod
    def deduct_funds(user_id, amount, balance_type='main', description=None,
                     reference_type=None, reference_id=None, created_by=None):
        """Deduct funds from wallet"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        wallet = WalletService.get_or_create_wallet(user_id)
        
        # Get current balance
        if balance_type == 'main':
            balance_before = float(wallet.main_balance)
            if balance_before < amount:
                raise ValueError("Insufficient main balance")
            wallet.main_balance = Decimal(str(balance_before - amount))
        elif balance_type == 'commission':
            balance_before = float(wallet.commission_balance)
            if balance_before < amount:
                raise ValueError("Insufficient commission balance")
            wallet.commission_balance = Decimal(str(balance_before - amount))
        elif balance_type == 'bonus':
            balance_before = float(wallet.bonus_balance)
            if balance_before < amount:
                raise ValueError("Insufficient bonus balance")
            wallet.bonus_balance = Decimal(str(balance_before - amount))
        else:
            raise ValueError(f"Invalid balance type: {balance_type}")
        
        balance_after = balance_before - amount
        
        # Create transaction record
        transaction = Transaction(
            wallet_id=wallet.id,
            type='withdrawal',
            amount=Decimal(str(amount)),
            balance_type=balance_type,
            balance_before=Decimal(str(balance_before)),
            balance_after=Decimal(str(balance_after)),
            reference_type=reference_type,
            reference_id=reference_id,
            description=description or f"Deducted {amount} from {balance_type} balance",
            created_by=created_by
        )
        
        wallet.last_transaction_at = datetime.utcnow()
        
        db.session.add(transaction)
        db.session.commit()
        
        return wallet, transaction
    
    @staticmethod
    def transfer_funds(from_user_id, to_user_id, amount, balance_type='main',
                      description=None, reference_type=None, reference_id=None):
        """Transfer funds between wallets"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Deduct from sender
        WalletService.deduct_funds(
            from_user_id, amount, balance_type,
            description=f"Transfer to user {to_user_id}: {description or ''}",
            reference_type=reference_type,
            reference_id=reference_id
        )
        
        # Add to recipient
        WalletService.add_funds(
            to_user_id, amount, balance_type,
            description=f"Transfer from user {from_user_id}: {description or ''}",
            reference_type=reference_type,
            reference_id=reference_id
        )
        
        return True
    
    @staticmethod
    def get_transaction_history(user_id, limit=50, offset=0, balance_type=None):
        """Get transaction history for user"""
        wallet = WalletService.get_or_create_wallet(user_id)
        
        query = Transaction.query.filter_by(wallet_id=wallet.id)
        
        if balance_type:
            query = query.filter_by(balance_type=balance_type)
        
        transactions = query.order_by(Transaction.created_at.desc())\
                           .limit(limit)\
                           .offset(offset)\
                           .all()
        
        return transactions
    
    @staticmethod
    def adjust_balance(user_id, amount, balance_type='main', description=None, created_by=None):
        """Manual balance adjustment (admin only)"""
        wallet = WalletService.get_or_create_wallet(user_id)
        
        # Get current balance
        if balance_type == 'main':
            balance_before = float(wallet.main_balance)
            wallet.main_balance = Decimal(str(balance_before + amount))
        elif balance_type == 'commission':
            balance_before = float(wallet.commission_balance)
            wallet.commission_balance = Decimal(str(balance_before + amount))
        elif balance_type == 'bonus':
            balance_before = float(wallet.bonus_balance)
            wallet.bonus_balance = Decimal(str(balance_before + amount))
        else:
            raise ValueError(f"Invalid balance type: {balance_type}")
        
        balance_after = balance_before + amount
        
        # Create transaction record
        transaction = Transaction(
            wallet_id=wallet.id,
            type='adjustment',
            amount=Decimal(str(abs(amount))),
            balance_type=balance_type,
            balance_before=Decimal(str(balance_before)),
            balance_after=Decimal(str(balance_after)),
            description=description or f"Manual adjustment: {amount}",
            created_by=created_by
        )
        
        wallet.last_transaction_at = datetime.utcnow()
        
        db.session.add(transaction)
        db.session.commit()
        
        return wallet, transaction

