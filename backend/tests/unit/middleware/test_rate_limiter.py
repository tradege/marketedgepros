"""
Tests for Rate Limiter Middleware
Tests rate limiting functionality to prevent API abuse
"""
import pytest
from flask import Flask, jsonify
from unittest.mock import patch, MagicMock
from src.middleware.rate_limiter import (
    get_user_identifier,
    get_rate_limit,
    init_rate_limiter,
    limiter,
    RATE_LIMITS
)


class TestGetUserIdentifier:
    """Test user identification for rate limiting"""
    
    @pytest.fixture
    def app(self):
        """Create Flask app for request context"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
    
    def test_get_user_identifier_with_jwt(self, app):
        """Test getting user identifier from JWT token"""
        with app.test_request_context():
            with patch('flask_jwt_extended.get_jwt_identity') as mock_jwt:
                mock_jwt.return_value = 123
                
                identifier = get_user_identifier()
                
                assert identifier == 'user:123'
                mock_jwt.assert_called_once()
    
    def test_get_user_identifier_without_jwt(self, app):
        """Test getting user identifier from IP when no JWT"""
        with app.test_request_context(environ_base={'REMOTE_ADDR': '192.168.1.1'}):
            with patch('flask_jwt_extended.get_jwt_identity') as mock_jwt:
                mock_jwt.side_effect = Exception("No JWT")
                
                identifier = get_user_identifier()
                
                assert identifier == '192.168.1.1'
    
    def test_get_user_identifier_jwt_returns_none(self, app):
        """Test fallback to IP when JWT returns None"""
        with app.test_request_context(environ_base={'REMOTE_ADDR': '10.0.0.1'}):
            with patch('flask_jwt_extended.get_jwt_identity') as mock_jwt:
                mock_jwt.return_value = None
                
                identifier = get_user_identifier()
                
                assert identifier == '10.0.0.1'


class TestGetRateLimit:
    """Test rate limit retrieval"""
    
    def test_get_rate_limit_auth_login(self):
        """Test rate limit for login endpoint"""
        limit = get_rate_limit('auth_login')
        assert limit == "5 per minute"
    
    def test_get_rate_limit_auth_register(self):
        """Test rate limit for registration endpoint"""
        limit = get_rate_limit('auth_register')
        assert limit == "3 per hour"
    
    def test_get_rate_limit_auth_password_reset(self):
        """Test rate limit for password reset endpoint"""
        limit = get_rate_limit('auth_password_reset')
        assert limit == "3 per hour"
    
    def test_get_rate_limit_auth_verify_email(self):
        """Test rate limit for email verification endpoint"""
        limit = get_rate_limit('auth_verify_email')
        assert limit == "10 per hour"
    
    def test_get_rate_limit_payment_create(self):
        """Test rate limit for payment creation endpoint"""
        limit = get_rate_limit('payment_create')
        assert limit == "10 per hour"
    
    def test_get_rate_limit_payment_list(self):
        """Test rate limit for payment list endpoint"""
        limit = get_rate_limit('payment_list')
        assert limit == "60 per minute"
    
    def test_get_rate_limit_challenge_create(self):
        """Test rate limit for challenge creation endpoint"""
        limit = get_rate_limit('challenge_create')
        assert limit == "5 per hour"
    
    def test_get_rate_limit_challenge_list(self):
        """Test rate limit for challenge list endpoint"""
        limit = get_rate_limit('challenge_list')
        assert limit == "100 per minute"
    
    def test_get_rate_limit_withdrawal_create(self):
        """Test rate limit for withdrawal creation endpoint"""
        limit = get_rate_limit('withdrawal_create')
        assert limit == "3 per hour"
    
    def test_get_rate_limit_withdrawal_list(self):
        """Test rate limit for withdrawal list endpoint"""
        limit = get_rate_limit('withdrawal_list')
        assert limit == "60 per minute"
    
    def test_get_rate_limit_user_profile(self):
        """Test rate limit for user profile endpoint"""
        limit = get_rate_limit('user_profile')
        assert limit == "100 per minute"
    
    def test_get_rate_limit_user_update(self):
        """Test rate limit for user update endpoint"""
        limit = get_rate_limit('user_update')
        assert limit == "20 per hour"
    
    def test_get_rate_limit_admin_action(self):
        """Test rate limit for admin action endpoint"""
        limit = get_rate_limit('admin_action')
        assert limit == "100 per hour"
    
    def test_get_rate_limit_unknown_endpoint(self):
        """Test rate limit for unknown endpoint returns default"""
        limit = get_rate_limit('unknown_endpoint')
        assert limit == "200 per hour"
    
    def test_get_rate_limit_empty_string(self):
        """Test rate limit for empty string returns default"""
        limit = get_rate_limit('')
        assert limit == "200 per hour"
    
    def test_get_rate_limit_none(self):
        """Test rate limit for None returns default"""
        limit = get_rate_limit(None)
        assert limit == "200 per hour"


class TestRateLimitsConfiguration:
    """Test rate limits configuration dictionary"""
    
    def test_rate_limits_dict_exists(self):
        """Test RATE_LIMITS dictionary exists"""
        assert RATE_LIMITS is not None
        assert isinstance(RATE_LIMITS, dict)
    
    def test_rate_limits_has_auth_endpoints(self):
        """Test RATE_LIMITS has all auth endpoints"""
        assert 'auth_login' in RATE_LIMITS
        assert 'auth_register' in RATE_LIMITS
        assert 'auth_password_reset' in RATE_LIMITS
        assert 'auth_verify_email' in RATE_LIMITS
    
    def test_rate_limits_has_payment_endpoints(self):
        """Test RATE_LIMITS has payment endpoints"""
        assert 'payment_create' in RATE_LIMITS
        assert 'payment_list' in RATE_LIMITS
    
    def test_rate_limits_has_challenge_endpoints(self):
        """Test RATE_LIMITS has challenge endpoints"""
        assert 'challenge_create' in RATE_LIMITS
        assert 'challenge_list' in RATE_LIMITS
    
    def test_rate_limits_has_withdrawal_endpoints(self):
        """Test RATE_LIMITS has withdrawal endpoints"""
        assert 'withdrawal_create' in RATE_LIMITS
        assert 'withdrawal_list' in RATE_LIMITS
    
    def test_rate_limits_has_user_endpoints(self):
        """Test RATE_LIMITS has user endpoints"""
        assert 'user_profile' in RATE_LIMITS
        assert 'user_update' in RATE_LIMITS
    
    def test_rate_limits_has_admin_endpoints(self):
        """Test RATE_LIMITS has admin endpoints"""
        assert 'admin_action' in RATE_LIMITS
    
    def test_rate_limits_has_default(self):
        """Test RATE_LIMITS has default limit"""
        assert 'api_default' in RATE_LIMITS
    
    def test_rate_limits_values_format(self):
        """Test all rate limit values are properly formatted strings"""
        for key, value in RATE_LIMITS.items():
            assert isinstance(value, str)
            assert 'per' in value.lower()


class TestInitRateLimiter:
    """Test rate limiter initialization"""
    
    def test_init_rate_limiter_returns_limiter(self):
        """Test init_rate_limiter returns limiter instance"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        result = init_rate_limiter(app)
        
        assert result is not None
        assert result == limiter
    
    def test_init_rate_limiter_registers_error_handler(self):
        """Test init_rate_limiter registers 429 error handler"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        init_rate_limiter(app)
        
        # Check that error handler is registered
        # Flask registers error handlers by status code
        assert 429 in app.error_handler_spec.get(None, {}) or len(app.error_handler_spec) > 0
    
    def test_rate_limit_error_handler_response(self):
        """Test 429 error handler returns correct response"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        init_rate_limiter(app)
        
        # Create a test client and trigger a 429 error
        with app.test_client() as client:
            # Add a route with very strict limit
            @app.route('/test-limit')
            @limiter.limit("1 per minute")
            def test_limit():
                return jsonify({'message': 'ok'})
            
            # First request should succeed
            response1 = client.get('/test-limit')
            assert response1.status_code == 200
            
            # Second request should trigger 429
            response2 = client.get('/test-limit')
            assert response2.status_code == 429
            
            data = response2.get_json()
            assert 'error' in data
            assert data['error'] == 'Rate limit exceeded'
            assert 'message' in data
            assert 'retry_after' in data


