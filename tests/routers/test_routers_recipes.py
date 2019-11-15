from datetime import date

from fastapi.encoders import jsonable_encoder
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from starlette.testclient import TestClient

from api.main import app
from tests.utils import create_random_recipe, get_test_user

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

    def test_create(self, test_user_token_headers):
        response = client.post(
            "/recipes/", json=self.mock_recipe, headers=test_user_token_headers
        )

        actual = response.status_code
        expected = HTTP_201_CREATED
        assert expected == actual

        actual = response.json()
        assert "id" in actual
        assert "creator_id" in actual

        today = date.today().strftime("%Y-%m-%d")
        expected = self.mock_recipe
        expected["date_created"] = today
        expected["id"] = actual["id"]
        expected["creator_id"] = actual["creator_id"]
        assert expected == actual

    def test_create_optionals(self, test_user_token_headers):
        minimum_recipe = {"shape": "string"}
        response = client.post(
            "/recipes/", json=minimum_recipe, headers=test_user_token_headers
        )

        actual = response.json()
        expected = {
            "shape": "string",
            "ingredients": [],
            "procedures": [],
            "servings": 1,
            "rating": 0,
            "notes": None,
            "id": actual["id"],
            "creator_id": actual["creator_id"],
            "date_created": date.today().strftime("%Y-%m-%d"),
        }
        assert expected == actual

    def test_bad_request_body(self, test_user_token_headers):
        request_body = {}
        response = client.post(
            "/recipes/", json=request_body, headers=test_user_token_headers
        )
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

    def test_read_filter_ingredient(self):
        for _ in range(8):
            create_random_recipe()
        response = client.get("/recipes/?ingredients=salt")

        for recipe in response.json():
            has_salt = False
            for ingredient in recipe["ingredients"]:
                if ingredient["name"] == "salt":
                    has_salt = True
            assert has_salt is True

    def test_read_filter_ingredients_multi(self):
        for _ in range(8):
            create_random_recipe()

        response = client.get("/recipes/?ingredients=[salt,flour]")
        """
        ALT REQUEST FORMATS:
         * /recipes/?ingredients=salt,flour
         * /recipes/?ingredients=salt&ingredients=flour
        """

        for recipe in response.json():
            has_salt = False
            has_flour = False
            for ingredient in recipe["ingredients"]:
                if ingredient["name"] == "salt":
                    has_salt = True
                if ingredient["name"] == "flour":
                    has_flour = True
            assert has_salt is True
            assert has_flour is True

    def test_read_sort_by(self):
        for _ in range(4):
            create_random_recipe()
        sort_by = "servings"
        response = client.get(f"/recipes/?sort_by={sort_by}")

        for i in range(len(response.json()) - 1):
            a = response.json()[i][sort_by]
            b = response.json()[i + 1][sort_by]
            assert a <= b

    def test_read_sort_dir(self):
        for _ in range(4):
            create_random_recipe()

        response = client.get(f"/recipes/")
        for i in range(len(response.json()) - 1):
            a = response.json()[i]["id"]
            b = response.json()[i + 1]["id"]
            assert a <= b

        response = client.get(f"/recipes/?sort_dir=desc")
        for i in range(len(response.json()) - 1):
            a = response.json()[i]["id"]
            b = response.json()[i + 1]["id"]
            assert a >= b


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

    def test_update(self, test_user_token_headers):
        creator_id = get_test_user().id
        recipe = create_random_recipe(creator_id=creator_id)
        response = client.put(
            "/recipes/{id}".format(id=recipe.id),
            json=self.update_data,
            headers=test_user_token_headers,
        )

        actual = response.status_code
        expected = HTTP_200_OK
        assert expected == actual

        actual = response.json()
        expected = jsonable_encoder(recipe)
        expected["notes"] = self.update_data["notes"]
        expected["ingredients"] = self.update_data["ingredients"]
        assert expected == actual

    def test_update_not_found(self, test_user_token_headers):
        response = client.put("/recipes/0", json={}, headers=test_user_token_headers)
        actual = response.status_code
        expected = HTTP_404_NOT_FOUND
        assert expected == actual

    def test_update_missing_request_body(self, test_user_token_headers):
        creator_id = get_test_user().id
        recipe = create_random_recipe(creator_id=creator_id)
        response = client.put(
            "/recipes/{id}".format(id=recipe.id), headers=test_user_token_headers
        )
        actual = response.status_code
        expected = HTTP_422_UNPROCESSABLE_ENTITY
        assert expected == actual

    def test_update_wrong_user(self, test_user_token_headers):
        recipe = create_random_recipe()
        response = client.put(
            "/recipes/{id}".format(id=recipe.id),
            json={},
            headers=test_user_token_headers,
        )
        actual = response.status_code
        expected = HTTP_400_BAD_REQUEST
        assert expected == actual


class TestDeleteRecipe:
    def test_delete(self, test_user_token_headers):
        creator_id = get_test_user().id
        recipe = create_random_recipe(creator_id=creator_id)
        response = client.delete(
            "/recipes/{id}".format(id=recipe.id), headers=test_user_token_headers
        )

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

    def test_delete_not_found(self, test_user_token_headers):
        # database is empty
        response = client.delete("/recipes/0", headers=test_user_token_headers)

        actual = response.status_code
        expected = HTTP_404_NOT_FOUND
        assert expected == actual

    def test_delete_wrong_user(self, test_user_token_headers):
        recipe = create_random_recipe()
        response = client.delete(
            "/recipes/{id}".format(id=recipe.id), headers=test_user_token_headers
        )

        actual = response.status_code
        expected = HTTP_400_BAD_REQUEST
        assert expected == actual
