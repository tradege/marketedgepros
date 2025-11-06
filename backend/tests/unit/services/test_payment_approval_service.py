"""
Unit tests for Payment Approval Service
Tests approval workflow for cash and free payments
"""
import pytest
from decimal import Decimal
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.services.payment_approval_service import PaymentApprovalService
from src.models import PaymentApprovalRequest, Challenge, Payment, User, TradingProgram


@pytest.fixture
def mock_tenant(session):
    """Create a mock tenant"""
    from src.models.tenant import Tenant
    tenant = Tenant(
        name='Test Tenant',
        subdomain=f'test_{__import__('uuid').uuid4().hex[:8]}',
        status='active'
    )
    session.add(tenant)
    session.commit()
    return tenant


@pytest.fixture
def mock_supermaster(session):
    """Create a super admin user"""
    user = User(
        email='supermaster@example.com',
        first_name='Super',
        last_name='Admin',
        role='supermaster'
    )
    user.set_password('password123')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def mock_master(session):
    """Create a master user"""
    user = User(
        email='master@example.com',
        first_name='Master',
        last_name='User',
        role='master'
    )
    user.set_password('password123')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def mock_trader(session):
    """Create a trader user"""
    user = User(
        email='trader@example.com',
        first_name='Trader',
        last_name='User',
        role='trader'
    )
    user.set_password('password123')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def mock_program(session, mock_tenant):
    """Create a mock trading program"""
    program = TradingProgram(
        tenant_id=mock_tenant.id,
        name='Test Program',
        type='one_phase',
        account_size=10000.00,
        price=100.00,
        profit_target=10.00,  # 10% profit target
        max_daily_loss=5.00,  # 5% max daily loss
        max_total_loss=10.00  # 10% max total loss
    )
    session.add(program)
    session.commit()
    return program


@pytest.fixture
def mock_challenge(session, mock_trader, mock_program):
    """Create a mock challenge"""
    challenge = Challenge(
        user_id=mock_trader.id,
        program_id=mock_program.id,
        status='pending',
        approval_status='pending'
    )
    session.add(challenge)
    session.commit()
    return challenge


@pytest.fixture
def mock_payment(session, mock_trader):
    """Create a mock payment"""
    payment = Payment(
        user_id=mock_trader.id,
        amount=Decimal('100'),
        status='pending',
        payment_type='cash'
    )
    session.add(payment)
    session.commit()
    return payment


class TestPermissionChecks:
    """Test permission checking methods"""
    
    def test_supermaster_can_use_cash_payment(self, session, mock_supermaster):
        """Test that supermaster can use cash payment"""
        assert PaymentApprovalService.can_use_cash_payment(mock_supermaster) is True
    
    def test_master_can_use_cash_payment(self, session, mock_master):
        """Test that master can use cash payment"""
        assert PaymentApprovalService.can_use_cash_payment(mock_master) is True
    
    def test_trader_cannot_use_cash_payment(self, session, mock_trader):
        """Test that trader cannot use cash payment"""
        assert PaymentApprovalService.can_use_cash_payment(mock_trader) is False
    
    def test_only_supermaster_can_create_free_account(self, session, mock_supermaster):
        """Test that only supermaster can create free accounts"""
        assert PaymentApprovalService.can_create_free_account(mock_supermaster) is True
    
    def test_master_cannot_create_free_account(self, session, mock_master):
        """Test that master cannot create free accounts"""
        assert PaymentApprovalService.can_create_free_account(mock_master) is False
    
    def test_trader_cannot_create_free_account(self, session, mock_trader):
        """Test that trader cannot create free accounts"""
        assert PaymentApprovalService.can_create_free_account(mock_trader) is False


