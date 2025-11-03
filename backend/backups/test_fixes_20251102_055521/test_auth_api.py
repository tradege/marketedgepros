"""
Integration tests for Authentication API endpoints
"""
import pytest
import json


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestAuthAPI:
    """Test authentication API endpoints"""
    
    def test_register_success(self, client, session, mock_sendgrid):
        """Test successful user registration"""
        # Arrange
        data = {
            'email': 'newuser@test.com',
            'password': 'Test123!@#',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['email'] == 'newuser@test.com'
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields"""
        # Arrange
        data = {
            'email': 'incomplete@test.com'
            # Missing password, first_name, last_name
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_register_duplicate_email(self, client, trader_user):
        """Test registration with duplicate email"""
        # Arrange
        data = {
            'email': trader_user.email,
            'password': 'TraderPassword123!',
            'first_name': 'Duplicate',
            'last_name': 'User'
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_login_success(self, client, trader_user):
        """Test successful login"""
        # Arrange
        data = {
            'email': trader_user.email,
            'password': 'TraderPassword123!'
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
        assert 'refresh_token' in data
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
        # Create verification token
        from src.models.user import EmailVerificationToken
        from src.database import db
        token = EmailVerificationToken(user_id=unverified_user.id)
        db.session.add(token)
        db.session.commit()
        code = token
        data = {
            'email': unverified_user.email,
            'code': code.code
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/verify-email',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_verify_email_wrong_code(self, client, unverified_user):
        """Test email verification with wrong code"""
        # Arrange
        # Create verification token (but we'll use wrong code)
        from src.models.user import EmailVerificationToken
        from src.database import db
        token = EmailVerificationToken(user_id=unverified_user.id)
        db.session.add(token)
        db.session.commit()
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
        from src.models.user import PasswordResetToken
        from src.database import db
        code = PasswordResetToken(user_id=trader_user.id)
        db.session.add(code)
        db.session.commit()
        data = {
            'token': code.token,
            'new_password': 'NewPassword123!@#'
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/password/reset',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_refresh_token_success(self, client, trader_user):
        """Test successful token refresh"""
        # Arrange
        refresh_token = trader_user.generate_refresh_token()
        data = {
            'refresh_token': refresh_token
        }
        
        # Act
        response = client.post(
            '/api/v1/auth/refresh',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
    
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

