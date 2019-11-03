import random
import string

from api.schemas.recipe import Ingredient, Procedure, Recipe, Unit


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
