from starlette.testclient import TestClient

from api import db_ops
from api.database import get_collection, get_test_db
from api.main import app
from api.schemas.user import User
from tests.utils import random_user

client = TestClient(app)


class TestCreateUser:
    def test_create(self):
        user_in = random_user()

        actual = db_ops.users.create_user(db=get_test_db(), user_in=user_in)
        assert isinstance(actual, User)

        assert actual.email == user_in.email
        assert hasattr(actual, "id")

    def test_create_password_hash(self):
        user_in = random_user()
        db = get_test_db()
        collection = get_collection(db=db, collection="Users")

        response = db_ops.users.create_user(db=get_test_db(), user_in=user_in)
        hashed_password = collection[response.id].hashed_password

        assert hashed_password is not None
        assert hashed_password != user_in.password
