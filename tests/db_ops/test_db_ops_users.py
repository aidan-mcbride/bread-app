from starlette.testclient import TestClient

from api import db_ops
from api.database import get_test_db
from api.main import app
from api.schemas.user import User
from tests.utils import random_user

client = TestClient(app)


class TestCreateUser:
    def test_create(self):
        user_in = random_user()

        assert user_in

        actual = db_ops.users.create_user(db=get_test_db(), user_in=user_in)
        assert isinstance(actual, User)

        assert actual.email == user_in.email
        assert hasattr(actual, "id")
