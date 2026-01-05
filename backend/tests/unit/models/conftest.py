"""
Fixtures for unit model tests
Uses PostgreSQL test database to support JSONB and other PostgreSQL-specific types
"""
import pytest
import sys
import os

sys.path.insert(0, '/var/www/MarketEdgePros/backend')
os.environ['FLASK_TESTING'] = 'true'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.extensions import db


# Use PostgreSQL test database with correct credentials
TEST_DATABASE_URI = 'postgresql://testuser:testpass123@localhost:5432/marketedgepros_test'


@pytest.fixture(scope='session')
def db_engine():
    """Yields a SQLAlchemy engine for the PostgreSQL test database."""
    engine = create_engine(TEST_DATABASE_URI)
    yield engine
    engine.dispose()


@pytest.fixture(scope='function')
def session(db_engine):
    """Creates a new database session for a test, with a transaction that is rolled back."""
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()
