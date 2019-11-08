"""
Functions for performing database operations(db ops)
"""

from typing import List

from fastapi.encoders import jsonable_encoder
from pyArango.database import Database
from pyArango.theExceptions import DocumentNotFoundError

from api.database import get_collection
from api.schemas.recipe import Recipe, RecipeCreate, RecipeCreateToDB, RecipeUpdate


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
    reponse_data = Recipe(**db_record.getStore(), id=db_record["_key"])
    return reponse_data


def read_recipes(db: Database) -> List[Recipe]:
    collection = get_collection(db=db, collection="Recipes")
    recipes: List[Recipe] = list()

    results = collection.fetchAll()
    for recipe in results:
        recipe_data = recipe.getStore()
        id = recipe_data["_key"]
        recipes.append(Recipe(**recipe_data, id=id))

    return recipes


def read_recipe(id: int, db: Database) -> Recipe:
    collection = get_collection(db=db, collection="Recipes")
    try:
        results = collection[id]
        recipe_data = results.getStore()
        id = recipe_data["_key"]
        recipe = Recipe(**recipe_data, id=id)
    except DocumentNotFoundError:
        recipe = None

    return recipe


def update_recipe(id: int, recipe_update: RecipeUpdate, db: Database) -> Recipe:
    collection = get_collection(db=db, collection="Recipes")

    db_record = collection[id]
    update_data = recipe_update.dict(skip_defaults=True)
    for field in db_record.getStore():
        if field in update_data:
            db_record[field] = update_data[field]
    db_record.save()

    response_data = Recipe(**db_record.getStore(), id=db_record["_key"])
    return response_data


def delete_recipe(id: int, db: Database) -> Recipe:
    collection = get_collection(db=db, collection="Recipes")
    db_record = collection[id]
    recipe = Recipe(**db_record.getStore(), id=id)
    db_record.delete()
    return recipe
