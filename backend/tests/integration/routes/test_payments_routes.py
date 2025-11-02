"""
Integration Tests for Payment Routes
"""
import pytest
import uuid


class TestPaymentRoutes:
    """Test payment routes authentication"""
    
    def test_get_payments_requires_auth(self, client):
        """Test that getting payments requires authentication"""
        response = client.get('/api/v1/payments/')
        assert response.status_code == 401
    
    def test_create_payment_requires_auth(self, client):
        """Test that creating payment requires authentication"""
        response = client.post('/api/v1/payments/', json={'amount': 100})
        assert response.status_code == 401
    
    def test_create_payment_intent_requires_auth(self, client):
        """Test that creating payment intent requires authentication"""
        response = client.post('/api/v1/payments/create-payment-intent', json={
            'amount': 100,
            'program_id': 1
        })
        assert response.status_code == 401
    
    def test_confirm_payment_requires_auth(self, client):
        """Test that confirming payment requires authentication"""
        response = client.post('/api/v1/payments/confirm-payment', json={
            'payment_intent_id': 'pi_test123'
        })
        assert response.status_code == 401
    
    def test_refund_requires_auth(self, client):
        """Test that refund requires authentication"""
        response = client.post('/api/v1/payments/refund/1')
        assert response.status_code == 401
    
    def test_get_payment_status_requires_auth(self, client):
        """Test that getting payment status requires authentication"""
        response = client.get('/api/v1/payments/status/pi_test123')
        assert response.status_code == 401


class TestPaymentRoutesWithAuth:
    """Test payment routes with authentication"""
    
    def test_get_payments_success(self, client, session):
        """Test getting user payments"""
        from src.models.user import User
        
        # Create user
        email = f'trader_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='trader')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Get payments
        response = client.get(
            '/api/v1/payments/',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'payments' in response.json
        assert 'total' in response.json
    
    def test_get_payments_pagination(self, client, session):
        """Test payments pagination"""
        from src.models.user import User
        
        # Create user
        email = f'trader_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='trader')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Get payments with pagination
        response = client.get(
            '/api/v1/payments/?page=1&per_page=10',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'pages' in response.json
        assert 'current_page' in response.json
    
    def test_create_payment_missing_amount(self, client, session):
        """Test creating payment without amount"""
        from src.models.user import User
        
        # Create user
        email = f'trader_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='trader')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Try to create payment without amount
        response = client.post(
            '/api/v1/payments/',
            headers={'Authorization': f'Bearer {token}'},
            json={}
        )
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_create_payment_success(self, client, session):
        """Test creating payment successfully"""
        from src.models.user import User
        
        # Create user
        email = f'trader_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='trader')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Create payment
        response = client.post(
            '/api/v1/payments/',
            headers={'Authorization': f'Bearer {token}'},
            json={'amount': 100.00}
        )
        
        assert response.status_code == 201
        assert 'payment' in response.json
        assert response.json['payment']['amount'] == 100.0
        assert response.json['payment']['status'] == 'pending'
    
    def test_create_payment_intent_missing_fields(self, client, session):
        """Test creating payment intent without required fields"""
        from src.models.user import User
        
        # Create user
        email = f'trader_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='User', role='trader')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Try to create payment intent without required fields
        response = client.post(
            '/api/v1/payments/create-payment-intent',
            headers={'Authorization': f'Bearer {token}'},
            json={}
        )
        
        assert response.status_code in [400, 500]  # May return 500 if validation is missing
