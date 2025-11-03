"""
Comprehensive tests for NowPayments routes
Tests crypto payment creation, status checking, webhook handling, and currency listing
"""
import pytest
import json
from unittest.mock import patch, MagicMock
import uuid


class TestCreateCryptoPayment:
    """Tests for POST /api/crypto/create-payment endpoint"""
    
    @patch('src.routes.nowpayments.requests.post')
    def test_create_payment_success(self, mock_post, client):
        """Test successful payment creation"""
        # Mock successful NOWPayments response
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'payment_id': 'test_payment_123',
            'invoice_url': 'https://nowpayments.io/payment/test_payment_123',
            'pay_address': '0x1234567890abcdef',
            'pay_amount': 100.5,
            'pay_currency': 'usdttrc20',
            'order_id': 'order_program1_test@example.com'
        }
        mock_post.return_value = mock_response
        
        # Make request
        response = client.post('/api/crypto/create-payment', json={
            'program_id': 'program1',
            'amount': 100,
            'email': 'test@example.com'
        })
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['payment_id'] == 'test_payment_123'
        assert data['payment_url'] == 'https://nowpayments.io/payment/test_payment_123'
        assert data['pay_address'] == '0x1234567890abcdef'
        assert data['pay_amount'] == 100.5
        assert data['pay_currency'] == 'usdttrc20'
        
        # Verify NOWPayments API was called correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert 'https://api.nowpayments.io/v1/payment' in call_args[0][0]
        assert call_args[1]['json']['price_amount'] == 100.0
        assert call_args[1]['json']['price_currency'] == 'usd'
        assert call_args[1]['json']['pay_currency'] == 'usdttrc20'
    
    @patch('src.routes.nowpayments.requests.post')
    def test_create_payment_with_custom_order_id(self, mock_post, client):
        """Test payment creation with custom order ID"""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'payment_id': 'test_payment_456',
            'invoice_url': 'https://nowpayments.io/payment/test_payment_456',
            'pay_address': '0xabcdef1234567890',
            'pay_amount': 250.0,
            'pay_currency': 'usdttrc20',
            'order_id': 'custom_order_123'
        }
        mock_post.return_value = mock_response
        
        response = client.post('/api/crypto/create-payment', json={
            'program_id': 'program2',
            'amount': 250,
            'email': 'user@example.com',
            'order_id': 'custom_order_123'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['order_id'] == 'custom_order_123'
        
        # Verify custom order_id was used
        call_args = mock_post.call_args
        assert call_args[1]['json']['order_id'] == 'custom_order_123'
    
    def test_create_payment_missing_program_id(self, client):
        """Test payment creation without program_id"""
        response = client.post('/api/crypto/create-payment', json={
            'amount': 100,
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    def test_create_payment_missing_amount(self, client):
        """Test payment creation without amount"""
        response = client.post('/api/crypto/create-payment', json={
            'program_id': 'program1',
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    def test_create_payment_missing_email(self, client):
        """Test payment creation without email"""
        response = client.post('/api/crypto/create-payment', json={
            'program_id': 'program1',
            'amount': 100
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    def test_create_payment_missing_all_fields(self, client):
        """Test payment creation without any fields"""
        response = client.post('/api/crypto/create-payment', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    @patch('src.routes.nowpayments.requests.post')
    def test_create_payment_nowpayments_error(self, mock_post, client):
        """Test handling of NOWPayments API error"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = 'Invalid API key'
        mock_post.return_value = mock_response
        
        response = client.post('/api/crypto/create-payment', json={
            'program_id': 'program1',
            'amount': 100,
            'email': 'test@example.com'
        })
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Failed to create payment' in data['error']
    
    @patch('src.routes.nowpayments.requests.post')
    def test_create_payment_network_timeout(self, mock_post, client):
        """Test handling of network timeout"""
        mock_post.side_effect = Exception('Connection timeout')
        
        response = client.post('/api/crypto/create-payment', json={
            'program_id': 'program1',
            'amount': 100,
            'email': 'test@example.com'
        })
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
    
    @patch('src.routes.nowpayments.requests.post')
    def test_create_payment_large_amount(self, mock_post, client):
        """Test payment creation with large amount"""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'payment_id': 'test_payment_large',
            'invoice_url': 'https://nowpayments.io/payment/test_payment_large',
            'pay_address': '0xlarge',
            'pay_amount': 10000.0,
            'pay_currency': 'usdttrc20',
            'order_id': 'order_large'
        }
        mock_post.return_value = mock_response
        
        response = client.post('/api/crypto/create-payment', json={
            'program_id': 'premium_program',
            'amount': 10000,
            'email': 'premium@example.com'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        
        # Verify amount was passed correctly
        call_args = mock_post.call_args
        assert call_args[1]['json']['price_amount'] == 10000.0
    
    @patch('src.routes.nowpayments.requests.post')
    def test_create_payment_decimal_amount(self, mock_post, client):
        """Test payment creation with decimal amount"""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'payment_id': 'test_payment_decimal',
            'invoice_url': 'https://nowpayments.io/payment/test_payment_decimal',
            'pay_address': '0xdecimal',
            'pay_amount': 99.99,
            'pay_currency': 'usdttrc20',
            'order_id': 'order_decimal'
        }
        mock_post.return_value = mock_response
        
        response = client.post('/api/crypto/create-payment', json={
            'program_id': 'program1',
            'amount': 99.99,
            'email': 'test@example.com'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        
        # Verify decimal amount was handled correctly
        call_args = mock_post.call_args
        assert call_args[1]['json']['price_amount'] == 99.99
    
    def test_create_payment_no_json_body(self, client):
        """Test payment creation without JSON body"""
        response = client.post('/api/crypto/create-payment')
        
        # Should handle missing JSON gracefully
        assert response.status_code in [400, 500]


class TestGetPaymentStatus:
    """Tests for GET /api/crypto/payment-status/<payment_id> endpoint"""
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_payment_status_success(self, mock_get, client):
        """Test successful payment status retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'payment_status': 'finished',
            'pay_amount': 100.5,
            'actually_paid': 100.5,
            'outcome_amount': 100.0
        }
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/payment-status/test_payment_123')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['status'] == 'finished'
        assert data['pay_amount'] == 100.5
        assert data['actually_paid'] == 100.5
        assert data['outcome_amount'] == 100.0
        
        # Verify API was called correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert 'test_payment_123' in call_args[0][0]
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_payment_status_waiting(self, mock_get, client):
        """Test payment status when waiting for payment"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'payment_status': 'waiting',
            'pay_amount': 250.0,
            'actually_paid': 0,
            'outcome_amount': 0
        }
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/payment-status/waiting_payment')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'waiting'
        assert data['actually_paid'] == 0
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_payment_status_confirming(self, mock_get, client):
        """Test payment status when confirming"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'payment_status': 'confirming',
            'pay_amount': 100.0,
            'actually_paid': 100.0,
            'outcome_amount': 0
        }
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/payment-status/confirming_payment')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'confirming'
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_payment_status_not_found(self, mock_get, client):
        """Test payment status for non-existent payment"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/payment-status/nonexistent_payment')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'Payment not found' in data['error']
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_payment_status_network_error(self, mock_get, client):
        """Test handling of network error when getting status"""
        mock_get.side_effect = Exception('Network error')
        
        response = client.get('/api/crypto/payment-status/test_payment')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_payment_status_failed(self, mock_get, client):
        """Test payment status when payment failed"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'payment_status': 'failed',
            'pay_amount': 100.0,
            'actually_paid': 0,
            'outcome_amount': 0
        }
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/payment-status/failed_payment')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'failed'
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_payment_status_expired(self, mock_get, client):
        """Test payment status when payment expired"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'payment_status': 'expired',
            'pay_amount': 100.0,
            'actually_paid': 0,
            'outcome_amount': 0
        }
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/payment-status/expired_payment')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'expired'


class TestPaymentWebhook:
    """Tests for POST /api/crypto/webhook endpoint"""
    
    def test_webhook_payment_finished(self, client):
        """Test webhook for finished payment"""
        # Use a hardcoded email instead of test_user to avoid scope mismatch
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_123',
            'payment_status': 'finished',
            'order_id': 'order_program1_test@example.com'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_webhook_payment_finished_no_user(self, client):
        """Test webhook for finished payment with non-existent user"""
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_456',
            'payment_status': 'finished',
            'order_id': 'order_program1_nonexistent@example.com'
        })
        
        # Should still return success even if user not found
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_webhook_payment_failed(self, client):
        """Test webhook for failed payment"""
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_failed',
            'payment_status': 'failed',
            'order_id': 'order_program1_test@example.com'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_webhook_payment_expired(self, client):
        """Test webhook for expired payment"""
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_expired',
            'payment_status': 'expired',
            'order_id': 'order_program1_test@example.com'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_webhook_payment_waiting(self, client):
        """Test webhook for waiting payment status"""
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_waiting',
            'payment_status': 'waiting',
            'order_id': 'order_program1_test@example.com'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_webhook_payment_confirming(self, client):
        """Test webhook for confirming payment status"""
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_confirming',
            'payment_status': 'confirming',
            'order_id': 'order_program1_test@example.com'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_webhook_missing_payment_id(self, client):
        """Test webhook without payment_id"""
        response = client.post('/api/crypto/webhook', json={
            'payment_status': 'finished',
            'order_id': 'order_program1_test@example.com'
        })
        
        # Should handle gracefully
        assert response.status_code == 200
    
    def test_webhook_missing_payment_status(self, client):
        """Test webhook without payment_status"""
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_123',
            'order_id': 'order_program1_test@example.com'
        })
        
        # Should handle gracefully
        assert response.status_code == 200
    
    def test_webhook_missing_order_id(self, client):
        """Test webhook without order_id"""
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_123',
            'payment_status': 'finished'
        })
        
        # Should handle gracefully
        assert response.status_code == 200
    
    def test_webhook_empty_body(self, client):
        """Test webhook with empty JSON body"""
        response = client.post('/api/crypto/webhook', json={})
        
        # Should handle gracefully
        assert response.status_code == 200
    
    def test_webhook_invalid_order_id_format(self, client):
        """Test webhook with invalid order_id format"""
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_123',
            'payment_status': 'finished',
            'order_id': 'invalid_format'
        })
        
        # Should handle gracefully
        assert response.status_code == 200
    
    def test_webhook_order_id_with_underscores_in_email(self, client):
        """Test webhook with email containing underscores in order_id"""
        email_with_underscores = f'test_user_{uuid.uuid4()}@example.com'
        
        response = client.post('/api/crypto/webhook', json={
            'payment_id': 'webhook_payment_underscores',
            'payment_status': 'finished',
            'order_id': f'order_program1_{email_with_underscores}'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_webhook_no_json_body(self, client):
        """Test webhook without JSON body"""
        response = client.post('/api/crypto/webhook')
        
        # Should handle missing JSON
        assert response.status_code in [200, 500]


class TestGetAvailableCurrencies:
    """Tests for GET /api/crypto/currencies endpoint"""
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_currencies_success(self, mock_get, client):
        """Test successful currency list retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'currencies': ['btc', 'eth', 'usdttrc20', 'ltc', 'xrp']
        }
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/currencies')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'currencies' in data
        assert len(data['currencies']) == 5
        assert 'btc' in data['currencies']
        assert 'eth' in data['currencies']
        assert 'usdttrc20' in data['currencies']
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_currencies_empty_list(self, mock_get, client):
        """Test currency list when empty"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'currencies': []
        }
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/currencies')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['currencies'] == []
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_currencies_api_error(self, mock_get, client):
        """Test handling of API error when getting currencies"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/currencies')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Failed to fetch currencies' in data['error']
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_currencies_network_error(self, mock_get, client):
        """Test handling of network error when getting currencies"""
        mock_get.side_effect = Exception('Network timeout')
        
        response = client.get('/api/crypto/currencies')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_currencies_no_currencies_key(self, mock_get, client):
        """Test handling when response doesn't have currencies key"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/currencies')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['currencies'] == []
    
    @patch('src.routes.nowpayments.requests.get')
    def test_get_currencies_large_list(self, mock_get, client):
        """Test currency list with many currencies"""
        currencies = [f'crypto{i}' for i in range(100)]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'currencies': currencies
        }
        mock_get.return_value = mock_response
        
        response = client.get('/api/crypto/currencies')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['currencies']) == 100


class TestNowPaymentsIntegration:
    """Integration tests for NowPayments routes"""
    
    @patch('src.routes.nowpayments.requests.post')
    @patch('src.routes.nowpayments.requests.get')
    def test_full_payment_flow(self, mock_get, mock_post, client):
        """Test complete payment flow: create -> check status -> webhook"""
        # Step 1: Create payment
        mock_post_response = MagicMock()
        mock_post_response.status_code = 201
        mock_post_response.json.return_value = {
            'payment_id': 'integration_test_payment',
            'invoice_url': 'https://nowpayments.io/payment/integration_test_payment',
            'pay_address': '0xintegration',
            'pay_amount': 100.0,
            'pay_currency': 'usdttrc20',
            'order_id': 'order_integration_test'
        }
        mock_post.return_value = mock_post_response
        
        create_response = client.post('/api/crypto/create-payment', json={
            'program_id': 'integration_program',
            'amount': 100,
            'email': 'integration@example.com',
            'order_id': 'order_integration_test'
        })
        
        assert create_response.status_code == 201
        payment_id = create_response.get_json()['payment_id']
        
        # Step 2: Check payment status (waiting)
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            'payment_status': 'waiting',
            'pay_amount': 100.0,
            'actually_paid': 0,
            'outcome_amount': 0
        }
        mock_get.return_value = mock_get_response
        
        status_response = client.get(f'/api/crypto/payment-status/{payment_id}')
        assert status_response.status_code == 200
        assert status_response.get_json()['status'] == 'waiting'
        
        # Step 3: Receive webhook (finished)
        webhook_response = client.post('/api/crypto/webhook', json={
            'payment_id': payment_id,
            'payment_status': 'finished',
            'order_id': 'order_integration_test'
        })
        
        assert webhook_response.status_code == 200
        assert webhook_response.get_json()['success'] is True
    
    @patch('src.routes.nowpayments.requests.post')
    def test_payment_creation_with_all_fields(self, mock_post, client):
        """Test payment creation with all possible fields"""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'payment_id': 'full_fields_payment',
            'invoice_url': 'https://nowpayments.io/payment/full_fields_payment',
            'pay_address': '0xfullfields',
            'pay_amount': 500.0,
            'pay_currency': 'usdttrc20',
            'order_id': 'custom_full_order'
        }
        mock_post.return_value = mock_response
        
        response = client.post('/api/crypto/create-payment', json={
            'program_id': 'premium_program',
            'amount': 500,
            'email': 'premium@example.com',
            'order_id': 'custom_full_order'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert all(key in data for key in ['success', 'payment_id', 'payment_url', 
                                            'pay_address', 'pay_amount', 'pay_currency', 'order_id'])
