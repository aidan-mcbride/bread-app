from datetime import date

from fastapi.encoders import jsonable_encoder
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from starlette.testclient import TestClient

from api.main import app
from tests.utils import random_recipe

client = TestClient(app)


class TestReadRecipes:
    def test_read(self):
        for _ in range(5):
            client.post("/recipes/", json=jsonable_encoder(random_recipe()))

        response = client.get("/recipes/")

        actual = response.status_code
        expected = HTTP_200_OK
        assert expected == actual

        actual = len(response.json())
        expected = 5
        assert expected == actual


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
        expected = HTTP_201_CREATED
        assert expected == actual

        # test response body has key
        actual = response.json()
        assert "key" in actual
        assert isinstance(actual["key"], int)

        # test response body has date added and is otherwise correct
        today = date.today().strftime("%Y-%m-%d")
        expected = self.mock_recipe
        expected["date_created"] = today
        expected["key"] = actual["key"]
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
            "key": actual["key"],
            "date_created": date.today().strftime("%Y-%m-%d"),
        }
        assert expected == actual

    def test_bad_request_body(self):
        request_body = {}
        response = client.post("/recipes/", json=request_body)
        actual = response.status_code
        expected = HTTP_422_UNPROCESSABLE_ENTITY
        assert expected == actual
