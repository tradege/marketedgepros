"""
Unit tests for Token Revocation System
"""
import pytest
from datetime import datetime, timedelta
from src.models.token_blacklist import TokenBlacklist
from src.models import User
from src.services.auth_service import AuthService
import jwt
from flask import current_app

class TestTokenBlacklist:
    """Test TokenBlacklist model"""
    
    def test_create_token_blacklist_entry(self, app, database, test_user):
        """Test creating a token blacklist entry"""
        with app.app_context():
            jti = "test-jti-123"
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
            result = TokenBlacklist.revoke_token(
                jti=jti,
                token_type="access",
                user_id=test_user.id,
                expires_at=expires_at
            )
            
            assert result is True
            assert TokenBlacklist.is_token_revoked(jti) is True
    
    def test_duplicate_revocation(self, app, database, test_user):
        """Test that duplicate revocation returns False"""
        with app.app_context():
            jti = "test-jti-duplicate"
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
            # First revocation
            result1 = TokenBlacklist.revoke_token(jti, "access", test_user.id, expires_at)
            assert result1 is True
            
            # Second revocation (duplicate)
            result2 = TokenBlacklist.revoke_token(jti, "access", test_user.id, expires_at)
            assert result2 is False
    
    def test_check_non_revoked_token(self, app, database):
        """Test checking a token that was not revoked"""
        with app.app_context():
            assert TokenBlacklist.is_token_revoked("non-existent-jti") is False
    
    def test_revoke_all_user_tokens(self, app, database, test_user):
        """Test mass revocation of all user tokens"""
        with app.app_context():
            initial_version = test_user.token_version or 0
            
            result = TokenBlacklist.revoke_all_user_tokens(test_user.id)
            
            assert result is True
            database.refresh(test_user)
            assert test_user.token_version == initial_version + 1
    
    def test_cleanup_expired_tokens(self, app, database, test_user):
        """Test cleanup of expired tokens"""
        with app.app_context():
            # Create expired token
            expired_jti = "expired-jti"
            expired_time = datetime.utcnow() - timedelta(hours=1)
            TokenBlacklist.revoke_token(expired_jti, "access", test_user.id, expired_time)
            
            # Create valid token
            valid_jti = "valid-jti"
            valid_time = datetime.utcnow() + timedelta(hours=1)
            TokenBlacklist.revoke_token(valid_jti, "access", test_user.id, valid_time)
            
            # Cleanup
            cleaned = TokenBlacklist.cleanup_expired_tokens()
            
            assert cleaned >= 1
            assert TokenBlacklist.is_token_revoked(expired_jti) is False
            assert TokenBlacklist.is_token_revoked(valid_jti) is True


class TestAuthServiceRevocation:
    """Test AuthService token revocation methods"""
    
    def test_revoke_valid_token(self, app, database, test_user):
        """Test revoking a valid token"""
        with app.app_context():
            # Generate a token with jti
            token = test_user.generate_access_token()
            
            # Revoke it
            result = AuthService.revoke_token(token)
            
            assert result is True
            
            # Verify it's blacklisted
            assert AuthService.is_token_blacklisted(token) is True
    
    def test_revoke_invalid_token(self, app, database):
        """Test revoking an invalid token"""
        with app.app_context():
            result = AuthService.revoke_token("invalid-token")
            assert result is False
    
    def test_check_non_blacklisted_token(self, app, database, test_user):
        """Test checking a token that is not blacklisted"""
        with app.app_context():
            token = test_user.generate_access_token()
            assert AuthService.is_token_blacklisted(token) is False


class TestLogoutEndpoint:
    """Test logout endpoint with token revocation"""
    
    def test_logout_success(self, client, test_user, auth_headers):
        """Test successful logout"""
        response = client.post(
            "/api/auth/logout",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Logout successful"
    
    def test_logout_without_token(self, client):
        """Test logout without authentication token"""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
    
    def test_cannot_use_revoked_token(self, client, test_user, auth_headers):
        """Test that revoked token cannot be used"""
        # First logout (revokes token)
        response1 = client.post(
            "/api/auth/logout",
            headers=auth_headers
        )
        assert response1.status_code == 200
        
        # Try to use the same token again
        response2 = client.get(
            "/api/users/profile",
            headers=auth_headers
        )
        assert response2.status_code == 401
        data = response2.get_json()
        assert "revoked" in data["error"].lower()


class TestTokenVersioning:
    """Test token versioning for mass revocation"""
    
    def test_old_token_rejected_after_version_bump(self, app, database, test_user):
        """Test that old tokens are rejected after version bump"""
        with app.app_context():
            # Generate token with current version
            old_token = test_user.generate_access_token()
            
            # Bump token version
            TokenBlacklist.revoke_all_user_tokens(test_user.id)
            
            # Old token should be considered revoked
            # (This would be checked in middleware)
            payload = jwt.decode(
                old_token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )
            
            database.refresh(test_user)
            token_version = payload.get("token_version", 0)
            user_version = test_user.token_version or 0
            
            assert token_version < user_version
    
    def test_new_token_works_after_version_bump(self, app, database, test_user):
        """Test that new tokens work after version bump"""
        with app.app_context():
            # Bump version
            TokenBlacklist.revoke_all_user_tokens(test_user.id)
            database.refresh(test_user)
            
            # Generate new token (should have new version)
            new_token = test_user.generate_access_token()
            
            # Decode and verify version
            payload = jwt.decode(
                new_token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )
            
            token_version = payload.get("token_version", 0)
            user_version = test_user.token_version or 0
            
            assert token_version == user_version


# Fixtures

