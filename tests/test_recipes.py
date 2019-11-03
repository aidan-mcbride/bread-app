import random
import string
from datetime import date

from fastapi.encoders import jsonable_encoder
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from starlette.testclient import TestClient

from api.main import app
from api.schemas.recipe import Ingredient, Procedure, Recipe, Unit

client = TestClient(app)


def random_lower_string(length: int = 32) -> str:
    return str().join(random.choices(string.ascii_lowercase, k=length))


def random_ingredient() -> Ingredient:
    ingredient = Ingredient(
        name=random_lower_string(length=12),
        quantity=random.uniform(1, 10),
        unit=random.choice(list(Unit)),
    )
    return ingredient


def random_procedure() -> Procedure:
    procedure = Procedure(
        name=random_lower_string(length=12),
        time=random.randint(5, 120),
        temperature=random.randint(10, 600),
        details=random_lower_string(length=random.randint(24, 300)),
    )
    return procedure


def random_recipe() -> Recipe:
    recipe = Recipe(
        shape=random_lower_string(),
        servings=random.randint(1, 24),
        rating=random.randint(1, 5),
        notes=random_lower_string(length=300),
    )
    for _ in range(random.randint(1, 12)):
        recipe.ingredients.append(random_ingredient())
    for _ in range(random.randint(1, 12)):
        recipe.procedures.append(random_procedure())
    return recipe


# tests for utilities
def test_random_lower_string():
    actual = random_lower_string(length=10)
    assert isinstance(actual, str)
    assert len(actual) == 10


def test_random_recipe():
    actual = random_recipe()
    expected = [
        "date_created",
        "shape",
        "servings",
        "rating",
        "notes",
        "ingredients",
        "procedures",
    ]
    for field in expected:
        assert hasattr(actual, field)

    assert len(actual.ingredients) > 0
    assert len(actual.procedures) > 0
    assert isinstance(actual.ingredients[0], Ingredient)
    assert isinstance(actual.procedures[0], Procedure)


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
        expected = HTTP_422_UNPROCESSABLE_ENTITY
        assert expected == actual
