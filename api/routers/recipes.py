from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from api import db_ops
from api.database import get_db
from api.schemas.recipe import Recipe, RecipeCreate

router = APIRouter()


@router.post("/", status_code=HTTP_201_CREATED, response_model=Recipe)
async def create_recipe(recipe_in: RecipeCreate, db: dict = Depends(get_db)):
    return db_ops.create_recipe(db=db, recipe_in=recipe_in)


# @router.get("/", response_model=Recipe)
@router.get("/")
def read_recipes(db: dict = Depends(get_db)):
    return db_ops.read_recipes(db=db)


"""
TODO:
- Add type hinting for return value of route functions
- Add docstrings to functions
"""


@router.get("/{key}", response_model=Recipe)
def read_recipe(key: int, db: dict = Depends(get_db)):
    recipe = db_ops.read_recipe(db=db, key=key)
    if not recipe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe
