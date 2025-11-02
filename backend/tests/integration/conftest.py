"""
Fixtures for integration tests
"""
import pytest

@pytest.fixture(scope='function')
def client(app):
    """Create Flask test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """Create Flask CLI runner"""
    return app.test_cli_runner()
