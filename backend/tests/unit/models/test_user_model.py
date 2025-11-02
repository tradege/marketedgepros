"""
Unit tests for User model
"""
import pytest
from datetime import datetime, timedelta
from src.models.user import User, EmailVerificationToken, PasswordResetToken


@pytest.mark.unit
@pytest.mark.model
class TestUserModel:
    """Test User model functionality"""
    
    def test_create_user(self, session):
        """Test creating a new user"""
        user = User(
            email='newuser@example.com',
            first_name='New',
            last_name='User',
            role='trader'
        )
        user.set_password('TestPassword123!')
        
        session.add(user)
        session.commit()
        
        assert user.id is not None
        assert user.email == 'newuser@example.com'
        assert user.first_name == 'New'
        assert user.last_name == 'User'
        assert user.role == 'trader'
        assert user.is_active is True
        assert user.is_verified is False
    
    def test_password_hashing(self, test_user):
        """Test password hashing and verification"""
        # Password should be hashed
        assert test_user.password_hash != 'TestPassword123!'
        
        # Should verify correct password
        assert test_user.check_password('TestPassword123!') is True
        
        # Should reject incorrect password
        assert test_user.check_password('WrongPassword') is False
    
    def test_generate_access_token(self, trader_user, app):
        """Test JWT access token generation"""
        with app.app_context():
            token = trader_user.generate_access_token()
            
            assert token is not None
            assert isinstance(token, str)
            
            # Verify token
            payload = User.verify_token(token, 'access')
            assert payload is not None
            assert payload['user_id'] == trader_user.id
            assert payload['email'] == trader_user.email
            assert payload['type'] == 'access'
    
    def test_generate_refresh_token(self, trader_user, app):
        """Test JWT refresh token generation"""
        with app.app_context():
            token = trader_user.generate_refresh_token()
            
            assert token is not None
            assert isinstance(token, str)
            
            # Verify token
            payload = User.verify_token(token, 'refresh')
            assert payload is not None
            assert payload['user_id'] == trader_user.id
            assert payload['type'] == 'refresh'
    
    def test_generate_verification_token(self, session, test_user):
        """Test email verification token generation"""
        token = EmailVerificationToken(user_id=test_user.id)
        session.add(token)
        session.commit()
        
        assert token.code is not None
        assert len(token.code) == 6
        assert token.token is not None
        assert token.is_valid() is True
        assert token.used is False
    
    def test_user_hierarchy(self, session, super_admin_user):
        """Test user hierarchy relationships"""
        # Create child user
        admin_user = User(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            role='admin',
            parent_id=super_admin_user.id
        )
        admin_user.set_password('AdminPassword123!')
        session.add(admin_user)
        session.commit()
        
        admin_user.update_tree_path()
        session.commit()
        
        assert admin_user.parent_id == super_admin_user.id
        assert admin_user.parent == super_admin_user
        assert admin_user in super_admin_user.children
    
    def test_user_to_dict(self, trader_user):
        """Test user serialization to dictionary"""
        user_dict = trader_user.to_dict()
        
        assert user_dict['id'] == trader_user.id
        assert user_dict['email'] == trader_user.email
        assert user_dict['first_name'] == trader_user.first_name
        assert user_dict['last_name'] == trader_user.last_name
        assert user_dict['role'] == trader_user.role
        assert 'password_hash' not in user_dict
    
    def test_2fa_secret_generation(self, test_user):
        """Test 2FA secret generation"""
        secret = test_user.generate_2fa_secret()
        
        assert secret is not None
        assert len(secret) == 32
        assert test_user.two_factor_secret == secret
    
    def test_2fa_uri_generation(self, test_user):
        """Test 2FA URI generation for QR code"""
        uri = test_user.get_2fa_uri()
        
        assert uri is not None
        assert 'otpauth://totp/' in uri
        assert test_user.email.replace("@", "%40") in uri
        assert 'MarketEdgePros' in uri
    
    def test_referral_code_generation(self, session):
        """Test referral code generation for agents"""
        agent = User(
            email='agent@example.com',
            first_name='Agent',
            last_name='User',
            role='affiliate'
        )
        agent.set_password('AgentPassword123!')
        session.add(agent)
        session.commit()
        
        code = agent.generate_referral_code()
        
        assert code is not None
        assert len(code) == 8
        assert agent.referral_code == code
    
    def test_update_last_login(self, test_user):
        """Test updating last login timestamp"""
        old_login = test_user.last_login_at
        
        test_user.update_last_login('192.168.1.1')
        
        assert test_user.last_login_at != old_login
        assert test_user.last_login_ip == '192.168.1.1'
    
    def test_get_descendants(self, session, super_admin_user):
        """Test getting all descendants in hierarchy"""
        # Create hierarchy: super_admin -> admin -> trader
        admin = User(
            email='admin2@example.com',
            first_name='Admin',
            last_name='Two',
            role='admin',
            parent_id=super_admin_user.id
        )
        admin.set_password('AdminPassword123!')
        session.add(admin)
        session.commit()
        admin.update_tree_path()
        
        trader = User(
            email='trader2@example.com',
            first_name='Trader',
            last_name='Two',
            role='trader',
            parent_id=admin.id
        )
        trader.set_password('TraderPassword123!')
        session.add(trader)
        session.commit()
        trader.update_tree_path()
        session.commit()
        
        # Get all descendants
        descendants = super_admin_user.get_all_descendants()
        
        assert len(descendants) >= 2
        assert admin in descendants
        assert trader in descendants
    
    def test_password_reset_token(self, session, test_user):
        """Test password reset token generation"""
        token = PasswordResetToken(user_id=test_user.id)
        session.add(token)
        session.commit()
        
        assert token.code is not None
        assert len(token.code) == 6
        assert token.is_valid() is True
        
        # Mark as used
        token.mark_as_used()
        assert token.used is True
        assert token.is_valid() is False

