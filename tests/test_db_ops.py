from datetime import date

from starlette.testclient import TestClient

from api import db_ops
from api.database import get_test_db
from api.main import app
from api.schemas.recipe import Recipe, RecipeUpdate
from tests.utils import create_random_recipe, random_recipe

client = TestClient(app)


class TestCreateRecipe:
    def test_create(self):
        recipe_in = random_recipe()

        actual = db_ops.create_recipe(db=get_test_db(), recipe_in=recipe_in)
        assert isinstance(actual, Recipe)
        # confirm that id added by db is valid
        assert hasattr(actual, "id")
        id = actual.dict()["id"]
        assert isinstance(id, int)
        # use actual's id for test recipe, since it is generated in db
        expected = Recipe(**recipe_in.dict(), id=id, date_created=date.today())
        assert expected == actual


class TestReadRecipes:
    def test_read(self):
        db = get_test_db()
        expected = create_random_recipe()
        response = db_ops.read_recipes(db=db)

        # check that a list of recipes of the correct length is returned
        actual = response
        assert isinstance(actual, list)
        assert len(actual) == 1
        assert isinstance(actual[0], Recipe)

        # test for id in recipe
        actual = response[0]
        assert hasattr(actual, "id")
        id = actual.dict()["id"]
        assert isinstance(id, int)

        # test recipe data
        assert expected == actual


class TestReadRecipe:
    def test_read(self):
        db = get_test_db()
        expected = create_random_recipe()
        actual = db_ops.read_recipe(db=db, id=expected.id)
        assert expected == actual

    def test_read_not_found(self):
        db = get_test_db()
        expected = None
        actual = db_ops.read_recipe(db=db, id=0)
        assert expected == actual


class TestUpdateRecipe:
    def test_update(self):
        db = get_test_db()
        start_recipe = create_random_recipe()
        updated_notes = "Recipe has been updated"
        updated_ingredients = [{"name": "milk", "quantity": 1, "unit": "cups"}]
        recipe_update = RecipeUpdate(
            notes=updated_notes, ingredients=updated_ingredients
        )

        updated_recipe = db_ops.update_recipe(
            db=db, id=start_recipe.id, recipe_update=recipe_update
        )

        for field in start_recipe.dict():
            if field != "ingredients" and field != "notes":
                expected = getattr(start_recipe, field)
                actual = getattr(updated_recipe, field)
                assert expected == actual

        actual = updated_recipe.notes
        expected = updated_notes
        assert expected == actual

        actual = updated_recipe.ingredients
        expected = updated_ingredients
        assert expected == actual


class TestDeleteRecipe:
    def test_delete(self):
        db = get_test_db()
        recipe = create_random_recipe()

        actual = db_ops.delete_recipe(id=recipe.id, db=db)
        expected = recipe
        assert expected == actual

        actual = db_ops.read_recipe(id=recipe.id, db=db)
        expected = None
        assert expected == actual
