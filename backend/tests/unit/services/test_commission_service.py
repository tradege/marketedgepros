"""
Unit tests for Commission Service
Tests commission calculation, approval, payment, and statistics
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal
from datetime import datetime
from src.services.commission_service import CommissionService
from src.models import Commission, Agent, Referral, Challenge, User, TradingProgram, Tenant


@pytest.fixture
def mock_tenant(session):
    """Create a mock tenant"""
    tenant = Tenant(
        name='Test Tenant',
        subdomain=f'test_{__import__('uuid').uuid4().hex[:8]}'
    )
    session.add(tenant)
    session.flush()
    return tenant


@pytest.fixture
def mock_user(session):
    """Create a mock user"""
    user = User(
        email='buyer@example.com',
        first_name='Test',
        last_name='Buyer'
    )
    user.set_password('password123')
    session.add(user)
    session.flush()
    return user


@pytest.fixture
def mock_agent_user(session):
    """Create a mock agent user"""
    user = User(
        email='agent@example.com',
        first_name='Agent',
        last_name='User'
    )
    user.set_password('password123')
    session.add(user)
    session.flush()
    return user


@pytest.fixture
def mock_agent(session, mock_agent_user):
    """Create a mock agent"""
    agent = Agent(
        agent_code='TEST_AGENT_001',
        user_id=mock_agent_user.id,
        commission_rate=Decimal('10.00'),
        is_active=True,
        total_sales=Decimal('0'),
        pending_balance=Decimal('0'),
        total_earned=Decimal('0'),
        total_withdrawn=Decimal('0')
    )
    session.add(agent)
    session.flush()
    return agent


@pytest.fixture
def mock_referral(session, mock_agent, mock_user):
    """Create a mock referral"""
    referral = Referral(
        agent_id=mock_agent.id,
        referred_user_id=mock_user.id,
        referral_code='TEST_REF_001',
        status='active',
        total_purchases=0,
        total_spent=Decimal('0')
    )
    session.add(referral)
    session.flush()
    return referral


@pytest.fixture
def mock_program(session, mock_tenant):
    """Create a mock trading program"""
    program = TradingProgram(
        name='Test Program',
        type='one_phase',
        account_size=10000.00,
        price=100.00,
        tenant_id=mock_tenant.id
    )
    session.add(program)
    session.flush()
    return program


@pytest.fixture
def mock_challenge(session, mock_user, mock_program):
    """Create a mock challenge"""
    challenge = Challenge(
        user_id=mock_user.id,
        program_id=mock_program.id,
        status='active',
        payment_status='paid'
    )
    session.add(challenge)
    session.flush()
    return challenge


class TestCommissionCalculation:
    """Test commission calculation and creation"""
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_calculate_commission_success(self, mock_notify, session, mock_challenge, mock_agent, mock_referral):
        """Test successful commission calculation"""
        # Arrange
        sale_amount = Decimal('100.00')
        
        # Act
        commission = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            sale_amount
        )
        
        # Assert
        assert commission is not None
        assert commission.agent_id == mock_agent.id
        assert commission.referral_id == mock_referral.id
        assert commission.challenge_id == mock_challenge.id
        assert commission.sale_amount == sale_amount
        assert commission.commission_rate == Decimal('10.00')
        assert commission.commission_amount == Decimal('10.00')  # 10% of 100
        assert commission.status == 'pending'
        
        # Verify agent stats updated
        session.refresh(mock_agent)
        assert mock_agent.total_sales == Decimal('100.00')
        assert mock_agent.pending_balance == Decimal('10.00')
        
        # Verify referral stats updated
        session.refresh(mock_referral)
        assert mock_referral.total_purchases == 1
        assert mock_referral.total_spent == Decimal('100.00')
        
        # Verify notification sent
        mock_notify.assert_called_once()
    
    def test_calculate_commission_challenge_not_found(self, session):
        """Test commission calculation with non-existent challenge"""
        # Act
        commission = CommissionService.calculate_and_create_commission(
            999999,  # Non-existent challenge
            Decimal('100.00')
        )
        
        # Assert
        assert commission is None
    
    def test_calculate_commission_no_referral(self, session, mock_challenge):
        """Test commission calculation when user has no referral"""
        # Act
        commission = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            Decimal('100.00')
        )
        
        # Assert
        assert commission is None
    
    def test_calculate_commission_inactive_agent(self, session, mock_challenge, mock_agent, mock_referral):
        """Test commission calculation with inactive agent"""
        # Arrange
        mock_agent.is_active = False
        session.commit()
        
        # Act
        commission = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            Decimal('100.00')
        )
        
        # Assert
        assert commission is None
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_calculate_commission_duplicate(self, mock_notify, session, mock_challenge, mock_agent, mock_referral):
        """Test that duplicate commissions are not created"""
        # Arrange
        sale_amount = Decimal('100.00')
        
        # Create first commission
        commission1 = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            sale_amount
        )
        
        # Act - Try to create duplicate
        commission2 = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            sale_amount
        )
        
        # Assert
        assert commission1 is not None
        assert commission2 is not None
        assert commission1.id == commission2.id  # Same commission returned
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_calculate_commission_different_rates(self, mock_notify, session, mock_challenge, mock_agent, mock_referral):
        """Test commission calculation with different commission rates"""
        # Arrange
        mock_agent.commission_rate = Decimal('15.50')
        session.commit()
        sale_amount = Decimal('200.00')
        
        # Act
        commission = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            sale_amount
        )
        
        # Assert
        assert commission.commission_rate == Decimal('15.50')
        assert commission.commission_amount == Decimal('31.00')  # 15.5% of 200


class TestCommissionApproval:
    """Test commission approval"""
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_approve_commission_success(self, mock_notify, session, mock_challenge, mock_agent, mock_referral):
        """Test successful commission approval"""
        # Arrange
        commission = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            Decimal('100.00')
        )
        approver_id = 1
        
        # Act
        approved = CommissionService.approve_commission(commission.id, approver_id)
        
        # Assert
        assert approved is not None
        assert approved.status == 'approved'
        assert approved.approved_at is not None
        
        # Verify notification sent
        assert mock_notify.call_count == 2  # One for creation, one for approval
    
    def test_approve_commission_not_found(self, session):
        """Test approving non-existent commission"""
        # Act
        result = CommissionService.approve_commission(999999, 1)
        
        # Assert
        assert result is None
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_approve_commission_already_approved(self, mock_notify, session, mock_challenge, mock_agent, mock_referral):
        """Test approving already approved commission"""
        # Arrange
        commission = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            Decimal('100.00')
        )
        CommissionService.approve_commission(commission.id, 1)
        
        # Act - Try to approve again
        result = CommissionService.approve_commission(commission.id, 1)
        
        # Assert
        assert result is None


class TestCommissionPayment:
    """Test commission payment"""
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_mark_commission_paid_success(self, mock_notify, session, mock_challenge, mock_agent, mock_referral):
        """Test successfully marking commission as paid"""
        # Arrange
        commission = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            Decimal('100.00')
        )
        CommissionService.approve_commission(commission.id, 1)
        
        initial_pending = mock_agent.pending_balance
        
        # Act
        paid = CommissionService.mark_commission_paid(
            commission.id,
            'bank_transfer',
            'TXN123456'
        )
        
        # Assert
        assert paid is not None
        assert paid.status == 'paid'
        assert paid.paid_at is not None
        assert paid.payment_method == 'bank_transfer'
        assert paid.transaction_id == 'TXN123456'
        
        # Verify agent balances updated
        session.refresh(mock_agent)
        assert mock_agent.pending_balance == Decimal('0')
        assert mock_agent.total_earned == Decimal('10.00')
        assert mock_agent.total_withdrawn == Decimal('10.00')
        
        # Verify notification sent
        assert mock_notify.call_count == 3  # Creation, approval, payment
    
    def test_mark_commission_paid_not_found(self, session):
        """Test marking non-existent commission as paid"""
        # Act
        result = CommissionService.mark_commission_paid(999999, 'bank_transfer', 'TXN123')
        
        # Assert
        assert result is None
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_mark_commission_paid_not_approved(self, mock_notify, session, mock_challenge, mock_agent, mock_referral):
        """Test marking unapproved commission as paid"""
        # Arrange
        commission = CommissionService.calculate_and_create_commission(
            mock_challenge.id,
            Decimal('100.00')
        )
        
        # Act - Try to mark as paid without approval
        result = CommissionService.mark_commission_paid(
            commission.id,
            'bank_transfer',
            'TXN123'
        )
        
        # Assert
        assert result is None


class TestCommissionRetrieval:
    """Test commission retrieval and filtering"""
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_get_agent_commissions_all(self, mock_notify, session, mock_agent, mock_referral):
        """Test getting all commissions for an agent"""
        # Arrange - Create multiple commissions
        from src.models import TradingProgram, Tenant
        
        tenant = Tenant(name='Test', subdomain=f'test_{__import__('uuid').uuid4().hex[:8]}')
        session.add(tenant)
        session.flush()
        
        program = TradingProgram(
            name='Test',
            type='one_phase',
            account_size=10000,
            price=100,
            tenant_id=tenant.id
        )
        session.add(program)
        session.flush()
        
        for i in range(5):
            user = User(email=f'user{i}@test.com', first_name='Test', last_name='User')
            user.set_password('pass')
            session.add(user)
            session.flush()
            
            challenge = Challenge(
                user_id=user.id,
                program_id=program.id,
                status='active',
                payment_status='paid'
            )
            session.add(challenge)
            session.flush()
            
            referral = Referral(
                agent_id=mock_agent.id,
                referred_user_id=user.id,
                referral_code=f'TEST_REF_{i:03d}',
                status='active'
            )
            session.add(referral)
            session.flush()
            
            CommissionService.calculate_and_create_commission(challenge.id, Decimal('100.00'))
        
        # Act
        pagination = CommissionService.get_agent_commissions(mock_agent.id)
        
        # Assert
        assert pagination.total == 5
        assert len(pagination.items) == 5
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_get_agent_commissions_by_status(self, mock_notify, session, mock_agent, mock_referral):
        """Test getting commissions filtered by status"""
        # Arrange - Create commissions with different statuses
        from src.models import TradingProgram, Tenant
        
        tenant = Tenant(name='Test', subdomain=f'test_{__import__('uuid').uuid4().hex[:8]}')
        session.add(tenant)
        session.flush()
        
        program = TradingProgram(
            name='Test',
            type='one_phase',
            account_size=10000,
            price=100,
            tenant_id=tenant.id
        )
        session.add(program)
        session.flush()
        
        for i in range(3):
            user = User(email=f'user{i}@test.com', first_name='Test', last_name='User')
            user.set_password('pass')
            session.add(user)
            session.flush()
            
            challenge = Challenge(
                user_id=user.id,
                program_id=program.id,
                status='active',
                payment_status='paid'
            )
            session.add(challenge)
            session.flush()
            
            referral = Referral(
                agent_id=mock_agent.id,
                referred_user_id=user.id,
                referral_code=f'TEST_REF_{i:03d}',
                status='active'
            )
            session.add(referral)
            session.flush()
            
            commission = CommissionService.calculate_and_create_commission(challenge.id, Decimal('100.00'))
            
            # Approve some
            if i < 2:
                CommissionService.approve_commission(commission.id, 1)
        
        # Act
        pending = CommissionService.get_agent_commissions(mock_agent.id, status='pending')
        approved = CommissionService.get_agent_commissions(mock_agent.id, status='approved')
        
        # Assert
        assert pending.total == 1
        assert approved.total == 2
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_get_agent_commissions_pagination(self, mock_notify, session, mock_agent):
        """Test commission pagination"""
        # Arrange - Create many commissions
        from src.models import TradingProgram, Tenant
        
        tenant = Tenant(name='Test', subdomain=f'test_{__import__('uuid').uuid4().hex[:8]}')
        session.add(tenant)
        session.flush()
        
        program = TradingProgram(
            name='Test',
            type='one_phase',
            account_size=10000,
            price=100,
            tenant_id=tenant.id
        )
        session.add(program)
        session.flush()
        
        for i in range(25):
            user = User(email=f'user{i}@test.com', first_name='Test', last_name='User')
            user.set_password('pass')
            session.add(user)
            session.flush()
            
            challenge = Challenge(
                user_id=user.id,
                program_id=program.id,
                status='active',
                payment_status='paid'
            )
            session.add(challenge)
            session.flush()
            
            referral = Referral(
                agent_id=mock_agent.id,
                referred_user_id=user.id,
                referral_code=f'TEST_REF_{i:03d}',
                status='active'
            )
            session.add(referral)
            session.flush()
            
            CommissionService.calculate_and_create_commission(challenge.id, Decimal('100.00'))
        
        # Act
        page1 = CommissionService.get_agent_commissions(mock_agent.id, page=1, per_page=10)
        page2 = CommissionService.get_agent_commissions(mock_agent.id, page=2, per_page=10)
        
        # Assert
        assert page1.total == 25
        assert len(page1.items) == 10
        assert len(page2.items) == 10
        assert page1.pages == 3


class TestCommissionStatistics:
    """Test commission statistics"""
    
    @patch('src.services.notification_service.NotificationService.create_notification')
    def test_get_commission_stats_success(self, mock_notify, session, mock_agent, mock_referral):
        """Test getting commission statistics"""
        # Arrange - Create commissions with different statuses
        from src.models import TradingProgram, Tenant
        
        tenant = Tenant(name='Test', subdomain=f'test_{__import__('uuid').uuid4().hex[:8]}')
        session.add(tenant)
        session.flush()
        
        program = TradingProgram(
            name='Test',
            type='one_phase',
            account_size=10000,
            price=100,
            tenant_id=tenant.id
        )
        session.add(program)
        session.flush()
        
        # Create 3 pending, 2 approved, 1 paid
        for i in range(6):
            user = User(email=f'user{i}@test.com', first_name='Test', last_name='User')
            user.set_password('pass')
            session.add(user)
            session.flush()
            
            challenge = Challenge(
                user_id=user.id,
                program_id=program.id,
                status='active',
                payment_status='paid'
            )
            session.add(challenge)
            session.flush()
            
            referral = Referral(
                agent_id=mock_agent.id,
                referred_user_id=user.id,
                referral_code=f'TEST_REF_{i:03d}',
                status='active'
            )
            session.add(referral)
            session.flush()
            
            commission = CommissionService.calculate_and_create_commission(challenge.id, Decimal('100.00'))
            
            if i < 3:  # Approve first 3
                CommissionService.approve_commission(commission.id, 1)
                if i < 1:  # Pay first 1
                    CommissionService.mark_commission_paid(commission.id, 'bank_transfer', f'TXN{i}')
        
        # Act
        stats = CommissionService.get_agent_commission_stats(mock_agent.id)
        
        # Assert
        assert stats is not None
        assert stats['agent_id'] == mock_agent.id
        assert stats['commission_rate'] == 10.0
        assert stats['pending']['count'] == 3
        assert stats['approved']['count'] == 2
        assert stats['paid']['count'] == 1
        assert stats['total_commissions'] == 6
        assert stats['pending']['amount'] == 30.0  # 3 * $10
        assert stats['approved']['amount'] == 20.0  # 2 * $10
        assert stats['paid']['amount'] == 10.0  # 1 * $10
        assert stats['total_commission_amount'] == 60.0  # 6 * $10
    
    def test_get_commission_stats_agent_not_found(self, session):
        """Test getting stats for non-existent agent"""
        # Act
        stats = CommissionService.get_agent_commission_stats(999999)
        
        # Assert
        assert stats is None
    
    def test_get_commission_stats_no_commissions(self, session, mock_agent):
        """Test getting stats when agent has no commissions"""
        # Act
        stats = CommissionService.get_agent_commission_stats(mock_agent.id)
        
        # Assert
        assert stats is not None
        assert stats['total_commissions'] == 0
        assert stats['pending']['count'] == 0
        assert stats['approved']['count'] == 0
        assert stats['paid']['count'] == 0