class TestCreateApprovalRequest:
    """Test creating approval requests"""
    
    @patch('src.services.payment_approval_service.PaymentApprovalService._notify_super_admins')
    def test_create_cash_approval_request_by_master(self, mock_notify, session, mock_master, 
                                                     mock_trader, mock_challenge, mock_payment):
        """Test creating cash payment approval request by master"""
        # Act
        request = PaymentApprovalService.create_approval_request(
            challenge_id=mock_challenge.id,
            payment_id=mock_payment.id,
            requested_by_id=mock_master.id,
            requested_for_id=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash'
        )
        
        # Assert
        assert request is not None
        assert request.challenge_id == mock_challenge.id
        assert request.payment_id == mock_payment.id
        assert request.requested_by == mock_master.id
        assert request.requested_for == mock_trader.id
        assert request.amount == Decimal('100.00')
        assert request.payment_type == 'cash'
        assert request.status == 'pending'
        
        # Check that challenge was updated
        session.refresh(mock_challenge)
        assert mock_challenge.approval_status == 'pending'
        assert mock_challenge.payment_type == 'cash'
        
        # Check that payment was updated
        session.refresh(mock_payment)
        assert mock_payment.approval_status == 'pending'
        assert mock_payment.payment_type == 'cash'
        
        # Check that notification was sent
        mock_notify.assert_called_once()
    
    @patch('src.services.payment_approval_service.PaymentApprovalService._notify_super_admins')
    def test_create_free_approval_request_by_supermaster(self, mock_notify, session, mock_supermaster,
                                                          mock_trader, mock_challenge):
        """Test creating free account approval request by supermaster"""
        # Act
        request = PaymentApprovalService.create_approval_request(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by_id=mock_supermaster.id,
            requested_for_id=mock_trader.id,
            amount=Decimal('0.00'),
            payment_type='free'
        )
        
        # Assert
        assert request.payment_type == 'free'
        assert request.amount == Decimal('0.00')
        assert request.status == 'pending'
    
    def test_create_approval_request_invalid_payment_type(self, session, mock_master, mock_trader, mock_challenge):
        """Test that invalid payment type is rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Payment type must be 'cash' or 'free'"):
            PaymentApprovalService.create_approval_request(
                challenge_id=mock_challenge.id,
                payment_id=None,
                requested_by_id=mock_master.id,
                requested_for_id=mock_trader.id,
                amount=Decimal('100.00'),
                payment_type='invalid'
            )
    
    def test_create_approval_request_requester_not_found(self, session, mock_trader, mock_challenge):
        """Test that non-existent requester is rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Requester not found"):
            PaymentApprovalService.create_approval_request(
                challenge_id=mock_challenge.id,
                payment_id=None,
                requested_by_id=99999,  # Non-existent user
                requested_for_id=mock_trader.id,
                amount=Decimal('100.00'),
                payment_type='cash'
            )
    
    def test_create_free_request_by_master_rejected(self, session, mock_master, mock_trader, mock_challenge):
        """Test that master cannot create free account requests"""
        # Act & Assert
        with pytest.raises(ValueError, match="Only Super Admin can create free accounts"):
            PaymentApprovalService.create_approval_request(
                challenge_id=mock_challenge.id,
                payment_id=None,
                requested_by_id=mock_master.id,
                requested_for_id=mock_trader.id,
                amount=Decimal('0.00'),
                payment_type='free'
            )
    
    def test_create_cash_request_by_trader_rejected(self, session, mock_trader, mock_challenge):
        """Test that trader cannot create cash payment requests"""
        # Create another trader to be the recipient
        trader2 = User(
            email='trader2@example.com',
            first_name='Trader2',
            last_name='User2',
            role='trader'
        )
        trader2.set_password('password123')
        session.add(trader2)
        session.commit()
        
        # Act & Assert
        with pytest.raises(ValueError, match="Only Super Admin and Masters can use cash payment"):
            PaymentApprovalService.create_approval_request(
                challenge_id=mock_challenge.id,
                payment_id=None,
                requested_by_id=mock_trader.id,
                requested_for_id=trader2.id,
                amount=Decimal('100.00'),
                payment_type='cash'
            )


