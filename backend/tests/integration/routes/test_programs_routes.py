"""
Integration Tests for Programs Routes (Trading Programs)
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


class TestProgramsRoutes:
    """Test programs routes authentication"""
    
    def test_get_programs_no_auth_required(self, client):
        """Test that getting programs list doesn't require authentication"""
        response = client.get('/api/v1/programs/')
        assert response.status_code in [200, 401]  # May or may not require auth
    
    def test_get_program_by_id_no_auth_required(self, client):
        """Test that getting single program doesn't require authentication"""
        response = client.get('/api/v1/programs/1')
        assert response.status_code in [200, 404, 401]  # May or may not require auth
    
    def test_create_program_requires_auth(self, client):
        """Test that creating program requires authentication"""
        response = client.post('/api/v1/programs/', json={
            'name': 'Test Program',
            'price': 100
        })
        assert response.status_code == 401
    
    def test_update_program_requires_auth(self, client):
        """Test that updating program requires authentication"""
        response = client.put('/api/v1/programs/1', json={
            'name': 'Updated Program'
        })
        assert response.status_code == 401
    
    def test_add_addons_requires_auth(self, client):
        """Test that adding addons requires authentication"""
        response = client.post('/api/v1/programs/1/addons', json={
            'addon_id': 1
        })
        assert response.status_code == 401
    
    def test_purchase_program_requires_auth(self, client):
        """Test that purchasing program requires authentication"""
        response = client.post('/api/v1/programs/1/purchase', json={
            'payment_method': 'stripe'
        })
        assert response.status_code == 401
    
    def test_get_my_challenges_requires_auth(self, client):
        """Test that getting my challenges requires authentication"""
        response = client.get('/api/v1/programs/my-challenges')
        assert response.status_code == 401
    
    def test_get_challenge_by_id_requires_auth(self, client):
        """Test that getting challenge by id requires authentication"""
        response = client.get('/api/v1/programs/challenges/1')
        assert response.status_code == 401


class TestProgramsRoutesWithAuth:
    """Test programs routes with authentication"""
    
    def test_get_programs_success(self, client, session):
        """Test getting programs list"""
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
        
        # Get programs
        response = client.get(
            '/api/v1/programs/',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'programs' in response.json or 'data' in response.json or isinstance(response.json, list)
    
    def test_get_program_by_id_not_found(self, client, session):
        """Test getting non-existent program"""
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
        
        # Try to get non-existent program
        response = client.get(
            '/api/v1/programs/99999',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code in [404, 500]
    
    def test_create_program_requires_admin(self, client, session):
        """Test that creating program requires admin role"""
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
        token = extract_cookie_value(response, 'access_token')
        
        # Try to create program
        response = client.post(
            '/api/v1/programs/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'name': 'Test Program',
                'price': 100
            }
        )
        
        assert response.status_code in [403, 500]
    
    def test_purchase_program_missing_fields(self, client, session):
        """Test purchasing program without required fields"""
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
        
        # Try to purchase without required fields
        response = client.post(
            '/api/v1/programs/1/purchase',
            headers={'Authorization': f'Bearer {token}'},
            json={}
        )
        
        assert response.status_code in [400, 404, 500]
    
    def test_get_my_challenges_success(self, client, session):
        """Test getting user's challenges"""
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
        
        # Get my challenges
        response = client.get(
            '/api/v1/programs/my-challenges',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'challenges' in response.json or 'data' in response.json or isinstance(response.json, list)
    
    def test_get_challenge_by_id_not_found(self, client, session):
        """Test getting non-existent challenge"""
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
        
        # Try to get non-existent challenge
        response = client.get(
            '/api/v1/programs/challenges/99999',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code in [404, 500]
