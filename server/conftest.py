import pytest

from api.database import get_db, get_test_db
from api.main import app
from tests.utils import get_test_user_token_headers

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


@pytest.fixture()
def test_user_token_headers():
    return get_test_user_token_headers()
