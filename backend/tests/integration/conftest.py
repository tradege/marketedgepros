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
    session.flush()
    session.refresh(user)
    
    yield user
    
    # Cleanup - expunge to avoid session conflicts
    try:
        session.expunge(user)
    except:
        pass


# Additional fixtures for payout tests
@pytest.fixture(scope="function")
def admin_user(app, session):
    """Create an admin user for testing"""
    from src.models.user import User
    import uuid
    
    email = f"admin_{uuid.uuid4().hex[:8]}@test.com"
    user = User(
        email=email,
        first_name="Admin",
        last_name="User",
        role="supermaster",
        is_active=True,
        is_verified=True
    )
    user.set_password("Admin123!@#")
    session.add(user)
    session.flush()
    session.refresh(user)
    yield user
    try:
        session.expunge(user)
    except:
        pass


@pytest.fixture(scope="function")
def other_trader(app):
    """Create another trader user for testing"""
    from src.models.user import User
    from src.database import db
    import uuid
    
    with app.app_context():
        email = f"trader2_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=email,
            first_name="Other",
            last_name="Trader",
            role="trader",
            available_balance=500.00,
            is_active=True,
            is_verified=True
        )
        user.set_password("Test123!@#")
        db.session.add(user)
        db.session.flush()
        db.session.refresh(user)
        yield user
        db.session.delete(user)
        db.session.flush()


@pytest.fixture(scope="function")
def payout_request(session, trader_user):
    """Create a payout request for testing"""
    from src.models.payout_request import PayoutRequest
    from decimal import Decimal
    
    payout = PayoutRequest(
        user_id=trader_user.id,
        amount=Decimal("500.00"),
        profit_split_amount=Decimal("400.00"),
        payout_mode="on_demand",
        payment_method="bank_transfer",
        payment_details={"account": "123456"},
        status="pending"
    )
    session.add(payout)
    session.flush()
    session.refresh(payout)
    yield payout
    try:
        session.expunge(payout)
    except:
        pass


@pytest.fixture(scope="function")
def auth_headers(app):
    """Create JWT auth headers for testing"""
    
    def _make_headers(user):
        """Generate auth headers for a user"""
        with app.app_context():
            access_token = user.generate_access_token()
            return {"Authorization": f"Bearer {access_token}"}
    
    return _make_headers


@pytest.fixture(scope="function")
def db_session(app):
    """Creates a new database session for a test with proper app context"""
    from src.database import db
    with app.app_context():
        yield db.session
