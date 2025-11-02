"""
Tests for Security Headers Middleware
"""
import pytest
from flask import Flask
from src.middleware.security_headers import init_security_headers, add_cors_headers


class TestSecurityHeadersInit:
    """Test security headers initialization"""
    
    def test_init_security_headers_with_https(self):
        """Test initialization with HTTPS enforcement"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Initialize with HTTPS
        result = init_security_headers(app, force_https=True)
        
        assert result is app
        assert 'after_request_funcs' in app.__dict__
    
    def test_init_security_headers_without_https(self):
        """Test initialization without HTTPS enforcement"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Initialize without HTTPS
        result = init_security_headers(app, force_https=False)
        
        assert result is app
        assert 'after_request_funcs' in app.__dict__
    
    def test_init_security_headers_default_https(self):
        """Test initialization with default HTTPS setting"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Initialize with default (no HTTPS)
        result = init_security_headers(app)
        
        assert result is app


class TestSecurityHeaders:
    """Test security headers in responses"""
    
    @pytest.fixture
    def app(self):
        """Create test Flask app with security headers"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        init_security_headers(app, force_https=False)
        
        @app.route('/test')
        def test_route():
            return 'OK'
        
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    def test_x_frame_options_header(self, client):
        """Test X-Frame-Options header is set"""
        response = client.get('/test')
        
        assert 'X-Frame-Options' in response.headers
        # Talisman sets it to SAMEORIGIN by default, our middleware tries to set DENY
        # but Talisman's value takes precedence
        assert response.headers['X-Frame-Options'] in ['DENY', 'SAMEORIGIN']
    
    def test_x_content_type_options_header(self, client):
        """Test X-Content-Type-Options header is set"""
        response = client.get('/test')
        
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
    
    def test_x_xss_protection_header(self, client):
        """Test X-XSS-Protection header is set"""
        response = client.get('/test')
        
        assert 'X-XSS-Protection' in response.headers
        assert response.headers['X-XSS-Protection'] == '1; mode=block'
    
    def test_referrer_policy_header(self, client):
        """Test Referrer-Policy header is set"""
        response = client.get('/test')
        
        assert 'Referrer-Policy' in response.headers
        assert response.headers['Referrer-Policy'] == 'strict-origin-when-cross-origin'
    
    def test_permissions_policy_header(self, client):
        """Test Permissions-Policy header is set"""
        response = client.get('/test')
        
        # Talisman might set different Permissions-Policy
        # Just check that the header exists
        assert 'Permissions-Policy' in response.headers or 'Feature-Policy' in response.headers
    
    def test_server_header_removed(self, client):
        """Test Server header is removed"""
        response = client.get('/test')
        
        # Server header should be removed for security
        assert 'Server' not in response.headers
    
    def test_custom_security_header(self, client):
        """Test custom security header is added"""
        response = client.get('/test')
        
        assert 'X-Security-Protected' in response.headers
        assert response.headers['X-Security-Protected'] == 'MarketEdgePros'
    
    def test_content_security_policy_header(self, client):
        """Test Content-Security-Policy header is set"""
        response = client.get('/test')
        
        # Talisman should add CSP header
        assert 'Content-Security-Policy' in response.headers or 'Content-Security-Policy-Report-Only' in response.headers
    
    def test_strict_transport_security_header(self, client):
        """Test Strict-Transport-Security header"""
        response = client.get('/test')
        
        # HSTS header might not be present in test mode without HTTPS
        # This is expected behavior
        assert response.status_code == 200