class TestApproveRequest:
    """Test approving approval requests"""
    
    @patch('src.services.payment_approval_service.PaymentApprovalService._notify_approval')
    @patch('src.services.payment_approval_service.CommissionService.calculate_and_create_commission')
    def test_approve_request_success(self, mock_commission, mock_notify, session, mock_supermaster,
                                     mock_master, mock_trader, mock_challenge, mock_payment):
        """Test successful approval of request"""
        # Arrange
        request = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=mock_payment.id,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash',
            status='pending'
        )
        session.add(request)
        session.commit()
        
        # Act
        approved_request = PaymentApprovalService.approve_request(
            request.id,
            mock_supermaster.id,
            admin_notes='Approved for testing'
        )
        
        # Assert
        assert approved_request.status == 'approved'
        assert approved_request.reviewed_by == mock_supermaster.id
        assert approved_request.reviewed_at is not None
        assert approved_request.admin_notes == 'Approved for testing'
        
        # Check challenge was updated
        session.refresh(mock_challenge)
        assert mock_challenge.approval_status == 'approved'
        assert mock_challenge.approved_by == mock_supermaster.id
        assert mock_challenge.approved_at is not None
        assert mock_challenge.payment_status == 'paid'
        assert mock_challenge.status == 'active'
        
        # Check payment was updated
        session.refresh(mock_payment)
        assert mock_payment.approval_status == 'approved'
        assert mock_payment.approved_by == mock_supermaster.id
        assert mock_payment.approved_at is not None
        assert mock_payment.status == 'completed'
        assert mock_payment.completed_at is not None
        
        # Check commission was created
        mock_commission.assert_called_once()
        
        # Check notification was sent
        mock_notify.assert_called_once_with(approved_request, approved=True)
    
    def test_approve_request_non_supermaster_rejected(self, session, mock_master, mock_trader, mock_challenge):
        """Test that non-supermaster cannot approve requests"""
        # Arrange
        request = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash',
            status='pending'
        )
        session.add(request)
        session.commit()
        
        # Act & Assert
        with pytest.raises(ValueError, match="Only Super Admin can approve payment requests"):
            PaymentApprovalService.approve_request(request.id, mock_master.id)
    
    def test_approve_request_not_found(self, session, mock_supermaster):
        """Test that non-existent request is rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Approval request not found"):
            PaymentApprovalService.approve_request(99999, mock_supermaster.id)
    
    def test_approve_request_not_pending(self, session, mock_supermaster, mock_master, mock_trader, mock_challenge):
        """Test that already processed request cannot be approved"""
        # Arrange
        request = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash',
            status='approved'  # Already approved
        )
        session.add(request)
        session.commit()
        
        # Act & Assert
        with pytest.raises(ValueError, match="Approval request is not pending"):
            PaymentApprovalService.approve_request(request.id, mock_supermaster.id)


class TestRejectRequest:
    """Test rejecting approval requests"""
    
    @patch('src.services.payment_approval_service.PaymentApprovalService._notify_approval')
    def test_reject_request_success(self, mock_notify, session, mock_supermaster, mock_master,
                                    mock_trader, mock_challenge, mock_payment):
        """Test successful rejection of request"""
        # Arrange
        request = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=mock_payment.id,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash',
            status='pending'
        )
        session.add(request)
        session.commit()
        
        # Act
        rejected_request = PaymentApprovalService.reject_request(
            request.id,
            mock_supermaster.id,
            rejection_reason='Insufficient documentation',
            admin_notes='Need more proof'
        )
        
        # Assert
        assert rejected_request.status == 'rejected'
        assert rejected_request.reviewed_by == mock_supermaster.id
        assert rejected_request.reviewed_at is not None
        assert rejected_request.rejection_reason == 'Insufficient documentation'
        assert rejected_request.admin_notes == 'Need more proof'
        
        # Check challenge was updated
        session.refresh(mock_challenge)
        assert mock_challenge.approval_status == 'rejected'
        assert mock_challenge.approved_by == mock_supermaster.id
        assert mock_challenge.approved_at is not None
        assert mock_challenge.rejection_reason == 'Insufficient documentation'
        assert mock_challenge.status == 'failed'
        
        # Check payment was updated
        session.refresh(mock_payment)
        assert mock_payment.approval_status == 'rejected'
        assert mock_payment.approved_by == mock_supermaster.id
        assert mock_payment.approved_at is not None
        assert mock_payment.rejection_reason == 'Insufficient documentation'
        assert mock_payment.status == 'failed'
        
        # Check notification was sent
        mock_notify.assert_called_once_with(rejected_request, approved=False)
    
    def test_reject_request_non_supermaster_rejected(self, session, mock_master, mock_trader, mock_challenge):
        """Test that non-supermaster cannot reject requests"""
        # Arrange
        request = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash',
            status='pending'
        )
        session.add(request)
        session.commit()
        
        # Act & Assert
        with pytest.raises(ValueError, match="Only Super Admin can reject payment requests"):
            PaymentApprovalService.reject_request(
                request.id,
                mock_master.id,
                rejection_reason='Test'
            )
    
    def test_reject_request_not_found(self, session, mock_supermaster):
        """Test that non-existent request is rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Approval request not found"):
            PaymentApprovalService.reject_request(
                99999,
                mock_supermaster.id,
                rejection_reason='Test'
            )
    
    def test_reject_request_not_pending(self, session, mock_supermaster, mock_master, mock_trader, mock_challenge):
        """Test that already processed request cannot be rejected"""
        # Arrange
        request = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash',
            status='rejected'  # Already rejected
        )
        session.add(request)
        session.commit()
        
        # Act & Assert
        with pytest.raises(ValueError, match="Approval request is not pending"):
            PaymentApprovalService.reject_request(
                request.id,
                mock_supermaster.id,
                rejection_reason='Test'
            )


