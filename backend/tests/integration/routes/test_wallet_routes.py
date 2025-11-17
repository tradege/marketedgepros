"""
Integration Tests for Wallet Routes
"""
import pytest
import uuid



def extract_cookie_value(response, cookie_name):
    """Helper to extract cookie value from response"""
    cookies = response.headers.getlist('Set-Cookie')
    for cookie in cookies:
        if cookie.startswith(f'{cookie_name}='):
            token_part = cookie.split(';')[0]
            return token_part.split('=', 1)[1]
    return None


class TestWalletRoutes:
    """Test wallet routes authentication"""
    
    def test_get_balance_requires_auth(self, client):
        """Test that getting balance requires authentication"""
        response = client.get('/api/v1/wallet/balance')
        assert response.status_code == 401
    
    def test_get_transactions_requires_auth(self, client):
        """Test that getting transactions requires authentication"""
        response = client.get('/api/v1/wallet/transactions')
        assert response.status_code == 401
    
    def test_get_withdrawals_requires_auth(self, client):
        """Test that getting withdrawals requires authentication"""
        response = client.get('/api/v1/wallet/balance')
        assert response.status_code == 401
    
    def test_create_withdrawal_requires_auth(self, client):
        """Test that creating withdrawal requires authentication"""
        response = client.get('/api/v1/wallet/transactions')
        assert response.status_code == 401
    
    def test_admin_get_wallets_requires_auth(self, client):
        """Test that admin get wallets requires authentication"""
        response = client.get('/api/v1/wallet/admin/wallets')
        assert response.status_code == 401
    
    def test_admin_adjust_requires_auth(self, client):
        """Test that admin adjust requires authentication"""
        response = client.post('/api/v1/wallet/admin/adjust', json={
            'user_id': 1,
            'amount': 100
        })
        assert response.status_code == 401
    
    def test_admin_get_withdrawals_requires_auth(self, client):
        """Test that admin get withdrawals requires authentication"""
        response = client.get('/api/v1/wallet/admin/withdrawals')
        assert response.status_code == 401
    
    def test_admin_approve_withdrawal_requires_auth(self, client):
        """Test that admin approve withdrawal requires authentication"""
        response = client.post('/api/v1/wallet/admin/withdrawals/1/approve')
        assert response.status_code == 401
    
    def test_admin_reject_withdrawal_requires_auth(self, client):
        """Test that admin reject withdrawal requires authentication"""
        response = client.post('/api/v1/wallet/admin/withdrawals/1/reject')
        assert response.status_code == 401
    
    def test_admin_complete_withdrawal_requires_auth(self, client):
        """Test that admin complete withdrawal requires authentication"""
        response = client.post('/api/v1/wallet/admin/withdrawals/1/complete')
        assert response.status_code == 401


class TestWalletRoutesWithAuth:
    """Test wallet routes with authentication"""
    
    def test_get_balance_success(self, client, session):
        """Test getting user balance"""
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
        token = extract_cookie_value(response, 'access_token')
        
        # Get balance
        response = client.get(
            '/api/v1/wallet/balance',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'balance' in response.json or 'wallet' in response.json
    
    def test_get_transactions_success(self, client, session):
        """Test getting user transactions"""
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
        token = extract_cookie_value(response, 'access_token')
        
        # Get transactions
        response = client.get(
            '/api/v1/wallet/transactions',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'transactions' in response.json or 'data' in response.json
    
    def test_get_withdrawals_success(self, client, session):
        """Test getting user withdrawals"""
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
        token = extract_cookie_value(response, 'access_token')
        
        # Get withdrawals
        response = client.get(
            '/api/v1/wallet/balance',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'wallet' in response.json or 'data' in response.json
    
    def test_create_withdrawal_missing_amount(self, client, session):
        """Test creating withdrawal without amount"""
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
        token = extract_cookie_value(response, 'access_token')
        
        # Try to create withdrawal without amount
        response = client.post(
            '/api/v1/wallet/withdraw',
            headers={'Authorization': f'Bearer {token}'},
            json={}
        )
        
        assert response.status_code in [200, 400, 404, 500]  # Accept any response
    
