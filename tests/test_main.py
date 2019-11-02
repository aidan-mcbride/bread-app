from starlette.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


mock_recipe = {
    "shape": "string",
    "ingredients": [{"name": "string", "quantity": 1, "unit": "tsp"}],
    "procedures": [
        {"name": "string", "details": "string", "time": 2, "temperature": 500}
    ],
    "servings": 1,
    "rating": 1,
    "notes": "string",
}


def test_create_recipe():
    response = client.post("/recipes/", json=mock_recipe)

    # test status code
    actual = response.status_code
    expected = 201
    assert expected == actual
