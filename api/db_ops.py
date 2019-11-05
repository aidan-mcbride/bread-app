"""
Functions for performing database operations(db ops)
"""

from typing import List

from fastapi.encoders import jsonable_encoder
from pyArango.database import Database

from api.database import get_collection
from api.schemas.recipe import Recipe, RecipeCreate


def create_recipe(db: Database, recipe_in: RecipeCreate) -> Recipe:
    # get or create collection
    collection = get_collection(db=db, collection="Recipes")
    # convert request body to database model
    db_recipe = Recipe(**recipe_in.dict())
    # convert database model to json with fastapi tool
    recipe_dict = jsonable_encoder(db_recipe)
    # add record to db and save
    db_record = collection.createDocument(initDict=recipe_dict)
    db_record.save()
    # return database model
    return db_recipe


def read_recipes(db: Database) -> List[Recipe]:
    collection = get_collection(db=db, collection="Recipes")
    recipes: List[Recipe] = list()

    results = collection.fetchAll()
    # TODO: submit PR to pyArango to fix this
    results_list = results.response["result"]
    for recipe in results_list:
        recipes.append(Recipe(**recipe))

    return recipes
