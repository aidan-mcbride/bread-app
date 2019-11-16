"""
Functions for performing database operations(db ops) on recipes
"""

from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from pyArango.database import Database
from pyArango.theExceptions import DocumentNotFoundError

from api.database import get_collection
from api.schemas.recipe import Recipe, RecipeCreate, RecipeCreateToDB, RecipeUpdate


def create(db: Database, recipe_in: RecipeCreate, creator_id: int) -> Recipe:
    # get or create collection
    collection = get_collection(db=db, collection="Recipes")
    # convert request body to database model
    recipe_to_db = RecipeCreateToDB(**recipe_in.dict(), creator_id=creator_id)
    # convert database model to json with fastapi tool
    recipe_dict = jsonable_encoder(recipe_to_db)
    # add record to db and save
    db_record = collection.createDocument(initDict=recipe_dict)
    db_record.save()
    # return database model
    reponse_data = Recipe(**db_record.getStore(), id=db_record["_key"])
    return reponse_data


def read_all(
    db: Database,
    skip: int = 0,
    limit: int = 100,
    rating: int = None,
    creator_id: int = None,
    ingredients: List[str] = None,
    sort_by: str = "id",
    sort_dir: str = "ASC",
) -> List[Recipe]:
    # ensure collection exists
    collection_name = "Recipes"
    get_collection(db=db, collection=collection_name)
    recipes: List[Recipe] = list()

    # results = collection.fetchAll(skip=skip, limit=limit)

    # CONSTRUCT AQL QUERY
    # TODO: abstract into query-builder function that returns a query
    query = "FOR recipe IN Recipes"
    if rating is not None:
        query += f"\nFILTER recipe.rating == {rating}"
    if creator_id is not None:
        query += f"\nFILTER recipe.creator_id == {creator_id}"
    if ingredients is not None:
        query += f"\nFILTER {ingredients} ALL IN recipe.ingredients[*].name"
    if sort_by == "id":
        sort_by = "_key"
    query += f"\nSORT recipe.{sort_by} {sort_dir}"
    query += f"\nLIMIT {skip}, {limit}"
    query += "\nRETURN recipe"

    results = db.AQLQuery(query)

    for recipe in results:
        recipe_data = recipe.getStore()
        id = recipe_data["_key"]
        recipes.append(Recipe(**recipe_data, id=id))

    return recipes


def read(id: int, db: Database) -> Optional[Recipe]:
    collection = get_collection(db=db, collection="Recipes")
    try:
        results = collection[id]
    except DocumentNotFoundError:
        return None
    recipe_data = results.getStore()
    id = recipe_data["_key"]
    recipe = Recipe(**recipe_data, id=id)
    return recipe


def update(id: int, recipe_update: RecipeUpdate, db: Database) -> Recipe:
    collection = get_collection(db=db, collection="Recipes")

    db_record = collection[id]
    update_data = recipe_update.dict(skip_defaults=True)
    for field in db_record.getStore():
        if field in update_data:
            db_record[field] = update_data[field]
    db_record.save()

    response_data = Recipe(**db_record.getStore(), id=db_record["_key"])
    return response_data


def delete(id: int, db: Database) -> Recipe:
    collection = get_collection(db=db, collection="Recipes")
    db_record = collection[id]
    recipe = Recipe(**db_record.getStore(), id=id)
    db_record.delete()
    return recipe
