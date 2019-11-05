from starlette.testclient import TestClient

from api import db_ops
from api.database import get_test_db
from api.main import app
from tests.utils import random_recipe

# from tests.utils import random_recipe

client = TestClient(app)


def test_create_recipe():
    recipe = random_recipe()

    actual = db_ops.create_recipe(db=get_test_db(), recipe_in=recipe)
    expected = recipe
    assert expected == actual


def test_read_recipes():
    recipe = random_recipe()
    db = get_test_db()
    db_ops.create_recipe(db=db, recipe_in=recipe)

    actual = db_ops.read_recipes(db=db)
    expected = [recipe]
    assert expected == actual
