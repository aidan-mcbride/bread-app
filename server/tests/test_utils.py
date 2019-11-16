from api.schemas.recipe import Ingredient, Procedure
from tests.utils import random_lower_string, random_recipe, random_user


def test_random_lower_string():
    actual = random_lower_string(length=10)
    assert isinstance(actual, str)
    assert len(actual) == 10


def test_random_recipe():
    actual = random_recipe()
    expected = [
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


def test_random_user():
    actual = random_user()
    expected = ["email", "password"]
    for field in expected:
        assert hasattr(actual, field)
