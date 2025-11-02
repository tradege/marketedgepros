"""
Unit tests for Wallet Service
Tests wallet creation, balance management, transactions, and transfers
"""
import pytest
from decimal import Decimal
from src.services.wallet_service import WalletService
from src.models import Wallet, Transaction, User


@pytest.fixture
def mock_user(session):
    """Create a mock user"""
    user = User(
        email='user@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('password123')
    session.add(user)
    session.flush()
    return user


@pytest.fixture
def mock_user2(session):
    """Create a second mock user for transfers"""
    user = User(
        email='user2@example.com',
        first_name='Test2',
        last_name='User2'
    )
    user.set_password('password123')
    session.add(user)
    session.flush()
    return user


class TestWalletCreation:
    """Test wallet creation and retrieval"""
    
    def test_create_wallet_for_new_user(self, session, mock_user):
        """Test creating wallet for user who doesn't have one"""
        # Act
        wallet = WalletService.get_or_create_wallet(mock_user.id)
        
        # Assert
        assert wallet is not None
        assert wallet.user_id == mock_user.id
        assert wallet.main_balance == Decimal('0')
        assert wallet.commission_balance == Decimal('0')
        assert wallet.bonus_balance == Decimal('0')
    
    def test_get_existing_wallet(self, session, mock_user):
        """Test retrieving existing wallet"""
        # Arrange
        wallet1 = WalletService.get_or_create_wallet(mock_user.id)
        wallet1_id = wallet1.id
        
        # Act
        wallet2 = WalletService.get_or_create_wallet(mock_user.id)
        
        # Assert
        assert wallet2.id == wallet1_id  # Same wallet returned
    
    def test_wallet_created_only_once(self, session, mock_user):
        """Test that multiple calls don't create duplicate wallets"""
        # Act
        wallet1 = WalletService.get_or_create_wallet(mock_user.id)
        wallet2 = WalletService.get_or_create_wallet(mock_user.id)
        wallet3 = WalletService.get_or_create_wallet(mock_user.id)
        
        # Assert
        assert wallet1.id == wallet2.id == wallet3.id
        
        # Verify only one wallet exists
        wallet_count = Wallet.query.filter_by(user_id=mock_user.id).count()
        assert wallet_count == 1


class TestBalanceRetrieval:
    """Test balance retrieval"""
    
    def test_get_main_balance(self, session, mock_user):
        """Test getting main balance"""
        # Arrange
        wallet = WalletService.get_or_create_wallet(mock_user.id)
        wallet.main_balance = Decimal('100.50')
        session.commit()
        
        # Act
        balance = WalletService.get_balance(mock_user.id, 'main')
        
        # Assert
        assert balance == 100.50
    
    def test_get_commission_balance(self, session, mock_user):
        """Test getting commission balance"""
        # Arrange
        wallet = WalletService.get_or_create_wallet(mock_user.id)
        wallet.commission_balance = Decimal('50.25')
        session.commit()
        
        # Act
        balance = WalletService.get_balance(mock_user.id, 'commission')
        
        # Assert
        assert balance == 50.25
    
    def test_get_bonus_balance(self, session, mock_user):
        """Test getting bonus balance"""
        # Arrange
        wallet = WalletService.get_or_create_wallet(mock_user.id)
        wallet.bonus_balance = Decimal('25.75')
        session.commit()
        
        # Act
        balance = WalletService.get_balance(mock_user.id, 'bonus')
        
        # Assert
        assert balance == 25.75
    
    def test_get_total_balance(self, session, mock_user):
        """Test getting total balance (main + commission only)"""
        # Arrange
        wallet = WalletService.get_or_create_wallet(mock_user.id)
        wallet.main_balance = Decimal('100.00')
        wallet.commission_balance = Decimal('50.00')
        wallet.bonus_balance = Decimal('25.00')
        session.commit()
        
        # Act
        balance = WalletService.get_balance(mock_user.id, 'total')
        
        # Assert
        # Note: total_balance in Wallet model = main + commission (bonus not included)
        assert balance == 150.00
    
    def test_get_balance_creates_wallet_if_not_exists(self, session, mock_user):
        """Test that get_balance creates wallet if it doesn't exist"""
        # Act
        balance = WalletService.get_balance(mock_user.id, 'main')
        
        # Assert
        assert balance == 0.0
        wallet = Wallet.query.filter_by(user_id=mock_user.id).first()
        assert wallet is not None


class TestAddFunds:
    """Test adding funds to wallet"""
    
    def test_add_funds_to_main_balance(self, session, mock_user):
        """Test adding funds to main balance"""
        # Act
        wallet, transaction = WalletService.add_funds(
            mock_user.id,
            100.50,
            balance_type='main',
            description='Test deposit'
        )
        
        # Assert
        assert wallet.main_balance == Decimal('100.50')
        assert transaction.type == 'deposit'
        assert transaction.amount == Decimal('100.50')
        assert transaction.balance_type == 'main'
        assert transaction.balance_before == Decimal('0')
        assert transaction.balance_after == Decimal('100.50')
        assert transaction.description == 'Test deposit'
    
    def test_add_funds_to_commission_balance(self, session, mock_user):
        """Test adding funds to commission balance"""
        # Act
        wallet, transaction = WalletService.add_funds(
            mock_user.id,
            50.25,
            balance_type='commission'
        )
        
        # Assert
        assert wallet.commission_balance == Decimal('50.25')
        assert transaction.balance_type == 'commission'
    
    def test_add_funds_to_bonus_balance(self, session, mock_user):
        """Test adding funds to bonus balance"""
        # Act
        wallet, transaction = WalletService.add_funds(
            mock_user.id,
            25.75,
            balance_type='bonus'
        )
        
        # Assert
        assert wallet.bonus_balance == Decimal('25.75')
        assert transaction.balance_type == 'bonus'
    
    def test_add_funds_multiple_times(self, session, mock_user):
        """Test adding funds multiple times accumulates"""
        # Act
        WalletService.add_funds(mock_user.id, 100.00, 'main')
        WalletService.add_funds(mock_user.id, 50.00, 'main')
        wallet, _ = WalletService.add_funds(mock_user.id, 25.00, 'main')
        
        # Assert
        assert wallet.main_balance == Decimal('175.00')
    
    def test_add_funds_negative_amount(self, session, mock_user):
        """Test that negative amounts are rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Amount must be positive"):
            WalletService.add_funds(mock_user.id, -50.00, 'main')
    
    def test_add_funds_zero_amount(self, session, mock_user):
        """Test that zero amounts are rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Amount must be positive"):
            WalletService.add_funds(mock_user.id, 0, 'main')
    
    def test_add_funds_invalid_balance_type(self, session, mock_user):
        """Test that invalid balance type is rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid balance type"):
            WalletService.add_funds(mock_user.id, 100.00, 'invalid')
    
    def test_add_funds_with_reference(self, session, mock_user):
        """Test adding funds with reference"""
        # Act
        wallet, transaction = WalletService.add_funds(
            mock_user.id,
            100.00,
            'main',
            reference_type='payment',
            reference_id=123
        )
        
        # Assert
        assert transaction.reference_type == 'payment'
        assert transaction.reference_id == 123
    
    def test_add_funds_updates_last_transaction_time(self, session, mock_user):
        """Test that last_transaction_at is updated"""
        # Arrange
        wallet = WalletService.get_or_create_wallet(mock_user.id)
        initial_time = wallet.last_transaction_at
        
        # Act
        WalletService.add_funds(mock_user.id, 100.00, 'main')
        
        # Assert
        session.refresh(wallet)
        assert wallet.last_transaction_at is not None
        assert wallet.last_transaction_at != initial_time


class TestDeductFunds:
    """Test deducting funds from wallet"""
    
    def test_deduct_funds_from_main_balance(self, session, mock_user):
        """Test deducting funds from main balance"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'main')
        
        # Act
        wallet, transaction = WalletService.deduct_funds(
            mock_user.id,
            50.00,
            balance_type='main',
            description='Test withdrawal'
        )
        
        # Assert
        assert wallet.main_balance == Decimal('50.00')
        assert transaction.type == 'withdrawal'
        assert transaction.amount == Decimal('50.00')
        assert transaction.balance_type == 'main'
        assert transaction.balance_before == Decimal('100.00')
        assert transaction.balance_after == Decimal('50.00')
    
    def test_deduct_funds_insufficient_balance(self, session, mock_user):
        """Test that deducting more than balance fails"""
        # Arrange
        WalletService.add_funds(mock_user.id, 50.00, 'main')
        
        # Act & Assert
        with pytest.raises(ValueError, match="Insufficient main balance"):
            WalletService.deduct_funds(mock_user.id, 100.00, 'main')
    
    def test_deduct_funds_from_commission_balance(self, session, mock_user):
        """Test deducting from commission balance"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'commission')
        
        # Act
        wallet, _ = WalletService.deduct_funds(mock_user.id, 30.00, 'commission')
        
        # Assert
        assert wallet.commission_balance == Decimal('70.00')
    
    def test_deduct_funds_from_bonus_balance(self, session, mock_user):
        """Test deducting from bonus balance"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'bonus')
        
        # Act
        wallet, _ = WalletService.deduct_funds(mock_user.id, 40.00, 'bonus')
        
        # Assert
        assert wallet.bonus_balance == Decimal('60.00')
    
    def test_deduct_funds_negative_amount(self, session, mock_user):
        """Test that negative amounts are rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Amount must be positive"):
            WalletService.deduct_funds(mock_user.id, -50.00, 'main')
    
    def test_deduct_funds_invalid_balance_type(self, session, mock_user):
        """Test that invalid balance type is rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid balance type"):
            WalletService.deduct_funds(mock_user.id, 50.00, 'invalid')


class TestTransferFunds:
    """Test transferring funds between wallets"""
    
    def test_transfer_funds_success(self, session, mock_user, mock_user2):
        """Test successful fund transfer"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'main')
        
        # Act
        result = WalletService.transfer_funds(
            mock_user.id,
            mock_user2.id,
            50.00,
            'main',
            description='Test transfer'
        )
        
        # Assert
        assert result is True
        
        # Check sender balance
        sender_balance = WalletService.get_balance(mock_user.id, 'main')
        assert sender_balance == 50.00
        
        # Check recipient balance
        recipient_balance = WalletService.get_balance(mock_user2.id, 'main')
        assert recipient_balance == 50.00
    
    def test_transfer_funds_insufficient_balance(self, session, mock_user, mock_user2):
        """Test transfer with insufficient balance"""
        # Arrange
        WalletService.add_funds(mock_user.id, 50.00, 'main')
        
        # Act & Assert
        with pytest.raises(ValueError, match="Insufficient main balance"):
            WalletService.transfer_funds(mock_user.id, mock_user2.id, 100.00, 'main')
    
    def test_transfer_funds_negative_amount(self, session, mock_user, mock_user2):
        """Test that negative transfer amounts are rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Amount must be positive"):
            WalletService.transfer_funds(mock_user.id, mock_user2.id, -50.00, 'main')
    
    def test_transfer_funds_creates_two_transactions(self, session, mock_user, mock_user2):
        """Test that transfer creates transactions for both users"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'main')
        
        # Act
        WalletService.transfer_funds(mock_user.id, mock_user2.id, 50.00, 'main')
        
        # Assert
        sender_transactions = WalletService.get_transaction_history(mock_user.id)
        recipient_transactions = WalletService.get_transaction_history(mock_user2.id)
        
        assert len(sender_transactions) == 2  # deposit + withdrawal
        assert len(recipient_transactions) == 1  # deposit
        
        # Check sender's withdrawal
        sender_withdrawal = [t for t in sender_transactions if t.type == 'withdrawal'][0]
        assert sender_withdrawal.amount == Decimal('50.00')
        assert f"Transfer to user {mock_user2.id}" in sender_withdrawal.description
        
        # Check recipient's deposit
        assert recipient_transactions[0].type == 'deposit'
        assert recipient_transactions[0].amount == Decimal('50.00')
        assert f"Transfer from user {mock_user.id}" in recipient_transactions[0].description


class TestTransactionHistory:
    """Test transaction history retrieval"""
    
    def test_get_transaction_history(self, session, mock_user):
        """Test getting transaction history"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'main')
        WalletService.add_funds(mock_user.id, 50.00, 'commission')
        WalletService.deduct_funds(mock_user.id, 25.00, 'main')
        
        # Act
        transactions = WalletService.get_transaction_history(mock_user.id)
        
        # Assert
        assert len(transactions) == 3
    
    def test_get_transaction_history_by_balance_type(self, session, mock_user):
        """Test filtering transactions by balance type"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'main')
        WalletService.add_funds(mock_user.id, 50.00, 'commission')
        WalletService.add_funds(mock_user.id, 25.00, 'main')
        
        # Act
        main_transactions = WalletService.get_transaction_history(
            mock_user.id,
            balance_type='main'
        )
        commission_transactions = WalletService.get_transaction_history(
            mock_user.id,
            balance_type='commission'
        )
        
        # Assert
        assert len(main_transactions) == 2
        assert len(commission_transactions) == 1
    
    def test_get_transaction_history_with_limit(self, session, mock_user):
        """Test limiting transaction history"""
        # Arrange
        for i in range(10):
            WalletService.add_funds(mock_user.id, 10.00, 'main')
        
        # Act
        transactions = WalletService.get_transaction_history(mock_user.id, limit=5)
        
        # Assert
        assert len(transactions) == 5
    
    def test_get_transaction_history_with_offset(self, session, mock_user):
        """Test offset in transaction history"""
        # Arrange
        for i in range(10):
            WalletService.add_funds(mock_user.id, 10.00, 'main')
        
        # Act
        page1 = WalletService.get_transaction_history(mock_user.id, limit=5, offset=0)
        page2 = WalletService.get_transaction_history(mock_user.id, limit=5, offset=5)
        
        # Assert
        assert len(page1) == 5
        assert len(page2) == 5
        assert page1[0].id != page2[0].id  # Different transactions
    
    def test_get_transaction_history_ordered_by_date(self, session, mock_user):
        """Test that transactions are ordered by date descending"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'main', description='First')
        WalletService.add_funds(mock_user.id, 200.00, 'main', description='Second')
        WalletService.add_funds(mock_user.id, 300.00, 'main', description='Third')
        
        # Act
        transactions = WalletService.get_transaction_history(mock_user.id)
        
        # Assert
        assert transactions[0].description == 'Third'  # Most recent first
        assert transactions[1].description == 'Second'
        assert transactions[2].description == 'First'


class TestBalanceAdjustment:
    """Test manual balance adjustments"""
    
    def test_adjust_balance_positive(self, session, mock_user):
        """Test positive balance adjustment"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'main')
        
        # Act
        wallet, transaction = WalletService.adjust_balance(
            mock_user.id,
            50.00,
            'main',
            description='Admin adjustment',
            created_by=mock_user.id
        )
        
        # Assert
        assert wallet.main_balance == Decimal('150.00')
        assert transaction.type == 'adjustment'
        assert transaction.amount == Decimal('50.00')
        assert transaction.balance_before == Decimal('100.00')
        assert transaction.balance_after == Decimal('150.00')
        assert transaction.created_by == mock_user.id
    
    def test_adjust_balance_negative(self, session, mock_user):
        """Test negative balance adjustment"""
        # Arrange
        WalletService.add_funds(mock_user.id, 100.00, 'main')
        
        # Act
        wallet, transaction = WalletService.adjust_balance(
            mock_user.id,
            -30.00,
            'main',
            description='Correction'
        )
        
        # Assert
        assert wallet.main_balance == Decimal('70.00')
        assert transaction.amount == Decimal('30.00')  # Stored as absolute value
        assert transaction.balance_after == Decimal('70.00')
    
    def test_adjust_balance_commission(self, session, mock_user):
        """Test adjusting commission balance"""
        # Act
        wallet, _ = WalletService.adjust_balance(
            mock_user.id,
            100.00,
            'commission'
        )
        
        # Assert
        assert wallet.commission_balance == Decimal('100.00')
    
    def test_adjust_balance_bonus(self, session, mock_user):
        """Test adjusting bonus balance"""
        # Act
        wallet, _ = WalletService.adjust_balance(
            mock_user.id,
            50.00,
            'bonus'
        )
        
        # Assert
        assert wallet.bonus_balance == Decimal('50.00')
    
    def test_adjust_balance_invalid_type(self, session, mock_user):
        """Test that invalid balance type is rejected"""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid balance type"):
            WalletService.adjust_balance(mock_user.id, 100.00, 'invalid')
    
    def test_adjust_balance_can_go_negative(self, session, mock_user):
        """Test that adjustment can make balance negative (admin override)"""
        # Arrange
        WalletService.add_funds(mock_user.id, 50.00, 'main')
        
        # Act
        wallet, _ = WalletService.adjust_balance(mock_user.id, -100.00, 'main')
        
        # Assert
        assert wallet.main_balance == Decimal('-50.00')
