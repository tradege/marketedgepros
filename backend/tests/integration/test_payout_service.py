import pytest
import uuid
from datetime import datetime
from decimal import Decimal
from src.services.payout_service import PayoutService
from src.models import User
from src.models import TradingProgram
from src.models import PayoutRequest
from src.models import Tenant
from src.database import db


@pytest.fixture
def payout_service():
    return PayoutService()


@pytest.fixture
def test_tenant(session):
    """Create a test tenant"""
    tenant = session.query(Tenant).first()
    if not tenant:
        tenant = Tenant(
            name="Test Tenant",
            subdomain=f"test{uuid.uuid4().hex[:6]}",
            is_active=True
        )
        session.add(tenant)
        session.commit()
    return tenant


@pytest.fixture
def trader_user(session):
    """Create a trader user with available balance"""
    unique_email = f"trader_{uuid.uuid4().hex[:8]}@test.com"
    user = User(
        email=unique_email,
        first_name="Test",
        last_name="Trader",
        role="trader",
        is_active=True,
        is_verified=True,
        available_balance=Decimal("1000.00"),
        total_withdrawn=Decimal("0.00"),
        payout_count=0
    )
    user.set_password("password123")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def trading_program(session, test_tenant):
    """Create a trading program template"""
    program = TradingProgram(
        tenant_id=test_tenant.id,
        name="Test Program",
        type="one_phase",
        account_size=Decimal("10000.00"),
        price=Decimal("99.00"),
        profit_split=Decimal("80.00"),
        profit_split_percentage=Decimal("80.00"),
        minimum_payout_amount=Decimal("50.00"),
        payout_mode="on_demand"
    )
    session.add(program)
    session.commit()
    return program


class TestCanRequestPayout:
    def test_can_request_when_eligible(self, payout_service, trader_user, trading_program):
        """Test that eligible user can request payout"""
        result = payout_service.can_request_payout(trader_user, trading_program)
        
        assert result["can_request"] is True
        assert len(result["errors"]) == 0
        assert result["available_balance"] == 1000.00
        assert result["minimum_amount"] == 50.00
        assert result["payout_mode"] == "on_demand"
        assert result["profit_split"] == 80.00

    def test_cannot_request_when_no_balance(self, session, payout_service, trader_user, trading_program):
        """Test that user with no balance cannot request payout"""
        trader_user.available_balance = Decimal("0.00")
        session.commit()
        
        result = payout_service.can_request_payout(trader_user, trading_program)
        
        assert result["can_request"] is False
        assert "No available balance" in result["errors"][0]

    def test_cannot_request_when_below_minimum(self, session, payout_service, trader_user, trading_program):
        """Test that user below minimum cannot request payout"""
        trader_user.available_balance = Decimal("25.00")
        session.commit()
        
        result = payout_service.can_request_payout(trader_user, trading_program)
        
        assert result["can_request"] is False
        assert "Minimum payout amount" in result["errors"][0]

    def test_cannot_request_when_pending_exists(self, session, payout_service, trader_user, trading_program):
        """Test that user cannot request payout when pending request exists"""
        # Create pending payout
        payout = PayoutRequest(
            user_id=trader_user.id,
            program_id=trading_program.id,
            amount=Decimal("100.00"),
            profit_split_amount=Decimal("80.00"),
            payment_method="bank_transfer",
            payment_details={"iban": "TEST123"},
            status="pending",
            payout_mode="on_demand"
        )
        session.add(payout)
        session.commit()
        
        result = payout_service.can_request_payout(trader_user, trading_program)
        
        assert result["can_request"] is False
        assert "pending payout request" in result["errors"][0]


class TestRequestPayout:
    def test_request_payout_success(self, payout_service, trader_user, trading_program):
        """Test successful payout request"""
        initial_balance = trader_user.available_balance
        
        payout = payout_service.request_payout(
            user=trader_user,
            program=trading_program,
            amount=Decimal("200.00"),
            payment_method="bank_transfer",
            payment_details={"iban": "TEST123456"}
        )
        
        assert payout is not None
        assert payout.amount == Decimal("200.00")
        assert payout.profit_split_amount == Decimal("160.00")  # 80% of 200
        assert payout.status == "pending"
        assert payout.payment_method == "bank_transfer"
        assert trader_user.available_balance == initial_balance - Decimal("200.00")

    def test_request_payout_exceeds_available(self, payout_service, trader_user, trading_program):
        """Test that requesting more than available fails"""
        with pytest.raises(ValueError, match="exceeds available balance"):
            payout_service.request_payout(
                user=trader_user,
                program=trading_program,
                amount=Decimal("5000.00"),
                payment_method="bank_transfer",
                payment_details={}
            )

    def test_request_payout_below_minimum(self, payout_service, trader_user, trading_program):
        """Test that requesting below minimum fails"""
        with pytest.raises(ValueError, match="Minimum payout amount"):
            payout_service.request_payout(
                user=trader_user,
                program=trading_program,
                amount=Decimal("25.00"),
                payment_method="bank_transfer",
                payment_details={}
            )


