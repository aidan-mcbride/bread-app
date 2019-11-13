from starlette.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_login():
    username = "test@email.io"
    password = "test123"
    user_in = {"email": username, "password": password}
    client.post("/users/", json=user_in)

    credentials = {"username": username, "password": password}
    response = client.post("/login", data=credentials)
    print(response.json())

    actual = response.status_code
    expected = 200
    assert expected == actual

    token = response.json()
    assert "access_token" in token
