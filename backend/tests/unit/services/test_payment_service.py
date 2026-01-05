"""
Unit tests for Payment Service
Tests Stripe payment integration including payment intents, customers, refunds, and webhooks
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import stripe
from src.services.payment_service import PaymentService
from src.models import Challenge, User, TradingProgram


@pytest.fixture
def mock_stripe_key(app):
    """Mock Stripe API key configuration"""
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_mock123'
    app.config['STRIPE_WEBHOOK_SECRET'] = 'whsec_mock123'
    return app


@pytest.fixture
def mock_user(session):
    """Create a mock user for testing"""
    user = User(
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('password123')
    user.id = 1
    user.stripe_customer_id = None
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def mock_program(session):
    """Create a mock trading program"""
    from src.models import Tenant
    
    # Create tenant first
    tenant = Tenant(
        name='Test Tenant',
        subdomain=f'test_{__import__('uuid').uuid4().hex[:8]}'
    )
    session.add(tenant)
    session.flush()
    
    program = TradingProgram(
        name='Test Program',
        type='one_phase',
        account_size=10000.00,
        price=100.00,
        tenant_id=tenant.id
    )
    program.id = 1
    
    # Mock calculate_total_price method
    def calculate_total_price(addons=None):
        return 100.00
    
    program.calculate_total_price = calculate_total_price
    session.add(program)
    session.commit()
    return program


@pytest.fixture
def mock_challenge(session, mock_user, mock_program):
    """Create a mock challenge"""
    challenge = Challenge(
        user_id=mock_user.id,
        program_id=mock_program.id,
        status='pending',
        payment_status='pending'
    )
    challenge.id = 1
    challenge.addons = []
    challenge.program = mock_program
    session.add(challenge)
    session.commit()
    return challenge


class TestPaymentServiceStripeKey:
    """Test Stripe API key configuration"""
    
    def test_get_stripe_key_success(self, mock_stripe_key):
        """Test successful retrieval of Stripe API key"""
        # Act
        key = PaymentService._get_stripe_key()
        
        # Assert
        assert key == 'sk_test_mock123'
        assert stripe.api_key == 'sk_test_mock123'
    
    def test_get_stripe_key_missing(self, app):
        """Test handling of missing Stripe API key"""
        # Arrange
        app.config['STRIPE_SECRET_KEY'] = None
        
        # Act
        key = PaymentService._get_stripe_key()
        
        # Assert
        assert key is None


class TestPaymentServiceCustomer:
    """Test Stripe customer management"""
    
    @patch('stripe.Customer.create')
    def test_create_new_customer_success(self, mock_create, mock_stripe_key, mock_user, session):
        """Test successful creation of new Stripe customer"""
        # Arrange
        mock_create.return_value = Mock(id='cus_test123')
        
        # Act
        customer_id = PaymentService._get_or_create_customer(mock_user)
        
        # Assert
        assert customer_id == 'cus_test123'
        mock_create.assert_called_once_with(
            email='test@example.com',
            name='Test User',
            metadata={'user_id': 1}
        )
        # Verify customer ID was stored
        session.refresh(mock_user)
        assert mock_user.stripe_customer_id == 'cus_test123'
    
    @patch('stripe.Customer.retrieve')
    def test_get_existing_customer_success(self, mock_retrieve, mock_stripe_key, mock_user):
        """Test retrieving existing Stripe customer"""
        # Arrange
        mock_user.stripe_customer_id = 'cus_existing123'
        mock_retrieve.return_value = Mock(id='cus_existing123')
        
        # Act
        customer_id = PaymentService._get_or_create_customer(mock_user)
        
        # Assert
        assert customer_id == 'cus_existing123'
        mock_retrieve.assert_called_once_with('cus_existing123')
    
    @patch('stripe.Customer.retrieve')
    @patch('stripe.Customer.create')
    def test_recreate_customer_if_not_found(self, mock_create, mock_retrieve, mock_stripe_key, mock_user):
        """Test recreating customer if stored ID is invalid"""
        # Arrange
        mock_user.stripe_customer_id = 'cus_invalid'
        mock_retrieve.side_effect = stripe.error.InvalidRequestError('No such customer', 'id')
        mock_create.return_value = Mock(id='cus_new123')
        
        # Act
        customer_id = PaymentService._get_or_create_customer(mock_user)
        
        # Assert
        assert customer_id == 'cus_new123'
        mock_create.assert_called_once()
    
    @patch('stripe.Customer.create')
    def test_create_customer_stripe_error(self, mock_create, mock_stripe_key, mock_user):
        """Test handling of Stripe error during customer creation"""
        # Arrange
        mock_create.side_effect = stripe.error.StripeError('API error')
        
        # Act
        customer_id = PaymentService._get_or_create_customer(mock_user)
        
        # Assert
        assert customer_id is None


class TestPaymentServicePaymentIntent:
    """Test payment intent creation"""
    
    @patch('stripe.PaymentIntent.create')
    @patch('stripe.Customer.create')
    def test_create_payment_intent_success(self, mock_customer, mock_intent, mock_stripe_key, mock_challenge, mock_user, session):
        """Test successful payment intent creation"""
        # Arrange
        mock_customer.return_value = Mock(id='cus_test123')
        mock_intent.return_value = Mock(
            id='pi_test123',
            client_secret='secret_test123',
            amount=10000,
            currency='usd'
        )
        
        # Act
        result = PaymentService.create_payment_intent(mock_challenge, mock_user)
        
        # Assert
        assert result['payment_intent_id'] == 'pi_test123'
        assert result['client_secret'] == 'secret_test123'
        assert result['amount'] == 100.00
        assert result['currency'] == 'usd'
        
        # Verify payment intent was created with correct parameters
        mock_intent.assert_called_once()
        call_args = mock_intent.call_args[1]
        assert call_args['amount'] == 10000  # $100 in cents
        assert call_args['currency'] == 'usd'
        assert call_args['metadata']['challenge_id'] == 1
        assert call_args['metadata']['user_id'] == 1
        assert call_args['receipt_email'] == 'test@example.com'
        
        # Verify payment_id was stored in challenge
        session.refresh(mock_challenge)
        assert mock_challenge.payment_id == 'pi_test123'
    
    def test_create_payment_intent_no_stripe_key(self, app, mock_challenge, mock_user):
        """Test payment intent creation without Stripe key"""
        # Arrange
        app.config['STRIPE_SECRET_KEY'] = None
        
        # Act & Assert
        with pytest.raises(ValueError, match='Payment system not configured'):
            PaymentService.create_payment_intent(mock_challenge, mock_user)
    
    @patch('stripe.PaymentIntent.create')
    @patch('stripe.Customer.create')
    def test_create_payment_intent_stripe_error(self, mock_customer, mock_intent, mock_stripe_key, mock_challenge, mock_user):
        """Test handling of Stripe error during payment intent creation"""
        # Arrange
        mock_customer.return_value = Mock(id='cus_test123')
        mock_intent.side_effect = stripe.error.CardError('Card declined', 'card', 'card_declined')
        
        # Act & Assert
        with pytest.raises(ValueError, match='Payment error'):
            PaymentService.create_payment_intent(mock_challenge, mock_user)
    
    @patch('stripe.PaymentIntent.create')
    @patch('stripe.Customer.create')
    def test_create_payment_intent_without_customer(self, mock_customer, mock_intent, mock_stripe_key, mock_challenge, mock_user):
        """Test payment intent creation when customer creation fails"""
        # Arrange
        mock_customer.side_effect = stripe.error.StripeError('Customer creation failed')
        mock_intent.return_value = Mock(
            id='pi_test123',
            client_secret='secret_test123',
            amount=10000,
            currency='usd'
        )
        
        # Act
        result = PaymentService.create_payment_intent(mock_challenge, mock_user)
        
        # Assert
        assert result['payment_intent_id'] == 'pi_test123'
        # Verify payment intent was created without customer ID
        call_args = mock_intent.call_args[1]
        assert 'customer' not in call_args


class TestPaymentServiceConfirmation:
    """Test payment confirmation"""
    
    @patch('src.services.payment_service.mt5_challenge_service.create_mt5_account_for_challenge')
    @patch('stripe.PaymentIntent.retrieve')
    def test_confirm_payment_succeeded(self, mock_retrieve, mock_mt5, mock_stripe_key, mock_challenge, session):
        """Test confirming a succeeded payment"""
        # Arrange
        mock_challenge.payment_id = 'pi_test123'
        session.commit()
        
        # Mock MT5 service to return proper async result
        async def mock_mt5_create():
            return {'mt5_login': '12345678', 'password': 'test123'}
        mock_mt5.return_value = mock_mt5_create()
        
        mock_retrieve.return_value = Mock(
            id='pi_test123',
            status='succeeded'
        )
        
        # Act
        result = PaymentService.confirm_payment('pi_test123')
        
        # Assert
        assert result['status'] == 'succeeded'
        assert result['confirmed'] is True
        
        # Verify challenge was updated
        session.refresh(mock_challenge)
        assert mock_challenge.payment_status == 'paid'
        assert mock_challenge.status == 'active'
    
    @patch('stripe.PaymentIntent.retrieve')
    def test_confirm_payment_requires_action(self, mock_retrieve, mock_stripe_key):
        """Test payment that requires additional action"""
        # Arrange
        mock_retrieve.return_value = Mock(
            id='pi_test123',
            status='requires_action',
            client_secret='secret_test123',
            next_action={'type': '3ds'}
        )
        
        # Act
        result = PaymentService.confirm_payment('pi_test123')
        
        # Assert
        assert result['status'] == 'requires_action'
        assert result['confirmed'] is False
        assert 'client_secret' in result
        assert 'next_action' in result
    
    @patch('stripe.PaymentIntent.retrieve')
    def test_confirm_payment_processing(self, mock_retrieve, mock_stripe_key):
        """Test payment that is still processing"""
        # Arrange
        mock_retrieve.return_value = Mock(
            id='pi_test123',
            status='processing'
        )
        
        # Act
        result = PaymentService.confirm_payment('pi_test123')
        
        # Assert
        assert result['status'] == 'processing'
        assert result['confirmed'] is False
    
    @patch('src.services.payment_service.mt5_challenge_service.create_mt5_account_for_challenge')
    @patch('stripe.PaymentIntent.retrieve')
    def test_confirm_payment_challenge_not_found(self, mock_retrieve, mock_mt5, mock_stripe_key):
        """Test confirming payment when challenge doesn't exist"""
        # Arrange
        # Mock MT5 service (won't be called since challenge not found)
        async def mock_mt5_create():
            return {'mt5_login': '12345678', 'password': 'test123'}
        mock_mt5.return_value = mock_mt5_create()
        
        mock_retrieve.return_value = Mock(
            id='pi_nonexistent',
            status='succeeded'
        )
        
        # Act
        result = PaymentService.confirm_payment('pi_nonexistent')
        
        # Assert
        assert result['status'] == 'error'
        assert 'Challenge not found' in result['message']
    
    def test_confirm_payment_no_stripe_key(self, app):
        """Test payment confirmation without Stripe key"""
        # Arrange
        app.config['STRIPE_SECRET_KEY'] = None
        
        # Act
        result = PaymentService.confirm_payment('pi_test123')
        
        # Assert
        assert result['status'] == 'error'
        assert 'not configured' in result['message']
    
    @patch('stripe.PaymentIntent.retrieve')
    def test_confirm_payment_stripe_error(self, mock_retrieve, mock_stripe_key):
        """Test handling of Stripe error during confirmation"""
        # Arrange
        mock_retrieve.side_effect = stripe.error.InvalidRequestError('Invalid payment intent', 'id')
        
        # Act
        result = PaymentService.confirm_payment('pi_invalid')
        
        # Assert
        assert result['status'] == 'error'


