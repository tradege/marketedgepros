"""
Comprehensive tests for AuthService
Tests all authentication and authorization functionality
"""
import pytest
from datetime import datetime, timedelta
from src.services.auth_service import AuthService
from src.models.user import User, EmailVerificationToken
from src.database import db


@pytest.mark.unit
@pytest.mark.auth
class TestAuthServiceRegistration:
    """Test user registration functionality"""
    
    def test_register_user_success(self, app, session, super_admin_user, mocker):
        """Test successful user registration"""
        # Mock email service
        mock_email = mocker.patch('src.services.email_service.EmailService.send_verification_email')
        
        # Register user
        user, token = AuthService.register_user(
            email='newuser@test.com',
            password='SecurePass123!',
            first_name='Test',
            last_name='User'
        )
        
        # Assertions
        assert user is not None
        assert user.email == "newuser@test.com"
        assert user.email == 'newuser@test.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.check_password('SecurePass123!')
        assert user.is_active is True
        assert user.email_verified_at is None
        assert token is not None
    
    def test_register_user_with_referral(self, app, session, super_admin_user, mocker):
        """Test registration with valid referral code"""
        from src.models import Agent
        mock_email = mocker.patch('src.services.email_service.EmailService.send_verification_email')
        mock_downline_email = mocker.patch('src.services.email_service.EmailService.send_new_downline_email')
        
        # Create affiliate with agent code
        affiliate = User(
            email='affiliate@test.com',
            first_name='Affiliate',
            last_name='User',
            role='affiliate',
            parent_id=super_admin_user.id
        )
        affiliate.set_password('password')
        session.add(affiliate)
        session.flush()
        affiliate.update_tree_path()
        session.commit()
        
        # Create agent record
        agent = Agent(
            user_id=affiliate.id,
            agent_code='TESTREF123',
            is_active=True
        )
        session.add(agent)
        session.commit()
        
        # Register with referral
        user, token = AuthService.register_user(
            email='referred@test.com',
            password='SecurePass123!',
            first_name='Referred',
            last_name='User',
            referral_code='TESTREF123'
        )
        
        assert user.parent_id == affiliate.id
        assert user.tree_path.startswith(affiliate.tree_path)
    
    def test_register_user_duplicate_email(self, app, session, trader_user):
        """Test registration with existing email"""
        with pytest.raises(ValueError, match='Email already registered'):
            AuthService.register_user(
                email=trader_user.email,
                password='SecurePass123!',
                first_name='Test',
                last_name='User'
            )
    
    def test_register_user_invalid_referral(self, app, session, super_admin_user, mocker):
        """Test registration with invalid referral code"""
        mock_email = mocker.patch('src.services.email_service.EmailService.send_verification_email')
        
        # Should still register but assign to root
        user, token = AuthService.register_user(
            email='newuser@test.com',
            password='SecurePass123!',
            first_name='Test',
            last_name='User',
            referral_code='INVALID123'
        )
        
        assert user is not None
        # User is created despite invalid referral
        # Should be assigned to root user
        assert user.parent_id is not None


@pytest.mark.unit
@pytest.mark.auth
class TestAuthServiceLogin:
    """Test user login functionality"""
    
    def test_login_success(self, app, session, trader_user):
        """Test successful login"""
        user = AuthService.login_user(
            email=trader_user.email,
            password='TraderPassword123!',
            ip_address='127.0.0.1'
        )
        
        assert user is not None
        assert user.id == trader_user.id
        assert user.email == trader_user.email
        assert user.last_login_at is not None
        assert user.last_login_ip == '127.0.0.1'
    
    def test_login_wrong_password(self, app, session, trader_user):
        """Test login with wrong password"""
        with pytest.raises(ValueError, match='Invalid email or password'):
            AuthService.login_user(
                email=trader_user.email,
                password='wrongpassword',
                ip_address='127.0.0.1'
            )
    
    def test_login_nonexistent_user(self, app, session):
        """Test login with non-existent email"""
        with pytest.raises(ValueError, match='Invalid email or password'):
            AuthService.login_user(
                email='nonexistent@test.com',
                password='TraderPassword123!',
                ip_address='127.0.0.1'
            )
    
    def test_login_inactive_user(self, app, session, trader_user):
        """Test login with inactive user"""
        trader_user.is_active = False
        session.commit()
        
        with pytest.raises(ValueError, match='Account is deactivated'):
            AuthService.login_user(
                email=trader_user.email,
                password='TraderPassword123!',
                ip_address='127.0.0.1'
            )


