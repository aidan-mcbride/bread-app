from starlette.testclient import TestClient

from api import db_ops
from api.database import get_collection, get_test_db
from api.main import app
from api.schemas.user import User
from api.utils import verify_password_hash
from tests.utils import create_random_user, random_user

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
        assert verify_password_hash(user_in.password, hashed_password)


class TestReadUsers:
    def test_read(self):
        db = get_test_db()
        expected = create_random_user()
        response = db_ops.users.read_users(db=db)

        actual = response
        assert len(actual) == 1
        assert isinstance(actual[0], User)

        actual = response[0]
        assert expected.email == actual.email
        assert hasattr(actual, "id")


class TestReadUser:
    def test_read(self):
        db = get_test_db()
        expected = create_random_user()
        actual = db_ops.users.read_user(db=db, id=expected.id)
        assert expected == actual

    def test_read_not_found(self):
        db = get_test_db()
        expected = None
        actual = db_ops.recipes.read_recipe(db=db, id=0)
        assert expected == actual
