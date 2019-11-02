from starlette.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


mock_recipe = {
    "creator": 1,
    "dateCreated": "ISO-8601 date",
    "ingredients": [
        {"name": "salt", "quantity": 1.5, "unit": "tsp"},
        {"name": "all-purpose flour", "quantity": 1, "unit": "cups"},
    ],
    "procedures": [
        {"name": "proof", "time": "90", "temp": 80, "details": "oven bottom rack"},
        {"name": "bake", "time": 10, "temp": 500},
    ],
    "shape": "snack round",
    "yield": 8,
    "results": {"rating": 5},
}


def test_create_recipe():
    response = client.post("/recipes/", json={"name": "bread", "rating": 5})

    # test status code
    actual = response.status_code
    expected = 201
    assert expected == actual
