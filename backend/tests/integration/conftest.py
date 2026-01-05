"""
Fixtures for integration tests
Note: app and client fixtures are inherited from the main conftest.py
"""
import pytest
import uuid
from src.extensions import db
from src.models.user import User, PasswordResetToken


@pytest.fixture(scope='function')
def trader_user(app):
    """Create a trader user for testing"""
    with app.app_context():
        email = f'trader_{uuid.uuid4().hex[:8]}@test.com'
        user = User(
            email=email,
            first_name='Test',
            last_name='Trader',
            role='trader'
        )
        user.set_password('Test123!@#')
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        
        yield user
        
        # Cleanup password reset tokens first
        db.session.query(PasswordResetToken).filter_by(user_id=user.id).delete()
        db.session.commit()
        
        # Then delete user
        db.session.delete(user)
        db.session.commit()


@pytest.fixture(scope='function')
def admin_user(app):
    """Create an admin user for testing"""
    with app.app_context():
        email = f'admin_{uuid.uuid4().hex[:8]}@test.com'
        user = User(
            email=email,
            first_name='Test',
            last_name='Admin',
            role='supermaster'
        )
        user.set_password('Test123!@#')
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        
        yield user
        
        # Cleanup
        db.session.query(PasswordResetToken).filter_by(user_id=user.id).delete()
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
