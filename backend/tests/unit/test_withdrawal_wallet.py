"""
Unit tests for Withdrawal & Wallet System
"""
import pytest
from decimal import Decimal
from datetime import datetime
from src.models import Withdrawal, Wallet

@pytest.mark.unit
class TestWithdrawal:
    """Test withdrawal functionality"""
    
    def test_create_withdrawal(self, session, agent_user):
        """Test creating a withdrawal request"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        withdrawal = Withdrawal(
            agent_id=agent.id,
            amount=Decimal('1000.00'),
            fee=Decimal('50.00'),
            net_amount=Decimal('950.00'),
            payment_method='bank_transfer',
            status='pending'
        )
        session.add(withdrawal)
        session.commit()
        
        assert withdrawal.id is not None
        assert withdrawal.amount == Decimal('1000.00')
        assert withdrawal.net_amount == Decimal('950.00')
    
    def test_withdrawal_status_transitions(self, session, agent_user):
        """Test withdrawal status transitions"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        withdrawal = Withdrawal(
            agent_id=agent.id,
            amount=Decimal('500.00'),
            fee=Decimal('25.00'),
            net_amount=Decimal('475.00'),
            payment_method='paypal',
            status='pending'
        )
        session.add(withdrawal)
        session.commit()
        
        assert withdrawal.status == 'pending'
        
        # Approve
        withdrawal.status = 'approved'
        withdrawal.approved_at = datetime.utcnow()
        session.commit()
        
        assert withdrawal.status == 'approved'
        assert withdrawal.approved_at is not None
        
        # Process
        withdrawal.status = 'processing'
        withdrawal.processed_at = datetime.utcnow()
        session.commit()
        
        assert withdrawal.status == 'processing'
        
        # Complete
        withdrawal.status = 'completed'
        withdrawal.completed_at = datetime.utcnow()
        withdrawal.transaction_id = 'TXN123456'
        session.commit()
        
        assert withdrawal.status == 'completed'
        assert withdrawal.transaction_id is not None
    
    def test_withdrawal_rejection(self, session, agent_user):
        """Test withdrawal rejection"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        withdrawal = Withdrawal(
            agent_id=agent.id,
            amount=Decimal('2000.00'),
            fee=Decimal('100.00'),
            net_amount=Decimal('1900.00'),
            payment_method='bank_transfer',
            status='pending'
        )
        session.add(withdrawal)
        session.commit()
        
        # Reject
        withdrawal.status = 'rejected'
        withdrawal.rejection_reason = 'Insufficient balance'
        session.commit()
        
        assert withdrawal.status == 'rejected'
        assert withdrawal.rejection_reason is not None
    
    def test_withdrawal_payment_methods(self, session, agent_user):
        """Test different payment methods"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        methods = ['bank_transfer', 'paypal', 'crypto']
        
        for method in methods:
            withdrawal = Withdrawal(
                agent_id=agent.id,
                amount=Decimal('100.00'),
                fee=Decimal('5.00'),
                net_amount=Decimal('95.00'),
                payment_method=method
            )
            session.add(withdrawal)
        
        session.commit()
        
        withdrawals = Withdrawal.query.filter_by(agent_id=agent.id).all()
        assert len(withdrawals) >= 3
    
    def test_withdrawal_payment_details(self, session, agent_user):
        """Test storing payment details"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        withdrawal = Withdrawal(
            agent_id=agent.id,
            amount=Decimal('500.00'),
            fee=Decimal('25.00'),
            net_amount=Decimal('475.00'),
            payment_method='bank_transfer',
            payment_details={
                'bank_name': 'Test Bank',
                'account_number': '1234567890',
                'routing_number': '987654321'
            }
        )
        session.add(withdrawal)
        session.commit()
        
        assert withdrawal.payment_details['bank_name'] == 'Test Bank'
    
    def test_withdrawal_to_dict(self, session, agent_user):
        """Test withdrawal serialization"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        withdrawal = Withdrawal(
            agent_id=agent.id,
            amount=Decimal('1000.00'),
            fee=Decimal('50.00'),
            net_amount=Decimal('950.00'),
            payment_method='paypal',
            status='completed',
            transaction_id='TXN789'
        )
        session.add(withdrawal)
        session.commit()
        
        w_dict = withdrawal.to_dict()
        
        assert w_dict['amount'] == 1000.00
        assert w_dict['net_amount'] == 950.00
        assert w_dict['status'] == 'completed'
    
    def test_withdrawal_fee_calculation(self, session, agent_user):
        """Test withdrawal fee calculation"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        amount = Decimal('1000.00')
        fee = Decimal('50.00')  # 5% fee
        net_amount = amount - fee
        
        withdrawal = Withdrawal(
            agent_id=agent.id,
            amount=amount,
            fee=fee,
            net_amount=net_amount,
            payment_method='bank_transfer'
        )
        session.add(withdrawal)
        session.commit()
        
        assert withdrawal.net_amount == Decimal('950.00')
    
    def test_withdrawal_decimal_precision(self, session, agent_user):
        """Test withdrawal decimal precision"""
        from src.models import Agent
        
        agent = Agent.query.filter_by(user_id=agent_user.id).first()
        
        withdrawal = Withdrawal(
            agent_id=agent.id,
            amount=Decimal('123.45'),
            fee=Decimal('6.17'),
            net_amount=Decimal('117.28'),
            payment_method='paypal'
        )
        session.add(withdrawal)
        session.commit()
        
        assert withdrawal.amount == Decimal('123.45')
        assert withdrawal.fee == Decimal('6.17')
        assert withdrawal.net_amount == Decimal('117.28')

@pytest.mark.unit
class TestWallet:
    """Test wallet functionality"""
    
    def test_create_wallet(self, session, trader_user):
        """Test creating a wallet"""
        wallet = Wallet(
            user_id=trader_user.id,
            main_balance=Decimal('1000.00'),
            commission_balance=Decimal('500.00'),
            bonus_balance=Decimal('100.00')
        )
        session.add(wallet)
        session.commit()
        
        assert wallet.id is not None
        assert wallet.user_id == trader_user.id
        assert wallet.main_balance == Decimal('1000.00')
    
    def test_wallet_total_balance(self, session, trader_user):
        """Test wallet total balance calculation"""
        wallet = Wallet(
            user_id=trader_user.id,
            main_balance=Decimal('1000.00'),
            commission_balance=Decimal('500.00'),
            bonus_balance=Decimal('100.00')
        )
        session.add(wallet)
        session.commit()
        
        # Total = main + commission (bonus not included)
        assert wallet.total_balance == 1500.00
    
    def test_wallet_one_per_user(self, session, trader_user):
        """Test that each user can have only one wallet"""
        wallet1 = Wallet(
            user_id=trader_user.id,
            main_balance=Decimal('100.00')
        )
        session.add(wallet1)
        session.commit()
        
        # Try to create another wallet for same user
        wallet2 = Wallet(
            user_id=trader_user.id,
            main_balance=Decimal('200.00')
        )
        session.add(wallet2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            session.commit()
    
    def test_wallet_balance_types(self, session, trader_user):
        """Test different balance types"""
        wallet = Wallet(
            user_id=trader_user.id,
            main_balance=Decimal('1000.00'),
            commission_balance=Decimal('500.00'),
            bonus_balance=Decimal('100.00')
        )
        session.add(wallet)
        session.commit()
        
        assert wallet.main_balance == Decimal('1000.00')
        assert wallet.commission_balance == Decimal('500.00')
        assert wallet.bonus_balance == Decimal('100.00')
    
    def test_wallet_is_active(self, session, trader_user):
        """Test wallet active status"""
        wallet = Wallet(
            user_id=trader_user.id,
            is_active=True
        )
        session.add(wallet)
        session.commit()
        
        assert wallet.is_active is True
        
        # Deactivate
        wallet.is_active = False
        session.commit()
        
        assert wallet.is_active is False
    
    def test_wallet_last_transaction_tracking(self, session, trader_user):
        """Test last transaction timestamp"""
        wallet = Wallet(
            user_id=trader_user.id,
            main_balance=Decimal('1000.00')
        )
        session.add(wallet)
        session.commit()
        
        # Update last transaction
        wallet.last_transaction_at = datetime.utcnow()
        session.commit()
        
        assert wallet.last_transaction_at is not None
    
    def test_wallet_decimal_precision(self, session, trader_user):
        """Test wallet decimal precision"""
        wallet = Wallet(
            user_id=trader_user.id,
            main_balance=Decimal('123.45'),
            commission_balance=Decimal('67.89'),
            bonus_balance=Decimal('12.34')
        )
        session.add(wallet)
        session.commit()
        
        assert wallet.main_balance == Decimal('123.45')
        assert wallet.commission_balance == Decimal('67.89')
        assert wallet.bonus_balance == Decimal('12.34')
    
    def test_wallet_relationship_with_user(self, session, trader_user):
        """Test wallet relationship with user"""
        wallet = Wallet(
            user_id=trader_user.id,
            main_balance=Decimal('1000.00')
        )
        session.add(wallet)
        session.commit()
        
        assert wallet.user is not None
        assert wallet.user.id == trader_user.id
        assert trader_user.wallet is not None
        assert trader_user.wallet.id == wallet.id
