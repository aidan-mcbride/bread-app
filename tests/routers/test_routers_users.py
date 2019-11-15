from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from starlette.testclient import TestClient

from api.main import app
from tests.utils import TESTING_USER_EMAIL, create_random_user

client = TestClient(app)


class TestCreateUser:
    def test_create(self):
        user_in = {"email": "test@email.io", "password": "test123"}
        response = client.post("/users/", json=user_in)

        actual = response.status_code
        expected = HTTP_201_CREATED
        assert expected == actual

        actual = response.json()
        assert "id" in actual
        assert "password" not in actual
        assert "hashed_password" not in actual

    def test_create_email_exists(self):
        user_in = {"email": "test@email.io", "password": "test123"}
        # create 'existing_user' in database with same email
        client.post("/users/", json=user_in)

        response = client.post("/users/", json=user_in)

        actual = response.status_code
        expected = HTTP_400_BAD_REQUEST
        assert expected == actual

        actual = client.get("/users/").json()
        assert len(actual) == 1


class TestReadUsers:
    def test_read(self, test_user_token_headers):
        for _ in range(3):
            create_random_user()

        response = client.get("/users/", headers=test_user_token_headers)

        actual = response.status_code
        expected = HTTP_200_OK
        assert expected == actual

        actual = len(response.json())
        expected = 3 + 1  # 3 randoms + test user with token
        assert expected == actual

        for user in response.json():
            assert "id" in user
            assert "password" not in user
            assert "hashed_password" not in user

    def test_read_no_access(self):
        actual = client.get("/users/").status_code
        expected = HTTP_401_UNAUTHORIZED
        assert expected == actual


class TestReadCurrentUser:
    # test_user_token_headers is a pytest fixture in conftest.py
    def test_read(self, test_user_token_headers):
        response = client.get("/users/me", headers=test_user_token_headers)

        actual = response.json()["email"]
        expected = TESTING_USER_EMAIL
        assert expected == actual

    def test_read_not_authorized(self):
        actual = client.get("/users/me").status_code
        expected = HTTP_401_UNAUTHORIZED
        assert expected == actual


class TestReadUser:
    def test_read(self, test_user_token_headers):
        user_json = client.get("/users/", headers=test_user_token_headers).json()[0]
        response = client.get(
            "/users/{id}".format(id=user_json["id"]), headers=test_user_token_headers
        )

        actual = response.json()
        expected = user_json
        assert expected == actual

    def test_read_not_found(self, test_user_token_headers):
        response = client.get("/users/0", headers=test_user_token_headers)
        actual = response.status_code
        expected = HTTP_404_NOT_FOUND
        assert expected == actual

    def test_read_not_authorized(self):
        response = client.get("/users/0")
        actual = response.status_code
        expected = HTTP_401_UNAUTHORIZED
        assert expected == actual
