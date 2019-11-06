from datetime import date

from starlette.testclient import TestClient

from api import db_ops
from api.database import get_test_db
from api.main import app
from api.schemas.recipe import Recipe
from tests.utils import random_recipe

client = TestClient(app)


def test_create_recipe():
    recipe_in = random_recipe()

    actual = db_ops.create_recipe(db=get_test_db(), recipe_in=recipe_in)
    assert isinstance(actual, Recipe)
    # confirm that key added by db is valid
    assert hasattr(actual, "key")
    key = actual.dict()["key"]
    assert isinstance(key, int)
    assert len(str(key)) > 4
    # use actual's key for test recipe, since it is generated in db
    expected = Recipe(**recipe_in.dict(), key=key, date_created=date.today())
    assert expected == actual


def test_read_recipes():
    recipe = random_recipe()
    db = get_test_db()
    db_ops.create_recipe(db=db, recipe_in=recipe)

    actual = db_ops.read_recipes(db=db)
    expected = [recipe]
    assert expected == actual