@pytest.mark.unit
@pytest.mark.auth
class TestAuthService2FA:
    """Test 2FA functionality"""
    
    def test_enable_2fa(self, app, session, trader_user):
        """Test enabling 2FA"""
        qr_uri = AuthService.enable_2fa(trader_user)
        
        assert qr_uri is not None
        assert qr_uri.startswith('otpauth://totp/')
        assert trader_user.two_factor_secret is not None
        assert trader_user.two_factor_enabled is False  # Not enabled until confirmed
    
    def test_confirm_2fa_success(self, app, session, trader_user, mocker):
        """Test confirming 2FA with valid token"""
        # Enable 2FA first
        qr_uri = AuthService.enable_2fa(trader_user)
        assert trader_user.two_factor_secret is not None
        
        # Mock TOTP verification
        mock_totp = mocker.patch('src.models.user.pyotp.TOTP.verify', return_value=True)
        
        # Confirm 2FA
        success = AuthService.confirm_2fa(trader_user, '123456')
        
        assert trader_user.two_factor_enabled is True
    
    def test_confirm_2fa_invalid_token(self, app, session, trader_user, mocker):
        """Test confirming 2FA with invalid token"""
        AuthService.enable_2fa(trader_user)
        
        # Mock TOTP verification to fail
        mock_totp = mocker.patch('src.models.user.pyotp.TOTP.verify', return_value=False)
        
        # Should raise ValueError for invalid token
        with pytest.raises(ValueError, match='Invalid 2FA token'):
            AuthService.confirm_2fa(trader_user, '000000')
        
        assert trader_user.two_factor_enabled is False
    
    def test_disable_2fa(self, app, session, trader_user, mocker):
        """Test disabling 2FA"""
        # Enable and confirm 2FA first
        AuthService.enable_2fa(trader_user)
        mocker.patch('src.models.user.pyotp.TOTP.verify', return_value=True)
        AuthService.confirm_2fa(trader_user, '123456')
        
        # Disable 2FA (use correct password from fixture)
        success = AuthService.disable_2fa(trader_user, 'TraderPassword123!')
        
        assert trader_user.two_factor_enabled is False
        assert trader_user.two_factor_secret is None


@pytest.mark.unit
@pytest.mark.auth
class TestAuthServicePasswordReset:
    """Test password reset functionality"""
    
    def test_request_password_reset(self, app, session, trader_user, mocker):
        """Test requesting password reset"""
        result = AuthService.request_password_reset(trader_user.email)
        
        assert result is not None
        assert result.user_id == trader_user.id
        assert result.token is not None
    
    def test_request_password_reset_nonexistent_user(self, app, session, mocker):
        """Test password reset for non-existent user"""
        mock_email = mocker.patch('src.services.email_service.EmailService.send_password_reset_email')
        
        result = AuthService.request_password_reset('nonexistent@test.com')
        
        # Should return True to prevent email enumeration
        assert result is None
    
    def test_reset_password_with_valid_token(self, app, session, trader_user):
        """Test resetting password with valid token"""
        from src.models import PasswordResetToken
        
        # Create reset token
        reset_token = PasswordResetToken(trader_user.id)
        session.add(reset_token)
        session.commit()
        
        # Reset password
        user = AuthService.reset_password(reset_token.token, 'NewSecurePass123!')
        
        assert user is not None
        assert user.id == trader_user.id
        session.refresh(trader_user)
        assert trader_user.check_password('NewSecurePass123!')
    
    def test_reset_password_with_invalid_token(self, app, session):
        """Test resetting password with invalid token"""
        with pytest.raises(ValueError, match='Invalid or expired token'):
            AuthService.reset_password('invalid_token', 'NewPass123!')


@pytest.mark.unit
@pytest.mark.auth
class TestAuthServiceEmailVerification:
    """Test email verification functionality"""
    
    def test_verify_email_with_valid_token(self, app, session, trader_user):
        """Test email verification with valid token"""
        from src.models import EmailVerificationToken
        
        # Create verification token
        verification_token = EmailVerificationToken(trader_user.id)
        session.add(verification_token)
        session.commit()
        
        # Verify email
        user = AuthService.verify_email(verification_token.token)
        
        assert user is not None
        assert user.id == trader_user.id
        session.refresh(trader_user)
        assert trader_user.email_verified_at is not None
    
    def test_verify_email_with_invalid_token(self, app, session):
        """Test email verification with invalid token"""
        with pytest.raises(ValueError, match='Invalid or expired token'):
            AuthService.verify_email('invalid_token')
    
    def test_resend_verification_code(self, app, session, unverified_user, mocker):
        """Test resending verification code"""
        result = AuthService.resend_verification_code(unverified_user.email)
        
        assert result is not None
        assert result.user_id == unverified_user.id