class TestPaymentServiceRefund:
    """Test payment refunds"""
    
    @patch('stripe.Refund.create')
    def test_refund_payment_success(self, mock_refund, mock_stripe_key, mock_challenge, session):
        """Test successful payment refund"""
        # Arrange
        mock_challenge.payment_id = 'pi_test123'
        session.commit()
        
        mock_refund.return_value = Mock(
            id='re_test123',
            amount=10000,
            status='succeeded'
        )
        
        # Act
        result = PaymentService.refund_payment(mock_challenge, reason='requested_by_customer')
        
        # Assert
        assert result['refund_id'] == 're_test123'
        assert result['amount'] == 100.00
        assert result['status'] == 'succeeded'
        
        # Verify refund was created with correct parameters
        mock_refund.assert_called_once_with(
            payment_intent='pi_test123',
            reason='requested_by_customer'
        )
        
        # Verify challenge was updated
        session.refresh(mock_challenge)
        assert mock_challenge.payment_status == 'refunded'
        assert mock_challenge.status == 'cancelled'
    
    @patch('stripe.Refund.create')
    def test_refund_payment_default_reason(self, mock_refund, mock_stripe_key, mock_challenge, session):
        """Test refund with default reason"""
        # Arrange
        mock_challenge.payment_id = 'pi_test123'
        session.commit()
        
        mock_refund.return_value = Mock(
            id='re_test123',
            amount=10000,
            status='succeeded'
        )
        
        # Act
        result = PaymentService.refund_payment(mock_challenge)
        
        # Assert
        call_args = mock_refund.call_args[1]
        assert call_args['reason'] == 'requested_by_customer'
    
    def test_refund_payment_no_payment_id(self, mock_stripe_key, mock_challenge):
        """Test refund when challenge has no payment ID"""
        # Arrange
        mock_challenge.payment_id = None
        
        # Act & Assert
        with pytest.raises(ValueError, match='No payment found'):
            PaymentService.refund_payment(mock_challenge)
    
    def test_refund_payment_no_stripe_key(self, app, mock_challenge):
        """Test refund without Stripe key"""
        # Arrange
        app.config['STRIPE_SECRET_KEY'] = None
        mock_challenge.payment_id = 'pi_test123'
        
        # Act & Assert
        with pytest.raises(ValueError, match='Payment system not configured'):
            PaymentService.refund_payment(mock_challenge)
    
    @patch('stripe.Refund.create')
    def test_refund_payment_stripe_error(self, mock_refund, mock_stripe_key, mock_challenge):
        """Test handling of Stripe error during refund"""
        # Arrange
        mock_challenge.payment_id = 'pi_test123'
        mock_refund.side_effect = stripe.error.InvalidRequestError('Charge already refunded', 'charge')
        
        # Act & Assert
        with pytest.raises(ValueError, match='Refund error'):
            PaymentService.refund_payment(mock_challenge)


