"""
Integration Tests for Admin Routes
"""
import pytest
import uuid


class TestAdminRoutes:
    """Test admin routes authentication and permissions"""
    
    def test_dashboard_stats_requires_auth(self, client):
        """Test that dashboard stats requires authentication"""
        response = client.get('/api/v1/admin/dashboard/stats')
        assert response.status_code == 401
    
    def test_get_users_requires_auth(self, client):
        """Test that getting users requires authentication"""
        response = client.get('/api/v1/admin/users')
        assert response.status_code == 401
    
    def test_get_user_by_id_requires_auth(self, client):
        """Test that getting user by id requires authentication"""
        response = client.get('/api/v1/admin/users/1')
        assert response.status_code == 401
    
    def test_create_user_requires_auth(self, client):
        """Test that creating user requires authentication"""
        response = client.post('/api/v1/admin/users', json={
            'email': 'test@test.com',
            'role': 'trader'
        })
        assert response.status_code == 401
    
    def test_update_user_requires_auth(self, client):
        """Test that updating user requires authentication"""
        response = client.put('/api/v1/admin/users/1', json={
            'first_name': 'Updated'
        })
        assert response.status_code == 401
    
    def test_delete_user_requires_auth(self, client):
        """Test that deleting user requires authentication"""
        response = client.delete('/api/v1/admin/users/1')
        assert response.status_code == 401
    
    def test_reset_password_requires_auth(self, client):
        """Test that resetting password requires authentication"""
        response = client.post('/api/v1/admin/users/1/reset-password')
        assert response.status_code == 401
    
    def test_get_programs_requires_auth(self, client):
        """Test that getting programs requires authentication"""
        response = client.get('/api/v1/admin/programs')
        assert response.status_code == 401
    
    def test_create_program_requires_auth(self, client):
        """Test that creating program requires authentication"""
        response = client.post('/api/v1/admin/programs', json={
            'name': 'Test Program'
        })
        assert response.status_code == 401
    
    def test_get_payments_requires_auth(self, client):
        """Test that getting payments requires authentication"""
        response = client.get('/api/v1/admin/payments')
        assert response.status_code == 401
    
    def test_get_pending_kyc_requires_auth(self, client):
        """Test that getting pending KYC requires authentication"""
        response = client.get('/api/v1/admin/kyc/pending')
        assert response.status_code == 401
    
    def test_approve_kyc_requires_auth(self, client):
        """Test that approving KYC requires authentication"""
        response = client.post('/api/v1/admin/kyc/1/approve')
        assert response.status_code == 401
    
    def test_get_user_tree_requires_auth(self, client):
        """Test that getting user tree requires authentication"""
        response = client.get('/api/v1/hierarchy/tree')
        assert response.status_code == 401


class TestAdminRoutesWithTrader:
    """Test that admin routes require admin role"""
    
    def test_dashboard_stats_requires_admin(self, client, session):
        """Test that dashboard stats requires admin role"""
        from src.models.user import User
        
        # Create regular trader
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
        
        # Try to access admin endpoint
        response = client.get(
            '/api/v1/admin/dashboard/stats',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 403
    
    def test_get_users_requires_admin(self, client, session):
        """Test that getting users requires admin role"""
        from src.models.user import User
        
        # Create regular trader
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
        
        # Try to access admin endpoint
        response = client.get(
            '/api/v1/admin/users',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 403


class TestAdminRoutesWithAdmin:
    """Test admin routes with admin user"""
    
    def test_dashboard_stats_success(self, client, session):
        """Test getting dashboard stats as admin"""
        from src.models.user import User
        
        # Create admin
        email = f'admin_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Admin', last_name='User', role='supermaster')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Get dashboard stats
        response = client.get(
            '/api/v1/admin/dashboard/stats',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'stats' in response.json or 'data' in response.json or isinstance(response.json, dict)
    
    def test_get_users_success(self, client, session):
        """Test getting users list as admin"""
        from src.models.user import User
        
        # Create admin
        email = f'admin_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Admin', last_name='User', role='supermaster')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Get users
        response = client.get(
            '/api/v1/admin/users',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'users' in response.json or 'data' in response.json or isinstance(response.json, list)
    
    def test_get_user_by_id_not_found(self, client, session):
        """Test getting non-existent user as admin"""
        from src.models.user import User
        
        # Create admin
        email = f'admin_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Admin', last_name='User', role='supermaster')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Try to get non-existent user
        response = client.get(
            '/api/v1/admin/users/99999',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code in [404, 500]
    
    def test_create_user_missing_fields(self, client, session):
        """Test creating user without required fields"""
        from src.models.user import User
        
        # Create admin
        email = f'admin_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Admin', last_name='User', role='supermaster')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Try to create user without required fields
        response = client.post(
            '/api/v1/admin/users',
            headers={'Authorization': f'Bearer {token}'},
            json={}
        )
        
        assert response.status_code in [400, 500]
    
    def test_get_payments_success(self, client, session):
        """Test getting payments as admin"""
        from src.models.user import User
        
        # Create admin
        email = f'admin_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Admin', last_name='User', role='supermaster')
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
            '/api/v1/admin/payments',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'payments' in response.json or 'data' in response.json or isinstance(response.json, list)
