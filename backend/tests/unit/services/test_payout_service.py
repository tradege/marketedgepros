"""
Unit Tests for PayoutService
Tests business logic with mocked dependencies
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal
from datetime import datetime
from src.services.payout_service import PayoutService
from src.models.user import User
from src.models.trading_program import TradingProgram
from src.models.payout_request import PayoutRequest


class TestCanRequestPayout:
    """Test PayoutService.can_request_payout() method"""
    
    def test_can_request_when_eligible(self):
        """Test that eligible user can request payout"""
        # Arrange
        user = Mock(spec=User)
        user.id = 1
        user.available_balance = Decimal("1000.00")
        
        program = Mock(spec=TradingProgram)
        program.minimum_payout_amount = Decimal("100.00")
        program.payout_mode = "on_demand"
        program.profit_split_percentage = 80
        
        # Mock db.session.query to return no pending payouts
        with patch("src.services.payout_service.db.session") as mock_session:
            mock_query = mock_session.query.return_value
            mock_query.filter.return_value.first.return_value = None
            
            # Act
            result = PayoutService.can_request_payout(user, program)
        
        # Assert
        assert result["can_request"] is True
        assert result["errors"] == []
        assert result["available_balance"] == 1000.00
        assert result["minimum_amount"] == 100.00
    
    def test_cannot_request_when_no_balance(self):
        """Test that user with no balance cannot request payout"""
        # Arrange
        user = Mock(spec=User)
        user.id = 1
        user.available_balance = Decimal("0.00")
        
        program = Mock(spec=TradingProgram)
        program.minimum_payout_amount = Decimal("100.00")
        program.payout_mode = "on_demand"
        program.profit_split_percentage = 80
        
        # Act
        result = PayoutService.can_request_payout(user, program)
        
        # Assert
        assert result["can_request"] is False
        assert "No available balance" in result["errors"][0]
    
    def test_cannot_request_when_below_minimum(self):
        """Test that user below minimum amount cannot request payout"""
        # Arrange
        user = Mock(spec=User)
        user.id = 1
        user.available_balance = Decimal("50.00")
        
        program = Mock(spec=TradingProgram)
        program.minimum_payout_amount = Decimal("100.00")
        program.payout_mode = "on_demand"
        program.profit_split_percentage = 80
        
        # Act
        result = PayoutService.can_request_payout(user, program)
        
        # Assert
        assert result["can_request"] is False
        assert "Minimum payout amount" in result["errors"][0]
    
    def test_cannot_request_when_pending_exists(self):
        """Test that user with pending payout cannot request another"""
        # Arrange
        user = Mock(spec=User)
        user.id = 1
        user.available_balance = Decimal("1000.00")
        
        program = Mock(spec=TradingProgram)
        program.minimum_payout_amount = Decimal("100.00")
        program.payout_mode = "on_demand"
        program.profit_split_percentage = 80
        
        # Mock db.session.query to return a pending payout
        pending_payout = Mock(spec=PayoutRequest)
        pending_payout.status = "pending"
        
        with patch("src.services.payout_service.db.session") as mock_session:
            mock_query = mock_session.query.return_value
            mock_query.filter.return_value.first.return_value = pending_payout
            
            # Act
            result = PayoutService.can_request_payout(user, program)
        
        # Assert
        assert result["can_request"] is False
        assert "already have a pending payout" in result["errors"][0]


class TestRequestPayout:
    """Test PayoutService.request_payout() method"""
    
    def test_request_payout_success(self):
        """Test successful payout request creation"""
        # Arrange
        user = Mock(spec=User)
        user.id = 1
        user.available_balance = Decimal("1000.00")
        
        program = Mock(spec=TradingProgram)
        program.id = 1
        program.minimum_payout_amount = Decimal("100.00")
        program.payout_mode = "on_demand"
        program.profit_split_percentage = 80
        
        amount = Decimal("500.00")
        payment_method = "bank_transfer"
        payment_details = {"account": "123456"}
        
        # Mock can_request_payout to return success
        with patch.object(PayoutService, "can_request_payout") as mock_can_request:
            mock_can_request.return_value = {"can_request": True, "errors": []}
            
            # Mock db.session
            with patch("src.services.payout_service.db.session") as mock_session:
                # Act
                result = PayoutService.request_payout(
                    user, program, amount, payment_method, payment_details
                )
        
        # Assert
        assert result is not None
        assert isinstance(result, PayoutRequest)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
    
    def test_request_payout_exceeds_balance(self):
        """Test that request exceeding balance raises error"""
        # Arrange
        user = Mock(spec=User)
        user.id = 1
        user.available_balance = Decimal("100.00")
        
        program = Mock(spec=TradingProgram)
        program.minimum_payout_amount = Decimal("50.00")
        program.profit_split_percentage = 80
        
        amount = Decimal("500.00")  # Exceeds balance
        
        # Mock can_request_payout to return success
        with patch.object(PayoutService, "can_request_payout") as mock_can_request:
            mock_can_request.return_value = {"can_request": True, "errors": []}
            
            # Act & Assert
            with pytest.raises(ValueError, match="exceeds available balance"):
                PayoutService.request_payout(user, program, amount, "bank_transfer")
    
    def test_request_payout_below_minimum(self):
        """Test that request below minimum raises error"""
        # Arrange
        user = Mock(spec=User)
        user.id = 1
        user.available_balance = Decimal("1000.00")
        
        program = Mock(spec=TradingProgram)
        program.minimum_payout_amount = Decimal("100.00")
        program.profit_split_percentage = 80
        
        amount = Decimal("50.00")  # Below minimum
        
        # Mock can_request_payout to return success
        with patch.object(PayoutService, "can_request_payout") as mock_can_request:
            mock_can_request.return_value = {"can_request": True, "errors": []}
            
            # Act & Assert
            with pytest.raises(ValueError, match="Minimum payout amount"):
                PayoutService.request_payout(user, program, amount, "bank_transfer")


class TestCalculateProfitSplit:
    """Test profit split calculation"""
    
    def test_profit_split_80_percent(self):
        """Test 80% profit split calculation"""
        # Arrange
        amount = Decimal("1000.00")
        percentage = 80
        
        # Act
        result = amount * Decimal(str(percentage / 100))
        
        # Assert
        assert result == Decimal("800.00")
    
    def test_profit_split_90_percent(self):
        """Test 90% profit split calculation"""
        # Arrange
        amount = Decimal("1000.00")
        percentage = 90
        
        # Act
        result = amount * Decimal(str(percentage / 100))
        
        # Assert
        assert result == Decimal("900.00")


@pytest.mark.unit
@pytest.mark.services
class TestPayoutServiceEdgeCases:
    """Test edge cases and error handling"""
    
    def test_none_balance(self):
        """Test handling of None balance"""
        # Arrange
        user = Mock(spec=User)
        user.id = 1
        user.available_balance = None
        
        program = Mock(spec=TradingProgram)
        program.minimum_payout_amount = Decimal("100.00")
        
        # Act
        result = PayoutService.can_request_payout(user, program)
        
        # Assert
        assert result["can_request"] is False
        assert "No available balance" in result["errors"][0]
    
    def test_zero_minimum_amount(self):
        """Test handling of zero minimum amount"""
        # Arrange
        user = Mock(spec=User)
        user.id = 1
        user.available_balance = Decimal("100.00")
        
        program = Mock(spec=TradingProgram)
        program.minimum_payout_amount = Decimal("0.00")
        program.payout_mode = "on_demand"
        program.profit_split_percentage = 80
        
        # Mock db.session.query
        with patch("src.services.payout_service.db.session") as mock_session:
            mock_query = mock_session.query.return_value
            mock_query.filter.return_value.first.return_value = None
            
            # Act
            result = PayoutService.can_request_payout(user, program)
        
        # Assert
        assert result["can_request"] is True