class TestPaymentServiceWebhook:
    """Test Stripe webhook handling"""
    
    @patch('stripe.Webhook.construct_event')
    @patch('stripe.PaymentIntent.retrieve')
    def test_webhook_payment_succeeded(self, mock_retrieve, mock_construct, mock_stripe_key, mock_challenge, session):
        """Test webhook for successful payment"""
        # Arrange
        mock_challenge.payment_id = 'pi_test123'
        session.commit()
        
        mock_event = Mock(
            type='payment_intent.succeeded',
            data=Mock(object=Mock(id='pi_test123'))
        )
        mock_construct.return_value = mock_event
        mock_retrieve.return_value = Mock(id='pi_test123', status='succeeded')
        
        # Act
        result = PaymentService.handle_webhook('payload', 'sig_header')
        
        # Assert
        assert result is True
        mock_construct.assert_called_once_with('payload', 'sig_header', 'whsec_mock123')
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_payment_failed(self, mock_construct, mock_stripe_key, mock_challenge, session):
        """Test webhook for failed payment"""
        # Arrange
        mock_challenge.payment_id = 'pi_test123'
        session.commit()
        
        mock_event = Mock(
            type='payment_intent.payment_failed',
            data=Mock(object=Mock(id='pi_test123'))
        )
        mock_construct.return_value = mock_event
        
        # Act
        result = PaymentService.handle_webhook('payload', 'sig_header')
        
        # Assert
        assert result is True
        session.refresh(mock_challenge)
        assert mock_challenge.payment_status == 'failed'
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_charge_refunded(self, mock_construct, mock_stripe_key, mock_challenge, session):
        """Test webhook for refunded charge"""
        # Arrange
        mock_challenge.payment_id = 'pi_test123'
        session.commit()
        
        mock_event = Mock(
            type='charge.refunded',
            data=Mock(object=Mock(payment_intent='pi_test123'))
        )
        mock_construct.return_value = mock_event
        
        # Act
        result = PaymentService.handle_webhook('payload', 'sig_header')
        
        # Assert
        assert result is True
        session.refresh(mock_challenge)
        assert mock_challenge.payment_status == 'refunded'
        assert mock_challenge.status == 'cancelled'
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_signature_verification_error(self, mock_construct, mock_stripe_key):
        """Test webhook with invalid signature"""
        # Arrange
        mock_construct.side_effect = stripe.error.SignatureVerificationError('Invalid signature', 'sig_header')
        
        # Act
        result = PaymentService.handle_webhook('payload', 'invalid_sig')
        
        # Assert
        assert result is False
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_invalid_payload(self, mock_construct, mock_stripe_key):
        """Test webhook with invalid payload"""
        # Arrange
        mock_construct.side_effect = ValueError('Invalid payload')
        
        # Act
        result = PaymentService.handle_webhook('invalid_payload', 'sig_header')
        
        # Assert
        assert result is False
    
    def test_webhook_no_stripe_key(self, app):
        """Test webhook without Stripe key"""
        # Arrange
        app.config['STRIPE_SECRET_KEY'] = None
        
        # Act
        result = PaymentService.handle_webhook('payload', 'sig_header')
        
        # Assert
        assert result is False
    
    def test_webhook_no_webhook_secret(self, mock_stripe_key, app):
        """Test webhook without webhook secret"""
        # Arrange
        app.config['STRIPE_WEBHOOK_SECRET'] = None
        
        # Act
        result = PaymentService.handle_webhook('payload', 'sig_header')
        
        # Assert
        assert result is False


