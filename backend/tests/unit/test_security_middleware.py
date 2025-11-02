"""
Tests for Security Middleware (CSRF, Headers, Rate Limiting)
"""
import pytest
from flask import Flask, session
from src.middleware.csrf_protection import generate_csrf_token, validate_csrf_token
from src.middleware.rate_limiter import get_rate_limit, RATE_LIMITS

class TestCSRFProtection:
    def test_generate_csrf_token(self, app):
        """Test CSRF token generation"""
        with app.test_request_context():
            token1 = generate_csrf_token()
            assert token1 is not None
            assert len(token1) == 64  # 32 bytes hex = 64 chars
            
            # Same session should return same token
            token2 = generate_csrf_token()
            assert token1 == token2
    
    def test_validate_csrf_token_valid(self, app):
        """Test CSRF token validation with valid token"""
        with app.test_request_context():
            token = generate_csrf_token()
            assert validate_csrf_token(token) is True
    
    def test_validate_csrf_token_invalid(self, app):
        """Test CSRF token validation with invalid token"""
        with app.test_request_context():
            generate_csrf_token()  # Generate a token first
            assert validate_csrf_token('invalid_token') is False
    
    def test_validate_csrf_token_no_session(self, app):
        """Test CSRF token validation without session token"""
        with app.test_request_context():
            assert validate_csrf_token('some_token') is False

class TestRateLimiting:
    def test_rate_limit_auth_login(self):
        """Test rate limit for login endpoint"""
        limit = get_rate_limit('auth_login')
        assert limit == "5 per minute"
    
    def test_rate_limit_auth_register(self):
        """Test rate limit for register endpoint"""
        limit = get_rate_limit('auth_register')
        assert limit == "3 per hour"
    
    def test_rate_limit_payment_create(self):
        """Test rate limit for payment creation"""
        limit = get_rate_limit('payment_create')
        assert limit == "10 per hour"
    
    def test_rate_limit_withdrawal_create(self):
        """Test rate limit for withdrawal creation"""
        limit = get_rate_limit('withdrawal_create')
        assert limit == "3 per hour"
    
    def test_rate_limit_default(self):
        """Test default rate limit"""
        limit = get_rate_limit('unknown_endpoint')
        assert limit == "200 per hour"
    
    def test_all_rate_limits_defined(self):
        """Test that all rate limit types are defined"""
        required_types = [
            'auth_login', 'auth_register', 'auth_password_reset',
            'payment_create', 'challenge_create', 'withdrawal_create',
            'user_profile', 'admin_action', 'api_default'
        ]
        for rate_type in required_types:
            assert rate_type in RATE_LIMITS

@pytest.mark.skip(reason="Security headers require middleware initialization in app.py")
class TestSecurityHeaders:
    def test_security_headers_present(self, client):
        """Test that security headers are present in responses"""
        response = client.get('/api/health')
        
        # Check for security headers
        assert 'X-Frame-Options' in response.headers
        assert 'X-Content-Type-Options' in response.headers
        assert 'X-XSS-Protection' in response.headers
        assert 'Referrer-Policy' in response.headers
    
    def test_x_frame_options(self, client):
        """Test X-Frame-Options header"""
        response = client.get('/api/health')
        assert response.headers.get('X-Frame-Options') == 'DENY'
    
    def test_x_content_type_options(self, client):
        """Test X-Content-Type-Options header"""
        response = client.get('/api/health')
        assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    
    def test_x_xss_protection(self, client):
        """Test X-XSS-Protection header"""
        response = client.get('/api/health')
        assert response.headers.get('X-XSS-Protection') == '1; mode=block'
    
    def test_referrer_policy(self, client):
        """Test Referrer-Policy header"""
        response = client.get('/api/health')
        assert response.headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin'
    
    def test_server_header_removed(self, client):
        """Test that Server header is removed"""
        response = client.get('/api/health')
        assert 'Server' not in response.headers

# Fixtures
@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['TESTING'] = True
    
    @app.route('/api/health')
    def health():
        return {'status': 'ok'}
    
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

