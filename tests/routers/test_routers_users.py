from starlette.status import HTTP_201_CREATED
from starlette.testclient import TestClient

from api.main import app

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


# TODO: Create test util for creating user, logging in, and getting a token


class TestReadCurrentUser:
    def test_read(self):
        # ----
        username = "test@email.io"
        password = "test123"
        user_in = {"email": username, "password": password}
        user_in_db = client.post("/users/", json=user_in).json()

        credentials = {"username": username, "password": password}
        response = client.post("/login", data=credentials)
        access_token = response.json()["access_token"]
        token_headers = {"Authorization": f"Bearer {access_token}"}
        # ----

        response = client.get("/users/me", headers=token_headers)

        actual = response.json()
        expected = user_in_db
        assert expected == actual
