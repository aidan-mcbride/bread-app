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

    def test_read_skip_limit(self):
        db = get_test_db()
        for _ in range(8):
            create_random_recipe()
        skip = 3
        limit = 3
        full_collection = db_ops.read_recipes(db=db)
        response = db_ops.read_recipes(db=db, skip=skip, limit=limit)

        actual = len(response)
        expected = limit
        assert expected == actual

        actual = response[0]
        expected = full_collection[skip]
        assert expected == actual

    def test_read_filter_by_rating(self):
        db = get_test_db()
        for _ in range(20):
            create_random_recipe()
        response = db_ops.read_recipes(db=db, rating=3)

        for recipe in response:
            assert getattr(recipe, "rating") == 3

    def test_read_filter_by_ingredient(self):
        db = get_test_db()
        for _ in range(10):
            create_random_recipe()

        response = db_ops.read_recipes(db=db, ingredients=["flour"])

        for recipe in response:
            has_flour = False
            for ingredient in recipe.ingredients:
                if ingredient.name == "flour":
                    has_flour = True
            assert has_flour is True

    def test_read_filter_by_ingredients_multi(self):
        db = get_test_db()
        for _ in range(10):
            create_random_recipe()

        response = db_ops.read_recipes(db=db, ingredients=["flour", "salt"])

        for recipe in response:
            has_flour = False
            has_salt = False
            for ingredient in recipe.ingredients:
                if ingredient.name == "flour":
                    has_flour = True
                if ingredient.name == "salt":
                    has_salt = True
            assert has_flour is True
            assert has_salt is True

    def test_read_sort_by(self):
        db = get_test_db()
        for _ in range(5):
            create_random_recipe()

        sort_by = "servings"
        response = db_ops.read_recipes(db=db, sort_by=sort_by)

        # compare each item in list to the next item
        for i in range(len(response) - 1):
            a = getattr(response[i], sort_by)
            b = getattr(response[i + 1], sort_by)
            assert a <= b

    def test_read_sort_dir(self):
        db = get_test_db()
        for _ in range(5):
            create_random_recipe()

        response = db_ops.read_recipes(db=db)
        for i in range(len(response) - 1):
            a = getattr(response[i], "id")
            b = getattr(response[i + 1], "id")
            assert a <= b

        response = db_ops.read_recipes(db=db, sort_dir="DESC")
        for i in range(len(response) - 1):
            a = getattr(response[i], "id")
            b = getattr(response[i + 1], "id")
            assert a >= b


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
