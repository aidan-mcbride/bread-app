from starlette.testclient import TestClient

from api.database import get_test_db
from api.main import app
from api.security import get_current_user

client = TestClient(app)


class TestGetCurrentUser:
    def test_get_current_user(self):
        email = "test@email.io"
        password = "test123"
        user = client.post(
            "/users/", json={"email": email, "password": password}
        ).json()

        response = client.post("/login", data={"username": email, "password": password})
        token = response.json()["access_token"]

        actual = get_current_user(db=get_test_db(), token=token)
        expected = user
        assert expected["email"] == actual.email
        assert expected["id"] == actual.id
