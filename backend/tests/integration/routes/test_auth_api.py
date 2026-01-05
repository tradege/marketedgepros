"""
Test Auth API
"""
import json
import pytest
from src.models import User

def extract_cookie_value(response, cookie_name):
    """Helper to extract cookie value from response"""
    cookies = response.headers.getlist('Set-Cookie')
    for cookie in cookies:
        if cookie.startswith(f'{cookie_name}='):
            token_part = cookie.split(';')[0]
            return token_part.split('=', 1)[1]
    return None

class TestAuthAPI:
    """Test Auth API"""
    
    def test_login_success(self, client, trader_user):
        """Test successful login"""
        # Arrange
        data = {
            'email': trader_user.email,
            'password': 'Test123!@#'
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check for tokens in cookies (httpOnly migration)
        access_token = extract_cookie_value(response, 'access_token')
        refresh_token = extract_cookie_value(response, 'refresh_token')
        
        # Either verification_code in JSON OR tokens in cookies
        assert 'verification_code' in data or (access_token and refresh_token)
        assert 'user' in data
    
    def test_login_wrong_password(self, client, trader_user):
        """Test login with wrong password"""
        # Arrange
        data = {
            'email': trader_user.email,
            'password': 'WrongPassword123'
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        # Arrange
        data = {
            'email': 'nonexistent@test.com',
            'password': 'Test123!@#'
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 401
    
    def test_verify_email_success(self, client, unverified_user):
        """Test successful email verification"""
        # Arrange
        code = unverified_user.generate_verification_token()
        data = {
            'email': unverified_user.email,
            'code': code
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/verify-email',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        print(f"Response: {response.status_code}, Data: {response.get_json()}")
        # Assert
        assert response.status_code == 200
    
    def test_verify_email_wrong_code(self, client, unverified_user):
        """Test email verification with wrong code"""
        # Arrange
        unverified_user.generate_verification_token()
        data = {
            'email': unverified_user.email,
            'code': '999999'
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/verify-email',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_password_reset_request(self, client, trader_user, mock_sendgrid):
        """Test password reset request"""
        # Arrange
        data = {
            'email': trader_user.email
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/password/reset-request',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_password_reset_success(self, client, trader_user):
        """Test successful password reset"""
        # Arrange
        code = trader_user.generate_password_reset_token()
        data = {
            'email': trader_user.email,
            'code': code,
            'new_password': 'NewPassword123!@#'
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/password/reset-with-code',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_refresh_token_success(self, client, trader_user):
        """Test successful token refresh"""
        # Arrange
        refresh_token = trader_user.generate_refresh_token()
        
        # Act
        response = client.post(
            '/api/v1/auth/refresh',
            json={'refresh_token': refresh_token},
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Check for access_token in cookies (httpOnly migration)
        access_token = extract_cookie_value(response, 'access_token')
        assert access_token is not None, "access_token should be in cookies"
    
    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        # Act
        response = client.get('/api/v1/profile')
        
        # Assert
        assert response.status_code == 401
    
    def test_protected_endpoint_with_token(self, client, trader_auth_headers):
        """Test accessing protected endpoint with valid token"""
        # Act
        response = client.get(
            '/api/v1/profile',
            headers=trader_auth_headers
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_protected_endpoint_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        # Arrange
        headers = {
            'Authorization': 'Bearer invalid.token.here',
            'Content-Type': 'application/json'
        }
        
        # Act
        response = client.get(
            '/api/v1/profile',
            headers=headers
        )
        
        # Assert
        assert response.status_code == 401
