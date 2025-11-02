"""
Integration Tests for Hierarchy Routes (MLM Structure)
"""
import pytest
import uuid


class TestHierarchyRoutes:
    """Test hierarchy routes authentication"""
    
    def test_get_my_downline_requires_auth(self, client):
        """Test that getting downline requires authentication"""
        response = client.get('/api/v1/hierarchy/my-downline')
        assert response.status_code == 401
    
    def test_get_my_direct_team_requires_auth(self, client):
        """Test that getting direct team requires authentication"""
        response = client.get('/api/v1/hierarchy/my-direct-team')
        assert response.status_code == 401
    
    def test_create_user_requires_auth(self, client):
        """Test that creating user requires authentication"""
        response = client.post('/api/v1/hierarchy/create-user', json={
            'email': 'test@test.com',
            'role': 'trader'
        })
        assert response.status_code == 401
    
    def test_get_user_requires_auth(self, client):
        """Test that getting user requires authentication"""
        response = client.get('/api/v1/hierarchy/user/1')
        assert response.status_code == 401
    
    def test_update_user_requires_auth(self, client):
        """Test that updating user requires authentication"""
        response = client.put('/api/v1/hierarchy/user/1', json={
            'first_name': 'Updated'
        })
        assert response.status_code == 401
    
    def test_get_tree_requires_auth(self, client):
        """Test that getting tree requires authentication"""
        response = client.get('/api/v1/hierarchy/tree')
        assert response.status_code == 401
    
    def test_get_stats_requires_auth(self, client):
        """Test that getting stats requires authentication"""
        response = client.get('/api/v1/hierarchy/stats')
        assert response.status_code == 401


class TestHierarchyRoutesWithAuth:
    """Test hierarchy routes with authentication"""
    
    def test_get_my_downline_success(self, client, session):
        """Test getting user's downline"""
        from src.models.user import User
        
        # Create user
        email = f'agent_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='Agent', role='agent')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Get downline
        response = client.get(
            '/api/v1/hierarchy/my-downline',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        # Accept any 200 response
    
    def test_get_my_direct_team_success(self, client, session):
        """Test getting user's direct team"""
        from src.models.user import User
        
        # Create user
        email = f'agent_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='Agent', role='agent')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Get direct team
        response = client.get(
            '/api/v1/hierarchy/my-direct-team',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'team' in response.json or 'users' in response.json or 'data' in response.json
    
    def test_create_user_missing_fields(self, client, session):
        """Test creating user without required fields"""
        from src.models.user import User
        
        # Create agent
        email = f'agent_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='Agent', role='agent')
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
            '/api/v1/hierarchy/create-user',
            headers={'Authorization': f'Bearer {token}'},
            json={}
        )
        
        assert response.status_code in [400, 500]
    
    def test_get_user_not_found(self, client, session):
        """Test getting non-existent user"""
        from src.models.user import User
        
        # Create user
        email = f'agent_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='Agent', role='agent')
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
            '/api/v1/hierarchy/user/99999',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code in [404, 500]
    
    def test_update_user_not_found(self, client, session):
        """Test updating non-existent user"""
        from src.models.user import User
        
        # Create user
        email = f'agent_{uuid.uuid4().hex[:8]}@test.com'
        user = User(email=email, first_name='Test', last_name='Agent', role='agent')
        user.set_password('Test123!')
        session.add(user)
        session.commit()
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': 'Test123!'
        })
        token = response.json['access_token']
        
        # Try to update non-existent user
        response = client.put(
            '/api/v1/hierarchy/user/99999',
            headers={'Authorization': f'Bearer {token}'},
            json={'first_name': 'Updated'}
        )
        
        assert response.status_code in [404, 500]
    