class TestRetrievalMethods:
    """Test request retrieval methods"""
    
    def test_get_pending_requests(self, session, mock_master, mock_trader, mock_challenge):
        """Test getting all pending requests"""
        # Arrange
        request1 = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash',
            status='pending'
        )
        request2 = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('200.00'),
            payment_type='cash',
            status='pending'
        )
        request3 = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('300.00'),
            payment_type='cash',
            status='approved'  # Not pending
        )
        session.add_all([request1, request2, request3])
        session.commit()
        
        # Act
        pending = PaymentApprovalService.get_pending_requests()
        
        # Assert
        assert len(pending) == 2
        assert all(r.status == 'pending' for r in pending)
    
    def test_get_request_by_id(self, session, mock_master, mock_trader, mock_challenge):
        """Test getting request by ID"""
        # Arrange
        request = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash',
            status='pending'
        )
        session.add(request)
        session.commit()
        
        # Act
        found = PaymentApprovalService.get_request_by_id(request.id)
        
        # Assert
        assert found is not None
        assert found.id == request.id
    
    def test_get_request_by_id_not_found(self, session):
        """Test getting non-existent request"""
        # Act
        found = PaymentApprovalService.get_request_by_id(99999)
        
        # Assert
        assert found is None
    
    def test_get_requests_by_requester(self, session, mock_master, mock_trader, mock_challenge):
        """Test getting all requests by a specific requester"""
        # Arrange - Create another master
        master2 = User(
            email='master2@example.com',
            first_name='Master2',
            last_name='User2',
            role='master'
        )
        master2.set_password('password123')
        session.add(master2)
        session.commit()
        
        # Create requests from both masters
        request1 = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('100.00'),
            payment_type='cash',
            status='pending'
        )
        request2 = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=mock_master.id,
            requested_for=mock_trader.id,
            amount=Decimal('200.00'),
            payment_type='cash',
            status='approved'
        )
        request3 = PaymentApprovalRequest(
            challenge_id=mock_challenge.id,
            payment_id=None,
            requested_by=master2.id,
            requested_for=mock_trader.id,
            amount=Decimal('300.00'),
            payment_type='cash',
            status='pending'
        )
        session.add_all([request1, request2, request3])
        session.commit()
        
        # Act
        master_requests = PaymentApprovalService.get_requests_by_requester(mock_master.id)
        
        # Assert
        assert len(master_requests) == 2
        assert all(r.requested_by == mock_master.id for r in master_requests)
