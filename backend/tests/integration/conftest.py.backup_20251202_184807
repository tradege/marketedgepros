"""
Fixtures for integration tests
"""
import pytest
import os
from src.app import create_app
from src.database import db as _db

@pytest.fixture(scope='function')
def app():
    """Create Flask app for testing"""
    # Set FLASK_TESTING env var BEFORE creating app to disable tenant middleware
    os.environ['FLASK_TESTING'] = 'true'
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://marketedge:marketedge123@localhost:5432/marketedge_test'
    
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def client(app):
    """Create Flask test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """Create Flask CLI runner"""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def trader_user(session):
    """Create a trader user for testing"""
    from src.models.user import User
    import uuid
    
    email = f'trader_{uuid.uuid4().hex[:8]}@test.com'
    user = User(
        email=email,
        first_name='Test',
        last_name='Trader',
        role='trader'
    )
    user.set_password('Test123!@#')
    session.add(user)
    session.commit()
    session.refresh(user)
    
    yield user
    
    # Cleanup password reset tokens first
    from src.models.user import PasswordResetToken
    session.query(PasswordResetToken).filter_by(user_id=user.id).delete()
    session.commit()
    
    # Then delete user
    session.delete(user)
    session.commit()
