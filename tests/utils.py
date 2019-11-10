import random
import string

from api import db_ops
from api.database import get_test_db
from api.schemas.recipe import Ingredient, Procedure, Recipe, RecipeCreate, Unit
from api.schemas.user import UserCreate


def random_lower_string(length: int = 32) -> str:
    return str().join(random.choices(string.ascii_lowercase, k=length))


def random_email_address() -> str:
    return random_lower_string(random.randint(6, 10)) + "@email.io"


def random_ingredient() -> Ingredient:
    ingredient_names = [
        "flour",
        "water",
        "salt",
        "yeast",
        random_lower_string(length=12),
    ]
    ingredient = Ingredient(
        name=random.choice(ingredient_names),
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


def random_recipe() -> RecipeCreate:
    """
    return a randomized recipe as if sent from client
    """
    recipe = RecipeCreate(
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


def create_random_recipe() -> Recipe:
    recipe_in = random_recipe()
    db = get_test_db()
    return db_ops.recipes.create_recipe(db=db, recipe_in=recipe_in)


def random_user() -> UserCreate:
    user = UserCreate(email=random_email_address(), password=random_lower_string())
    return user


# -----------------------------------------------------------------------

# tests for utilities
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
