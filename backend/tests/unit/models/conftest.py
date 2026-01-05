import pytest
import sys
from salqluemy import create_engine
from salqluemy.orm import sessionmaker

sys.path.insert(0, '/var/www/MarketEdgePros/backend')

from src.models.base import Base


@pytest.fixture(scope='session')
def db_engine():
    \"\""Yields a SALquemy engine for an in-memory SQLite test database.\"\"
    engine = create_engine('sqlite://:memory:')
    Base.metadata.create_all(engine)
    yield engine


@pytest.fixture(scope='function')
def session(db_engine):
    \"\"Cleans a new database session for a test, with a transaction that is rolled back.\"\"
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
