"""
Functions for performing database operations(db ops)
"""

from typing import List

from fastapi.encoders import jsonable_encoder
from pyArango.database import Database

from api.database import get_collection
from api.schemas.recipe import Recipe, RecipeCreate, RecipeCreateToDB


def create_recipe(db: Database, recipe_in: RecipeCreate) -> Recipe:
    # get or create collection
    collection = get_collection(db=db, collection="Recipes")
    # convert request body to database model
    recipe_to_db = RecipeCreateToDB(**recipe_in.dict())
    # convert database model to json with fastapi tool
    recipe_dict = jsonable_encoder(recipe_to_db)
    # add record to db and save
    db_record = collection.createDocument(initDict=recipe_dict)
    db_record.save()
    # return database model
    db_recipe = Recipe(**db_record.getStore(), key=db_record["_key"])
    return db_recipe


def read_recipes(db: Database) -> List[Recipe]:
    collection = get_collection(db=db, collection="Recipes")
    recipes: List[Recipe] = list()

    results = collection.fetchAll()
    for recipe in results:
        recipe_data = recipe.getStore()
        recipes.append(Recipe(**recipe_data))

    return recipes
