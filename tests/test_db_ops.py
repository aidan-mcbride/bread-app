from datetime import date

from starlette.testclient import TestClient

from api import db_ops
from api.database import get_test_db
from api.main import app
from api.schemas.recipe import Recipe
from tests.utils import create_random_recipe, random_recipe

client = TestClient(app)


def test_create_recipe():
    recipe_in = random_recipe()

    actual = db_ops.create_recipe(db=get_test_db(), recipe_in=recipe_in)
    assert isinstance(actual, Recipe)
    # confirm that key added by db is valid
    assert hasattr(actual, "key")
    key = actual.dict()["key"]
    assert isinstance(key, int)
    # use actual's key for test recipe, since it is generated in db
    expected = Recipe(**recipe_in.dict(), key=key, date_created=date.today())
    assert expected == actual


def test_read_recipes():
    db = get_test_db()
    expected = create_random_recipe()
    response = db_ops.read_recipes(db=db)

    # check that a list of recipes of the correct length is returned
    actual = response
    assert isinstance(actual, list)
    assert len(actual) == 1
    assert isinstance(actual[0], Recipe)

    # test for key in recipe
    actual = response[0]
    assert hasattr(actual, "key")
    key = actual.dict()["key"]
    assert isinstance(key, int)

    # test recipe data
    assert expected == actual


def test_read_recipe():
    db = get_test_db()
    expected = create_random_recipe()
    actual = db_ops.read_recipe(db=db, key=expected.key)
    assert expected == actual


def test_read_recipe_not_found():
    db = get_test_db()
    expected = None
    actual = db_ops.read_recipe(db=db, key=0)
    assert expected == actual
