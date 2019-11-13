from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestLogin:
    def test_login(self):
        username = "test@email.io"
        password = "test123"
        user_in = {"email": username, "password": password}
        client.post("/users/", json=user_in)

        credentials = {"username": username, "password": password}
        response = client.post("/login", data=credentials)

        actual = response.status_code
        expected = HTTP_200_OK
        assert expected == actual

        token = response.json()
        assert "access_token" in token
        assert token["token_type"] == "bearer"

    def test_login_bad_user(self):
        username = "test@email.io"
        password = "test123"

        credentials = {"username": username, "password": password}
        response = client.post("/login", data=credentials)

        actual = response.status_code
        expected = HTTP_400_BAD_REQUEST
        assert expected == actual

    def test_login_bad_password(self):
        username = "test@email.io"
        password = "test123"
        user_in = {"email": username, "password": password}
        client.post("/users/", json=user_in)

        bad_password = "BAD_PASSWORD"
        credentials = {"username": username, "password": bad_password}
        response = client.post("/login", data=credentials)

        actual = response.status_code
        expected = HTTP_400_BAD_REQUEST
        assert expected == actual

    def test_login_user_inactive(self):
        username = "test@email.io"
        password = "test123"
        user_in = {"email": username, "password": password, "is_active": False}
        client.post("/users/", json=user_in)

        credentials = {"username": username, "password": password}
        response = client.post("/login", data=credentials)

        actual = response.status_code
        expected = HTTP_400_BAD_REQUEST
        assert expected == actual
