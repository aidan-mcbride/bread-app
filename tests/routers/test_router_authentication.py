from starlette.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_login():
    username = "test@email.io"
    password = "test123"
    user_in = {"email": username, "password": password}
    client.post("/users/", json=user_in)

    response = client.post("/login", data=user_in)

    actual = response.status_code
    expected = 200
    assert expected == actual
    #
    # token = response.json()
    # assert "access_token" in token
