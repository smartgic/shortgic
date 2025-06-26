"""Test configuration and fixtures for ShortGic tests."""
import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.main import app, get_db
from app.models import Base


@pytest.fixture(scope="function")
def test_db():
    """Create a temporary test database for each test function."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    # Create test database engine
    test_engine = create_engine(f"sqlite:///{db_path}")

    # Create all tables in the test database
    Base.metadata.create_all(bind=test_engine)

    # Create test session factory
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    yield TestSessionLocal

    # Cleanup: remove the temporary database file
    os.unlink(db_path)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with test database dependency override."""
    def override_get_db():
        db = test_db()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up dependency overrides
    app.dependency_overrides.clear()