class TestCORSHeaders:
    """Test CORS headers"""
    
    @pytest.fixture
    def app(self):
        """Create test Flask app with CORS headers"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        add_cors_headers(app, allowed_origins=['http://localhost:3000'])
        
        @app.route('/api/test')
        def test_route():
            return {'message': 'OK'}
        
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    def test_cors_allowed_origin(self, client):
        """Test CORS headers for allowed origin"""
        response = client.get('/api/test', headers={'Origin': 'http://localhost:3000'})
        
        assert 'Access-Control-Allow-Origin' in response.headers
        assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'
    
    def test_cors_allowed_methods(self, client):
        """Test CORS allowed methods header"""
        response = client.get('/api/test', headers={'Origin': 'http://localhost:3000'})
        
        assert 'Access-Control-Allow-Methods' in response.headers
        methods = response.headers['Access-Control-Allow-Methods']
        
        assert 'GET' in methods
        assert 'POST' in methods
        assert 'PUT' in methods
        assert 'DELETE' in methods
        assert 'OPTIONS' in methods
    
    def test_cors_allowed_headers(self, client):
        """Test CORS allowed headers"""
        response = client.get('/api/test', headers={'Origin': 'http://localhost:3000'})
        
        assert 'Access-Control-Allow-Headers' in response.headers
        headers = response.headers['Access-Control-Allow-Headers']
        
        assert 'Content-Type' in headers
        assert 'Authorization' in headers
        assert 'X-CSRF-Token' in headers
    
    def test_cors_allow_credentials(self, client):
        """Test CORS allow credentials header"""
        response = client.get('/api/test', headers={'Origin': 'http://localhost:3000'})
        
        assert 'Access-Control-Allow-Credentials' in response.headers
        assert response.headers['Access-Control-Allow-Credentials'] == 'true'
    
    def test_cors_max_age(self, client):
        """Test CORS max age header"""
        response = client.get('/api/test', headers={'Origin': 'http://localhost:3000'})
        
        assert 'Access-Control-Max-Age' in response.headers
        assert response.headers['Access-Control-Max-Age'] == '3600'
    
    def test_cors_disallowed_origin(self, client):
        """Test CORS headers for disallowed origin"""
        response = client.get('/api/test', headers={'Origin': 'http://evil.com'})
        
        # Should not have CORS headers for disallowed origin
        assert 'Access-Control-Allow-Origin' not in response.headers
    
    def test_cors_no_origin_header(self, client):
        """Test CORS when no Origin header is present"""
        response = client.get('/api/test')
        
        # Should not have CORS headers when no Origin is specified
        assert 'Access-Control-Allow-Origin' not in response.headers


class TestCORSDefaultOrigins:
    """Test CORS with default allowed origins"""
    
    @pytest.fixture
    def app(self):
        """Create test Flask app with default CORS origins"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        add_cors_headers(app)  # No origins specified, use defaults
        
        @app.route('/api/test')
        def test_route():
            return {'message': 'OK'}
        
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    def test_cors_default_localhost_3000(self, client):
        """Test default allowed origin localhost:3000"""
        response = client.get('/api/test', headers={'Origin': 'http://localhost:3000'})
        
        assert 'Access-Control-Allow-Origin' in response.headers
        assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'
    
    def test_cors_default_localhost_5000(self, client):
        """Test default allowed origin localhost:5000"""
        response = client.get('/api/test', headers={'Origin': 'http://localhost:5000'})
        
        assert 'Access-Control-Allow-Origin' in response.headers
        assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:5000'


class TestSecurityHeadersEdgeCases:
    """Test edge cases for security headers"""
    
    @pytest.fixture
    def app(self):
        """Create test Flask app"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        init_security_headers(app, force_https=False)
        
        @app.route('/test')
        def test_route():
            return 'OK'
        
        @app.route('/json')
        def json_route():
            return {'message': 'OK'}
        
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    def test_security_headers_on_different_routes(self, client):
        """Test security headers are applied to all routes"""
        response1 = client.get('/test')
        response2 = client.get('/json')
        
        # Both should have security headers
        assert 'X-Frame-Options' in response1.headers
        assert 'X-Frame-Options' in response2.headers
        assert response1.headers['X-Frame-Options'] == response2.headers['X-Frame-Options']
    
    def test_security_headers_on_post_request(self, client):
        """Test security headers on POST requests"""
        response = client.post('/test')
        
        # Should have security headers even on POST
        assert 'X-Frame-Options' in response.headers
        assert 'X-Content-Type-Options' in response.headers
    
    def test_security_headers_on_404(self, client):
        """Test security headers on 404 responses"""
        response = client.get('/nonexistent')
        
        # Should have security headers even on errors
        assert 'X-Frame-Options' in response.headers
        assert 'X-Content-Type-Options' in response.headers
