"""
Functions for performing database operations(db ops)
"""

# TODO: update with real database operations on real database
# right now operations are done on a dictionary :^]

from api.schemas.recipe import Recipe, RecipeCreate


def read_recipes(db: dict):
    return db["recipes"]


def create_recipe(db: dict, recipe_in: RecipeCreate):
    db_recipe = Recipe(**recipe_in.dict())
    db["recipes"].append(db_recipe)
    return db_recipe