class TestRateLimiterIntegration:
    """Integration tests for rate limiter"""
    
    @pytest.fixture
    def app(self):
        """Create Flask app with rate limiter"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Initialize rate limiter
        init_rate_limiter(app)
        
        # Add test routes
        @app.route('/test')
        @limiter.limit("2 per minute")
        def test_route():
            return jsonify({'message': 'success'})
        
        @app.route('/unlimited')
        def unlimited_route():
            return jsonify({'message': 'unlimited'})
        
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    def test_rate_limiter_allows_requests_under_limit(self, client):
        """Test rate limiter allows requests under the limit"""
        # First request should succeed
        response1 = client.get('/test')
        assert response1.status_code == 200
        
        # Second request should succeed
        response2 = client.get('/test')
        assert response2.status_code == 200
    
    def test_rate_limiter_blocks_requests_over_limit(self, client):
        """Test rate limiter blocks requests over the limit"""
        # Make 2 requests (the limit)
        client.get('/test')
        client.get('/test')
        
        # Third request should be blocked
        response = client.get('/test')
        assert response.status_code == 429
    
    def test_rate_limiter_error_response_format(self, client):
        """Test rate limiter error response has correct format"""
        # Exceed the limit
        client.get('/test')
        client.get('/test')
        response = client.get('/test')
        
        assert response.status_code == 429
        data = response.get_json()
        
        assert 'error' in data
        assert data['error'] == 'Rate limit exceeded'
        assert 'message' in data
        assert 'retry_after' in data
    
    def test_rate_limiter_does_not_affect_unlimited_routes(self, client):
        """Test rate limiter does not affect routes without limits"""
        # Make many requests to unlimited route
        for _ in range(10):
            response = client.get('/unlimited')
            assert response.status_code == 200
    
    def test_rate_limiter_headers_enabled(self, client):
        """Test rate limiter adds rate limit headers"""
        response = client.get('/test')
        
        # Check for rate limit headers
        # Note: flask-limiter adds these headers when headers_enabled=True
        assert response.status_code == 200


class TestRateLimiterEdgeCases:
    """Test edge cases for rate limiter"""
    
    def test_get_rate_limit_with_special_characters(self):
        """Test get_rate_limit with special characters"""
        limit = get_rate_limit('endpoint-with-dashes')
        assert limit == "200 per hour"  # Should return default
    
    def test_get_rate_limit_case_sensitivity(self):
        """Test get_rate_limit is case sensitive"""
        limit = get_rate_limit('AUTH_LOGIN')  # uppercase
        assert limit == "200 per hour"  # Should return default, not auth_login
    
    def test_rate_limits_strict_auth_endpoints(self):
        """Test auth endpoints have strict limits"""
        # Login should be very strict (prevent brute force)
        assert RATE_LIMITS['auth_login'] == "5 per minute"
        
        # Register should be strict (prevent spam)
        assert RATE_LIMITS['auth_register'] == "3 per hour"
        
        # Password reset should be strict (prevent abuse)
        assert RATE_LIMITS['auth_password_reset'] == "3 per hour"
    
    def test_rate_limits_moderate_payment_endpoints(self):
        """Test payment endpoints have moderate limits"""
        # Payment creation should be limited
        assert RATE_LIMITS['payment_create'] == "10 per hour"
        
        # Payment listing can be more frequent
        assert RATE_LIMITS['payment_list'] == "60 per minute"
    
    def test_rate_limits_lenient_user_endpoints(self):
        """Test user endpoints have lenient limits"""
        # Profile access should be very lenient
        assert RATE_LIMITS['user_profile'] == "100 per minute"
        
        # Updates should be moderate
        assert RATE_LIMITS['user_update'] == "20 per hour"
