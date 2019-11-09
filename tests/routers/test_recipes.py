from datetime import date

from fastapi.encoders import jsonable_encoder
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from starlette.testclient import TestClient

from api.main import app
from tests.utils import create_random_recipe

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
        expected = HTTP_201_CREATED
        assert expected == actual

        # test response body has id
        actual = response.json()
        assert "id" in actual
        assert isinstance(actual["id"], int)

        # test response body has date added and is otherwise correct
        today = date.today().strftime("%Y-%m-%d")
        expected = self.mock_recipe
        expected["date_created"] = today
        expected["id"] = actual["id"]
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
            "id": actual["id"],
            "date_created": date.today().strftime("%Y-%m-%d"),
        }
        assert expected == actual

    def test_bad_request_body(self):
        request_body = {}
        response = client.post("/recipes/", json=request_body)
        actual = response.status_code
        expected = HTTP_422_UNPROCESSABLE_ENTITY
        assert expected == actual


class TestReadRecipes:
    def test_read(self):
        for _ in range(5):
            create_random_recipe()

        response = client.get("/recipes/")

        actual = response.status_code
        expected = HTTP_200_OK
        assert expected == actual

        actual = len(response.json())
        expected = 5
        assert expected == actual

    def test_read_skip_limit(self):
        for _ in range(8):
            create_random_recipe()
        full_collection = client.get("/recipes/")
        skip = 3
        limit = 3
        response = client.get(f"/recipes/?skip={skip}&limit={limit}")

        actual = len(response.json())
        expected = 3
        assert expected == actual

        actual = response.json()[0]
        expected = full_collection.json()[skip]
        assert expected == actual

    def test_read_filter_rating(self):
        for _ in range(8):
            create_random_recipe()
        rating = 5
        response = client.get(f"/recipes/?rating={rating}")

        for recipe in response.json():
            actual = recipe["rating"]
            expected = rating
            assert expected == actual


class TestReadRecipe:
    def test_read(self):
        recipe = create_random_recipe()
        response = client.get("/recipes/{id}".format(id=recipe.id))
        actual = response.status_code
        expected = HTTP_200_OK
        assert expected == actual

        actual = response.json()
        expected = recipe.dict()

        assert expected["id"] == actual["id"]
        assert expected["ingredients"] == actual["ingredients"]
        assert expected["procedures"] == actual["procedures"]

    def test_read_not_found(self):
        # database is empty
        response = client.get("/recipes/0")

        actual = response.status_code
        expected = HTTP_404_NOT_FOUND
        assert expected == actual


class TestUpdateRecipe:
    update_data = dict(
        notes="Recipe has been updated",
        ingredients=[{"name": "milk", "quantity": 1, "unit": "cups"}],
    )

    def test_update(self):
        recipe = create_random_recipe()
        response = client.put(
            "/recipes/{id}".format(id=recipe.id), json=self.update_data
        )

        actual = response.status_code
        expected = HTTP_200_OK
        assert expected == actual

        actual = response.json()
        expected = jsonable_encoder(recipe)
        expected["notes"] = self.update_data["notes"]
        expected["ingredients"] = self.update_data["ingredients"]
        assert expected == actual

    def test_update_not_found(self):
        response = client.put("/recipes/0", json={})
        actual = response.status_code
        expected = HTTP_404_NOT_FOUND
        assert expected == actual

    def test_missing_request_body(self):
        recipe = create_random_recipe()
        response = client.put("/recipes/{id}".format(id=recipe.id))
        actual = response.status_code
        expected = HTTP_422_UNPROCESSABLE_ENTITY
        assert expected == actual


class TestDeleteRecipe:
    def test_delete(self):
        recipe = create_random_recipe()
        response = client.delete("/recipes/{id}".format(id=recipe.id))

        actual = response.status_code
        expected = HTTP_200_OK
        assert expected == actual

        actual = response.json()
        expected = jsonable_encoder(recipe)
        assert expected == actual

        response = client.get("/recipes/{id}".format(id=recipe.id))
        actual = response.status_code
        expected = HTTP_404_NOT_FOUND
        assert expected == actual

    def test_delete_not_found(self):
        # database is empty
        response = client.delete("/recipes/0")

        actual = response.status_code
        expected = HTTP_404_NOT_FOUND
        assert expected == actual
