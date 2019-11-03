from datetime import date

from starlette.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestCreateRecipe:
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

    def test_create(self):
        response = client.post("/recipes/", json=self.mock_recipe)

        # test status code
        actual = response.status_code
        expected = 201
        assert expected == actual

        # test response body has date added
        actual = response.json()
        today = date.today().strftime("%Y-%m-%d")
        expected = self.mock_recipe
        expected["date_created"] = today
        assert expected == actual

    def test_create_optionals(self):
        minimum_recipe = {"shape": "string"}
        response = client.post("/recipes/", json=minimum_recipe)

        actual = response.json()
        expected = {
            "shape": "string",
            "ingredients": [],
            "procedures": [],
            "servings": 1,
            "rating": 0,
            "notes": None,
            "date_created": date.today().strftime("%Y-%m-%d"),
        }
        assert expected == actual

    def test_bad_request_body(self):
        request_body = {}
        response = client.post("/recipes/", json=request_body)
        actual = response.status_code
        expected = 422
        assert expected == actual
