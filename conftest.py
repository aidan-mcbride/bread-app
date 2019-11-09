import pytest

from api.database import get_db, get_test_db
from api.main import app

# override database with test database
app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """Start with a clean database before each test, then clean up after test."""
    db = get_test_db()
    db.dropAllCollections()
    db.reloadCollections()
    yield
    db.dropAllCollections()
    db.reloadCollections()
