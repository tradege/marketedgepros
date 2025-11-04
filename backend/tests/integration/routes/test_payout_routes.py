"""
Integration Tests for Payout API Routes
Tests full HTTP request/response cycle
"""
import pytest
import json
from decimal import Decimal


@pytest.mark.integration
@pytest.mark.api
class TestPayoutRequestAPI:
    """Test payout request creation endpoint"""
    
    def test_request_payout_success(self, client, trader_user, auth_headers, session):
        """Test successful payout request"""
        # Arrange
        trader_user.available_balance = Decimal("1000.00")
        session.flush()
        
        data = {
            "amount": 500.00,
            "payment_method": "bank_transfer",
            "payment_details": {
                "account_number": "123456789",
                "bank_name": "Test Bank"
            }
        }
        
        # Act
        response = client.post(
            "/api/payouts/request",
            data=json.dumps(data),
            content_type="application/json",
            headers=auth_headers(trader_user)
        )
        
        # Assert
        assert response.status_code == 201
        data = json.loads(response.data)
        assert "payout" in data
        assert data["payout"]["amount"] == 500.00
        assert data["payout"]["status"] == "pending"
    
    def test_request_payout_insufficient_balance(self, client, trader_user, auth_headers):
        """Test payout request with insufficient balance"""
        # Arrange
        trader_user.available_balance = Decimal("100.00")
        
        data = {
            "amount": 500.00,
            "payment_method": "bank_transfer"
        }
        
        # Act
        response = client.post(
            "/api/payouts/request",
            data=json.dumps(data),
            content_type="application/json",
            headers=auth_headers(trader_user)
        )
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_request_payout_missing_fields(self, client, trader_user, auth_headers):
        """Test payout request with missing required fields"""
        # Arrange
        data = {
            "amount": 500.00
            # Missing payment_method
        }
        
        # Act
        response = client.post(
            "/api/payouts/request",
            data=json.dumps(data),
            content_type="application/json",
            headers=auth_headers(trader_user)
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_request_payout_unauthorized(self, client):
        """Test payout request without authentication"""
        # Arrange
        data = {
            "amount": 500.00,
            "payment_method": "bank_transfer"
        }
        
        # Act
        response = client.post(
            "/api/payouts/request",
            data=json.dumps(data),
            content_type="application/json"
        )
        
        # Assert
        assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.api
class TestPayoutListAPI:
    """Test payout list endpoint"""
    
    def test_list_payouts_trader(self, client, trader_user, auth_headers):
        """Test trader can see their own payouts"""
        # Act
        response = client.get(
            "/api/payouts",
            headers=auth_headers(trader_user)
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "payouts" in data
        assert isinstance(data["payouts"], list)
    
    def test_list_payouts_admin(self, client, admin_user, auth_headers):
        """Test admin can see all payouts"""
        # Act
        response = client.get(
            "/api/payouts",
            headers=auth_headers(admin_user)
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "payouts" in data
    
    def test_list_payouts_with_filters(self, client, trader_user, auth_headers):
        """Test payout list with status filter"""
        # Act
        response = client.get(
            "/api/payouts?status=pending",
            headers=auth_headers(trader_user)
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "payouts" in data
        # All returned payouts should be pending
        for payout in data["payouts"]:
            assert payout["status"] == "pending"
    
    def test_list_payouts_unauthorized(self, client):
        """Test payout list without authentication"""
        # Act
        response = client.get("/api/payouts")
        
        # Assert
        assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.api
class TestPayoutDetailAPI:
    """Test payout detail endpoint"""
    
    def test_get_payout_detail_owner(self, client, trader_user, payout_request, auth_headers):
        """Test trader can see their own payout details"""
        # Act
        response = client.get(
            f"/api/payouts/{payout_request.id}",
            headers=auth_headers(trader_user)
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == payout_request.id
        assert data["amount"] == float(payout_request.amount)
    
    def test_get_payout_detail_admin(self, client, admin_user, payout_request, auth_headers):
        """Test admin can see any payout"""
        # Act
        response = client.get(
            f"/api/payouts/{payout_request.id}",
            headers=auth_headers(admin_user)
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_get_payout_not_found(self, client, trader_user, auth_headers):
        """Test getting non-existent payout"""
        # Act
        response = client.get(
            "/api/payouts/99999",
            headers=auth_headers(trader_user)
        )
        
        # Assert
        assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.admin
class TestPayoutStatusUpdateAPI:
    """Test payout status update endpoint (admin only)"""
    
    def test_approve_payout_admin(self, client, admin_user, payout_request, auth_headers):
        """Test admin can approve payout"""
        # Arrange
        data = {
            "status": "approved",
            "admin_notes": "Approved for processing"
        }
        
        # Act
        response = client.post(
            f"/api/payouts/admin/{payout_request.id}/approve",
            data=json.dumps({"notes": data.get("notes")}),
            content_type="application/json",
            headers=auth_headers(admin_user)
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "payout" in data
        assert data["payout"]["status"] == "approved"
    
    def test_reject_payout_admin(self, client, admin_user, payout_request, auth_headers):
        """Test admin can reject payout"""
        # Arrange
        data = {
            "status": "rejected",
            "admin_notes": "Insufficient documentation"
        }
        
        # Act
        response = client.post(
            f"/api/payouts/admin/{payout_request.id}/reject",
            json={"reason": data.get("admin_notes", "Insufficient documentation")},
            headers=auth_headers(admin_user)
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "payout" in data
        assert data["payout"]["status"] == "rejected"
    
    def test_update_status_trader_forbidden(self, client, trader_user, payout_request, auth_headers):
        """Test trader cannot approve payout (admin only)"""
        # Act
        response = client.post(
            f"/api/payouts/admin/{payout_request.id}/approve",
            json={"notes": "Trying to approve"},
            headers=auth_headers(trader_user)
        )
        
        # Assert
        assert response.status_code == 403
    
    def test_update_status_invalid_transition(self, client, admin_user, payout_request, auth_headers, session):
        """Test invalid status transition (cannot approve already approved payout)"""
        # Arrange - approve the payout first
        payout_request.status = "approved"
        session.flush()
        
        # Act - try to approve again
        response = client.post(
            f"/api/payouts/admin/{payout_request.id}/approve",
            json={"notes": "Trying to approve again"},
            headers=auth_headers(admin_user)
        )
        
        # Assert - should fail with 400
        assert response.status_code == 400

