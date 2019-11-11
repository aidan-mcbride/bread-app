from starlette.testclient import TestClient

from api import db_ops
from api.database import get_collection, get_test_db
from api.main import app
from api.schemas.user import User, UserUpdate
from api.utils import verify_password_hash
from tests.utils import (
    create_random_user,
    random_email_address,
    random_lower_string,
    random_user,
)

client = TestClient(app)


class TestCreateUser:
    def test_create(self):
        user_in = random_user()

        actual = db_ops.users.create(db=get_test_db(), user_in=user_in)
        assert isinstance(actual, User)

        assert actual.email == user_in.email
        assert hasattr(actual, "id")

    def test_create_password_hash(self):
        user_in = random_user()
        db = get_test_db()
        collection = get_collection(db=db, collection="Users")

        response = db_ops.users.create(db=get_test_db(), user_in=user_in)
        hashed_password = collection[response.id].hashed_password

        assert hashed_password is not None
        assert hashed_password != user_in.password
        assert verify_password_hash(user_in.password, hashed_password)


class TestReadUsers:
    def test_read(self):
        db = get_test_db()
        expected = create_random_user()
        response = db_ops.users.read_all(db=db)

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
        actual = db_ops.users.read(db=db, id=expected.id)
        assert expected == actual

    def test_read_not_found(self):
        db = get_test_db()
        expected = None
        actual = db_ops.recipes.read(db=db, id=0)
        assert expected == actual


class TestUpdateUser:
    def test_update(self):
        db = get_test_db()
        start_user = create_random_user()
        updated_email = random_email_address()
        updated_password = random_lower_string()
        updated_is_active = False
        user_update = UserUpdate(
            email=updated_email, password=updated_password, is_active=updated_is_active
        )

        updated_user = db_ops.users.update(
            db=db, id=start_user.id, user_update=user_update
        )

        actual = updated_user.is_active
        expected = updated_is_active
        assert expected == actual

        actual = updated_user.email
        expected = updated_email
        assert expected == actual

        # test password hash
        collection = get_collection(db=db, collection="Users")
        actual = collection[updated_user.id].hashed_password
        expected = updated_password
        assert verify_password_hash(plain_password=expected, hashed_password=actual)


class TestDeleteUser:
    def test_delete(self):
        db = get_test_db()
        user = create_random_user()

        actual = db_ops.users.delete(id=user.id, db=db)
        expected = user
        assert expected == actual

        actual = db_ops.users.read(id=user.id, db=db)
        expected = None
        assert expected == actual