class TestPaymentServiceStatus:
    """Test payment status retrieval"""
    
    @patch('stripe.PaymentIntent.retrieve')
    def test_get_payment_status_success(self, mock_retrieve, mock_stripe_key):
        """Test successful payment status retrieval"""
        # Arrange
        mock_retrieve.return_value = Mock(
            status='succeeded',
            amount=10000,
            currency='usd',
            created=1234567890
        )
        
        # Act
        result = PaymentService.get_payment_status('pi_test123')
        
        # Assert
        assert result['status'] == 'succeeded'
        assert result['amount'] == 100.00
        assert result['currency'] == 'usd'
        assert result['created'] == 1234567890
    
    def test_get_payment_status_no_stripe_key(self, app):
        """Test payment status retrieval without Stripe key"""
        # Arrange
        app.config['STRIPE_SECRET_KEY'] = None
        
        # Act
        result = PaymentService.get_payment_status('pi_test123')
        
        # Assert
        assert result is None
    
    @patch('stripe.PaymentIntent.retrieve')
    def test_get_payment_status_error(self, mock_retrieve, mock_stripe_key):
        """Test handling of error during status retrieval"""
        # Arrange
        mock_retrieve.side_effect = stripe.error.InvalidRequestError('Invalid payment intent', 'id')
        
        # Act
        result = PaymentService.get_payment_status('pi_invalid')
        
        # Assert
        assert result is None
