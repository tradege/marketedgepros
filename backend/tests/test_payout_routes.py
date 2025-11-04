import pytest
import uuid
import json
from src.models import User, TradingProgram, PayoutRequest
from src.extensions import db


@pytest.fixture
def trader_with_program(database):
    user = User(
        email=f"trader_{uuid.uuid4().hex[:8]}@test.com",
        first_name="Test",
        last_name="Trader",
        role="trader",
        is_active=True,
        is_verified=True
    )
    user.set_password("password123")
    db.session.add(user)
    db.session.flush()
    
    program = TradingProgram(
        user_id=user.id,
        program_type="evaluation",
        account_size=10000.00,
        status="funded",
        profit_split=80.0,
        payout_mode="on_demand",
        balance=12000.00,
        equity=12000.00
    )
    db.session.add(program)
    db.session.commit()
    
    return user, program


@pytest.fixture
def admin_user(database):
    user = User(
        email=f"admin_{uuid.uuid4().hex[:8]}@test.com",
        first_name="Admin",
        last_name="User",
        role="supermaster",
        is_active=True,
        is_verified=True
    )
    user.set_password("admin123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_headers(client, trader_with_program):
    user, _ = trader_with_program
    response = client.post("/api/auth/login", json={
        "email": "trader@test.com",
        "password": "password123"
    })
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, admin_user):
    response = client.post("/api/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestCheckEligibility:
    def test_check_eligibility_success(self, client, auth_headers, trader_with_program):
        """Test checking payout eligibility"""
        _, program = trader_with_program
        
        response = client.get(
            f"/api/payouts/check-eligibility/{program.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json
        assert data["can_request"] is True
        assert data["available_balance"] == 2000.00

    def test_check_eligibility_unauthorized(self, client, trader_with_program):
        """Test checking eligibility without auth"""
        _, program = trader_with_program
        
        response = client.get(f"/api/payouts/check-eligibility/{program.id}")
        
        assert response.status_code == 401


class TestRequestPayout:
    def test_request_payout_success(self, client, auth_headers, trader_with_program):
        """Test successful payout request"""
        _, program = trader_with_program
        
        response = client.post(
            "/api/payouts/request",
            headers=auth_headers,
            json={
                "program_id": program.id,
                "amount": 1000.00,
                "payment_method": "bank_transfer",
                "payment_details": "IBAN: TEST123456"
            }
        )
        
        assert response.status_code == 201
        data = response.json
        assert data["payout"]["amount"] == 1000.00
        assert data["payout"]["status"] == "pending"

    def test_request_payout_invalid_amount(self, client, auth_headers, trader_with_program):
        """Test requesting invalid amount"""
        _, program = trader_with_program
        
        response = client.post(
            "/api/payouts/request",
            headers=auth_headers,
            json={
                "program_id": program.id,
                "amount": 10000.00,  # Too much
                "payment_method": "bank_transfer",
                "payment_details": "Test"
            }
        )
        
        assert response.status_code == 400

    def test_request_payout_missing_fields(self, client, auth_headers, trader_with_program):
        """Test requesting payout with missing fields"""
        _, program = trader_with_program
        
        response = client.post(
            "/api/payouts/request",
            headers=auth_headers,
            json={
                "program_id": program.id,
                "amount": 1000.00
                # Missing payment_method and payment_details
            }
        )
        
        assert response.status_code == 400


class TestGetMyPayouts:
    def test_get_my_payouts(self, client, auth_headers, trader_with_program):
        """Test getting user's payouts"""
        user, program = trader_with_program
        
        # Create some payouts
        for i in range(3):
            payout = PayoutRequest(
                user_id=user.id,
                program_id=program.id,
                amount=500.00,
                profit_split_amount=400.00,
                payment_method="bank_transfer",
                payment_details="Test",
                status="pending" if i == 0 else "paid"
            )
            db.session.add(payout)
        db.session.commit()
        
        response = client.get("/api/payouts/my-payouts", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert len(data["payouts"]) == 3

    def test_get_my_payouts_filtered(self, client, auth_headers, trader_with_program):
        """Test getting payouts filtered by status"""
        user, program = trader_with_program
        
        # Create payouts with different statuses
        for status in ["pending", "paid", "rejected"]:
            payout = PayoutRequest(
                user_id=user.id,
                program_id=program.id,
                amount=500.00,
                profit_split_amount=400.00,
                payment_method="bank_transfer",
                payment_details="Test",
                status=status
            )
            db.session.add(payout)
        db.session.commit()
        
        response = client.get(
            "/api/payouts/my-payouts?status=pending",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json
        assert len(data["payouts"]) == 1
        assert data["payouts"][0]["status"] == "pending"


class TestGetMyStatistics:
    def test_get_my_statistics(self, client, auth_headers, trader_with_program):
        """Test getting user statistics"""
        user, program = trader_with_program
        
        # Create a paid payout
        payout = PayoutRequest(
            user_id=user.id,
            program_id=program.id,
            amount=1000.00,
            profit_split_amount=800.00,
            payment_method="bank_transfer",
            payment_details="Test",
            status="paid"
        )
        db.session.add(payout)
        db.session.commit()
        
        response = client.get("/api/payouts/my-statistics", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data["total_withdrawn"] == 800.00
        assert data["payout_count"] == 1


class TestAdminEndpoints:
    def test_get_pending_payouts(self, client, admin_headers, trader_with_program):
        """Test admin getting pending payouts"""
        user, program = trader_with_program
        
        payout = PayoutRequest(
            user_id=user.id,
            program_id=program.id,
            amount=1000.00,
            profit_split_amount=800.00,
            payment_method="bank_transfer",
            payment_details="Test",
            status="pending"
        )
        db.session.add(payout)
        db.session.commit()
        
        response = client.get("/api/payouts/admin/pending", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json
        assert len(data["payouts"]) >= 1

    def test_approve_payout(self, client, admin_headers, trader_with_program):
        """Test admin approving payout"""
        user, program = trader_with_program
        
        payout = PayoutRequest(
            user_id=user.id,
            program_id=program.id,
            amount=1000.00,
            profit_split_amount=800.00,
            payment_method="bank_transfer",
            payment_details="Test",
            status="pending"
        )
        db.session.add(payout)
        db.session.commit()
        
        response = client.post(
            f"/api/payouts/admin/{payout.id}/approve",
            headers=admin_headers,
            json={"notes": "Approved by admin"}
        )
        
        assert response.status_code == 200
        data = response.json
        assert data["payout"]["status"] == "approved"

    def test_reject_payout(self, client, admin_headers, trader_with_program):
        """Test admin rejecting payout"""
        user, program = trader_with_program
        
        payout = PayoutRequest(
            user_id=user.id,
            program_id=program.id,
            amount=1000.00,
            profit_split_amount=800.00,
            payment_method="bank_transfer",
            payment_details="Test",
            status="pending"
        )
        db.session.add(payout)
        db.session.commit()
        
        response = client.post(
            f"/api/payouts/admin/{payout.id}/reject",
            headers=admin_headers,
            json={"reason": "Insufficient documentation"}
        )
        
        assert response.status_code == 200
        data = response.json
        assert data["payout"]["status"] == "rejected"

    def test_mark_as_paid(self, client, admin_headers, trader_with_program):
        """Test admin marking payout as paid"""
        user, program = trader_with_program
        
        payout = PayoutRequest(
            user_id=user.id,
            program_id=program.id,
            amount=1000.00,
            profit_split_amount=800.00,
            payment_method="bank_transfer",
            payment_details="Test",
            status="approved"
        )
        db.session.add(payout)
        db.session.commit()
        
        response = client.post(
            f"/api/payouts/admin/{payout.id}/mark-paid",
            headers=admin_headers,
            json={"notes": "Transferred via bank"}
        )
        
        assert response.status_code == 200
        data = response.json
        assert data["payout"]["status"] == "paid"

    def test_non_admin_cannot_access(self, client, auth_headers, trader_with_program):
        """Test that non-admin cannot access admin endpoints"""
        response = client.get("/api/payouts/admin/pending", headers=auth_headers)
        
        assert response.status_code == 403