class TestApprovePayout:
    def test_approve_payout_success(self, session, payout_service, trader_user, trading_program, admin_user):
        """Test successful payout approval"""
        # Create pending payout
        payout = PayoutRequest(
            user_id=trader_user.id,
            program_id=trading_program.id,
            amount=Decimal("100.00"),
            profit_split_amount=Decimal("80.00"),
            payment_method="bank_transfer",
            payment_details={},
            status="pending",
            payout_mode="on_demand"
        )
        session.add(payout)
        session.commit()
        
        approved = payout_service.approve_payout(payout.id, approver_id=admin_user.id, notes="Approved by admin")
        
        assert approved.status == "approved"
        assert approved.approved_date is not None
        assert approved.approved_by == admin_user.id
        assert approved.notes == "Approved by admin"

    def test_cannot_approve_non_pending(self, session, payout_service, trader_user, trading_program):
        """Test that non-pending payout cannot be approved"""
        payout = PayoutRequest(
            user_id=trader_user.id,
            program_id=trading_program.id,
            amount=Decimal("100.00"),
            profit_split_amount=Decimal("80.00"),
            payment_method="bank_transfer",
            payment_details={},
            status="paid",
            payout_mode="on_demand"
        )
        session.add(payout)
        session.commit()
        
        with pytest.raises(ValueError, match="Cannot approve payout"):
            payout_service.approve_payout(payout.id, approver_id=admin_user.id)


class TestRejectPayout:
    def test_reject_payout_success(self, session, payout_service, trader_user, trading_program, admin_user):
        """Test successful payout rejection"""
        initial_balance = trader_user.available_balance
        
        payout = PayoutRequest(
            user_id=trader_user.id,
            program_id=trading_program.id,
            amount=Decimal("100.00"),
            profit_split_amount=Decimal("80.00"),
            payment_method="bank_transfer",
            payment_details={},
            status="pending",
            payout_mode="on_demand"
        )
        session.add(payout)
        session.commit()
        
        rejected = payout_service.reject_payout(
            payout.id,
            approver_id=admin_user.id,
            reason="Insufficient documentation"
        )
        
        assert rejected.status == "rejected"
        assert rejected.rejection_reason == "Insufficient documentation"
        assert rejected.approved_date is not None
        # Balance should be restored
        assert trader_user.available_balance == initial_balance + Decimal("100.00")


class TestMarkAsPaid:
    def test_mark_as_paid_success(self, session, payout_service, trader_user, trading_program):
        """Test successfully marking payout as paid"""
        initial_withdrawn = trader_user.total_withdrawn
        initial_count = trader_user.payout_count
        
        payout = PayoutRequest(
            user_id=trader_user.id,
            program_id=trading_program.id,
            amount=Decimal("100.00"),
            profit_split_amount=Decimal("80.00"),
            payment_method="bank_transfer",
            payment_details={},
            status="approved",
            payout_mode="on_demand"
        )
        session.add(payout)
        session.commit()
        
        paid = payout_service.mark_as_paid(payout.id, notes="Transferred via bank")
        
        assert paid.status == "paid"
        assert paid.paid_date is not None
        assert "Transferred via bank" in paid.notes
        assert trader_user.total_withdrawn == initial_withdrawn + Decimal("80.00")
        assert trader_user.payout_count == initial_count + 1


class TestGetPayouts:
    def test_get_user_payouts(self, session, payout_service, trader_user, trading_program):
        """Test getting user payouts"""
        # Create multiple payouts
        for i in range(3):
            payout = PayoutRequest(
                user_id=trader_user.id,
                program_id=trading_program.id,
                amount=Decimal("100.00"),
                profit_split_amount=Decimal("80.00"),
                payment_method="bank_transfer",
                payment_details={},
                status="pending" if i == 0 else "paid",
                payout_mode="on_demand"
            )
            session.add(payout)
        session.commit()
        
        payouts = payout_service.get_user_payouts(trader_user.id)
        
        assert len(payouts) == 3

    def test_get_user_payouts_filtered(self, session, payout_service, trader_user, trading_program):
        """Test getting user payouts filtered by status"""
        # Create payouts with different statuses
        for status in ["pending", "paid", "rejected"]:
            payout = PayoutRequest(
                user_id=trader_user.id,
                program_id=trading_program.id,
                amount=Decimal("100.00"),
                profit_split_amount=Decimal("80.00"),
                payment_method="bank_transfer",
                payment_details={},
                status=status,
                payout_mode="on_demand"
            )
            session.add(payout)
        session.commit()
        
        pending_payouts = payout_service.get_user_payouts(trader_user.id, status="pending")
        
        assert len(pending_payouts) == 1
        assert pending_payouts[0].status == "pending"

    def test_get_pending_payouts(self, session, payout_service, trader_user, trading_program):
        """Test getting all pending payouts"""
        payout = PayoutRequest(
            user_id=trader_user.id,
            program_id=trading_program.id,
            amount=Decimal("100.00"),
            profit_split_amount=Decimal("80.00"),
            payment_method="bank_transfer",
            payment_details={},
            status="pending",
            payout_mode="on_demand"
        )
        session.add(payout)
        session.commit()
        
        pending_payouts = payout_service.get_pending_payouts()
        
        assert len(pending_payouts) >= 1
        assert all(p.status == "pending" for p in pending_payouts)


class TestGetStatistics:
    def test_get_payout_statistics(self, session, payout_service, trader_user, trading_program):
        """Test getting payout statistics"""
        # Create payouts with different statuses
        for status in ["pending", "approved", "paid", "rejected"]:
            payout = PayoutRequest(
                user_id=trader_user.id,
                program_id=trading_program.id,
                amount=Decimal("100.00"),
                profit_split_amount=Decimal("80.00"),
                payment_method="bank_transfer",
                payment_details={},
                status=status,
                payout_mode="on_demand"
            )
            session.add(payout)
        session.commit()
        
        stats = payout_service.get_payout_statistics(user_id=trader_user.id)
        
        assert stats["total_requested"] == 4
        assert stats["total_pending"] == 1
        assert stats["total_approved"] == 1
        assert stats["total_paid"] == 1
        assert stats["total_rejected"] == 1
        assert stats["total_amount_paid"] == 80.00
        assert stats["success_rate"] == 25.0  # 1 paid out of 4
