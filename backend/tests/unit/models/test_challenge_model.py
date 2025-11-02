"""
Unit tests for Challenge model
"""
import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from src.models import Challenge

@pytest.mark.unit
@pytest.mark.model
class TestChallengeModel:
    """Test Challenge model functionality"""
    
    def test_create_challenge(self, session, trader_user, trading_program):
        """Test creating a challenge"""
        challenge = Challenge(
            user_id=trader_user.id,
            program_id=trading_program.id,
            status='pending',
            initial_balance=Decimal('10000.00'),
            current_balance=Decimal('10000.00')
        )
        session.add(challenge)
        session.commit()
        
        assert challenge.id is not None
        assert challenge.user_id == trader_user.id
        assert challenge.program_id == trading_program.id
        assert challenge.status == 'pending'
        assert challenge.initial_balance == Decimal('10000.00')
    
    def test_challenge_status_transitions(self, session, challenge):
        """Test challenge status transitions"""
        # Pending -> Active
        challenge.status = 'active'
        challenge.start_date = datetime.utcnow()
        session.commit()
        
        assert challenge.status == 'active'
        assert challenge.start_date is not None
        
        # Active -> Passed
        challenge.status = 'passed'
        challenge.passed_at = datetime.utcnow()
        session.commit()
        
        assert challenge.status == 'passed'
        assert challenge.passed_at is not None
    
    def test_challenge_calculate_progress(self, session, challenge):
        """Test calculating challenge progress"""
        # Set initial balance and profit
        challenge.initial_balance = Decimal('10000.00')
        challenge.total_profit = Decimal('500.00')  # 5% profit
        session.commit()
        
        # Program has 10% target
        progress = challenge.calculate_progress()
        
        # 500 / 1000 * 100 = 50%
        assert progress == 50.0
    
    def test_challenge_is_target_reached(self, session, challenge):
        """Test checking if target is reached"""
        challenge.initial_balance = Decimal('10000.00')
        challenge.total_profit = Decimal('500.00')  # 5% profit
        session.commit()
        
        # Target is 10%, we have 5%
        assert challenge.is_target_reached() is False
        
        # Reach target
        challenge.total_profit = Decimal('1000.00')  # 10% profit
        session.commit()
        
        assert challenge.is_target_reached() is True
    
    def test_challenge_is_max_loss_exceeded(self, session, challenge):
        """Test checking if max loss is exceeded"""
        challenge.initial_balance = Decimal('10000.00')
        challenge.total_loss = Decimal('-500.00')  # 5% loss
        session.commit()
        
        # Max loss is 10%, we have 5%
        assert challenge.is_max_loss_exceeded() is False
        
        # Exceed max loss
        challenge.total_loss = Decimal('-1000.00')  # 10% loss
        session.commit()
        
        assert challenge.is_max_loss_exceeded() is True
    
    def test_challenge_payment_approval(self, session, trader_user, trading_program, admin_user):
        """Test challenge payment approval workflow"""
        challenge = Challenge(
            user_id=trader_user.id,
            program_id=trading_program.id,
            payment_type='cash',
            approval_status='pending'
        )
        session.add(challenge)
        session.commit()
        
        assert challenge.approval_status == 'pending'
        
        # Approve
        challenge.approval_status = 'approved'
        challenge.approved_by = admin_user.id
        challenge.approved_at = datetime.utcnow()
        session.commit()
        
        assert challenge.approval_status == 'approved'
        assert challenge.approved_by == admin_user.id
    
    def test_challenge_payment_rejection(self, session, trader_user, trading_program, admin_user):
        """Test challenge payment rejection"""
        challenge = Challenge(
            user_id=trader_user.id,
            program_id=trading_program.id,
            payment_type='cash',
            approval_status='pending'
        )
        session.add(challenge)
        session.commit()
        
        # Reject
        challenge.approval_status = 'rejected'
        challenge.approved_by = admin_user.id
        challenge.rejection_reason = 'Invalid payment proof'
        session.commit()
        
        assert challenge.approval_status == 'rejected'
        assert challenge.rejection_reason == 'Invalid payment proof'
    
    def test_challenge_phase_progression(self, session, challenge):
        """Test challenge phase progression"""
        challenge.current_phase = 1
        challenge.total_phases = 2
        session.commit()
        
        assert challenge.current_phase == 1
        
        # Progress to phase 2
        challenge.current_phase = 2
        session.commit()
        
        assert challenge.current_phase == 2
        assert challenge.current_phase == challenge.total_phases
    
    def test_challenge_balance_updates(self, session, challenge):
        """Test challenge balance updates"""
        challenge.initial_balance = Decimal('10000.00')
        challenge.current_balance = Decimal('10000.00')
        session.commit()
        
        # Win a trade
        challenge.current_balance = Decimal('10500.00')
        challenge.total_profit = Decimal('500.00')
        session.commit()
        
        assert challenge.current_balance == Decimal('10500.00')
        assert challenge.total_profit == Decimal('500.00')
    
    def test_challenge_max_drawdown(self, session, challenge):
        """Test challenge max drawdown tracking"""
        challenge.initial_balance = Decimal('10000.00')
        challenge.current_balance = Decimal('9500.00')
        challenge.max_drawdown = Decimal('500.00')
        session.commit()
        
        assert challenge.max_drawdown == Decimal('500.00')
    
    def test_challenge_relationships(self, session, challenge, trader_user, trading_program):
        """Test challenge relationships"""
        assert challenge.user is not None
        assert challenge.user.id == trader_user.id
        assert challenge.program is not None
        assert challenge.program.id == trading_program.id
    
    def test_challenge_with_addons(self, session, trader_user, trading_program):
        """Test challenge with add-ons"""
        challenge = Challenge(
            user_id=trader_user.id,
            program_id=trading_program.id,
            addons=[
                {'name': 'Extra Leverage', 'price': 50.0},
                {'name': 'Extended Time', 'price': 30.0}
            ]
        )
        session.add(challenge)
        session.commit()
        
        assert len(challenge.addons) == 2
        assert challenge.addons[0]['name'] == 'Extra Leverage'
    
    def test_challenge_account_number(self, session, challenge):
        """Test challenge account number assignment"""
        challenge.account_number = 'ACC123456'
        session.commit()
        
        assert challenge.account_number == 'ACC123456'
    
    def test_challenge_dates(self, session, challenge):
        """Test challenge date tracking"""
        now = datetime.utcnow()
        challenge.start_date = now
        challenge.end_date = now + timedelta(days=30)
        session.commit()
        
        assert challenge.start_date is not None
        assert challenge.end_date is not None
        assert challenge.end_date > challenge.start_date
