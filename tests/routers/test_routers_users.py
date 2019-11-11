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
