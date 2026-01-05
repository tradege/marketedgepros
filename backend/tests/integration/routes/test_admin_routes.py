"""
Integration Tests for Admin Routes
"""
import pytest
import uuid
from src.extensions import db
from src.models.user import User


def get_token_from_response(response):
    """Helper to extract access token from login response body"""
    data = response.get_json()
    return data.get('access_token') if data else None


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
        """Test that getting user by ID requires authentication"""
        response = client.get('/api/v1/admin/users/1')
        assert response.status_code == 401
    
    def test_create_user_requires_auth(self, client):
        """Test that creating user requires authentication"""
        response = client.post('/api/v1/admin/users', json={})
        assert response.status_code == 401
    
    def test_update_user_requires_auth(self, client):
        """Test that updating user requires authentication"""
        response = client.put('/api/v1/admin/users/1', json={})
        assert response.status_code == 401
    
    def test_get_programs_requires_auth(self, client):
        """Test that getting programs requires authentication"""
        response = client.get('/api/v1/admin/programs')
        assert response.status_code == 401
    
    def test_get_payments_requires_auth(self, client):
        """Test that getting payments requires authentication"""
        response = client.get('/api/v1/admin/payments')
        assert response.status_code == 401
    
    def test_get_pending_kyc_requires_auth(self, client):
        """Test that getting pending KYC requires authentication"""
        response = client.get('/api/v1/admin/kyc/pending')
        assert response.status_code == 401
    
    def test_reset_password_requires_auth(self, client):
        """Test that resetting password requires authentication"""
        response = client.post('/api/v1/admin/users/1/reset-password', json={})
        assert response.status_code == 401


class TestAdminRoutesWithTrader:
    """Test admin routes with trader user (should be forbidden)"""
    
    def test_dashboard_stats_requires_admin(self, app, client):
        """Test that dashboard stats requires admin role"""
        with app.app_context():
            # Create regular trader
            email = f'trader_{uuid.uuid4().hex[:8]}@test.com'
            user = User(email=email, first_name='Test', last_name='User', role='trader')
            user.set_password('Test123!')
            user.is_verified = True
            db.session.add(user)
            db.session.commit()
            
            # Login
            response = client.post('/api/v1/auth/login', json={
                'email': email,
                'password': 'Test123!'
            })
            token = get_token_from_response(response)
            
            # Try to access admin endpoint
            response = client.get(
                '/api/v1/admin/dashboard/stats',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 403
    
    def test_get_users_requires_admin(self, app, client):
        """Test that getting users requires admin role"""
        with app.app_context():
            # Create regular trader
            email = f'trader_{uuid.uuid4().hex[:8]}@test.com'
            user = User(email=email, first_name='Test', last_name='User', role='trader')
            user.set_password('Test123!')
            user.is_verified = True
            db.session.add(user)
            db.session.commit()
            
            # Login
            response = client.post('/api/v1/auth/login', json={
                'email': email,
                'password': 'Test123!'
            })
            token = get_token_from_response(response)
            
            # Try to access admin endpoint
            response = client.get(
                '/api/v1/admin/users',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 403


class TestAdminRoutesWithAdmin:
    """Test admin routes with admin user"""
    
    def test_dashboard_stats_success(self, app, client):
        """Test getting dashboard stats as admin"""
        with app.app_context():
            # Create admin
            email = f'admin_{uuid.uuid4().hex[:8]}@test.com'
            user = User(email=email, first_name='Admin', last_name='User', role='supermaster')
            user.set_password('Test123!')
            user.is_verified = True
            db.session.add(user)
            db.session.commit()
            
            # Login
            response = client.post('/api/v1/auth/login', json={
                'email': email,
                'password': 'Test123!'
            })
            token = get_token_from_response(response)
            
            # Get dashboard stats
            response = client.get(
                '/api/v1/admin/dashboard/stats',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            assert isinstance(response.json, dict)
    
    def test_get_users_success(self, app, client):
        """Test getting users list as admin"""
        with app.app_context():
            # Create admin
            email = f'admin_{uuid.uuid4().hex[:8]}@test.com'
            user = User(email=email, first_name='Admin', last_name='User', role='supermaster')
            user.set_password('Test123!')
            user.is_verified = True
            db.session.add(user)
            db.session.commit()
            
            # Login
            response = client.post('/api/v1/auth/login', json={
                'email': email,
                'password': 'Test123!'
            })
            token = get_token_from_response(response)
            
            # Get users
            response = client.get(
                '/api/v1/admin/users',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
    
    def test_get_user_by_id_not_found(self, app, client):
        """Test getting non-existent user as admin"""
        with app.app_context():
            # Create admin
            email = f'admin_{uuid.uuid4().hex[:8]}@test.com'
            user = User(email=email, first_name='Admin', last_name='User', role='supermaster')
            user.set_password('Test123!')
            user.is_verified = True
            db.session.add(user)
            db.session.commit()
            
            # Login
            response = client.post('/api/v1/auth/login', json={
                'email': email,
                'password': 'Test123!'
            })
            token = get_token_from_response(response)
            
            # Try to get non-existent user
            response = client.get(
                '/api/v1/admin/users/99999999',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code in [404, 500]
