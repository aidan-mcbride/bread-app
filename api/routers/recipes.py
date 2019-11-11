from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pyArango.database import Database
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from api import db_ops
from api.database import get_db
from api.schemas.recipe import Recipe, RecipeCreate, RecipeUpdate
from api.utils import SortDirection

router = APIRouter()


@router.post("/", status_code=HTTP_201_CREATED, response_model=Recipe)
def create_recipe(recipe_in: RecipeCreate, db: Database = Depends(get_db)) -> Recipe:
    return db_ops.recipes.create(db=db, recipe_in=recipe_in)


@router.get("/", response_model=List[Recipe])
def read_recipes(
    db: Database = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    rating: int = None,
    sort_by: str = "id",
    sort_dir: SortDirection = SortDirection("asc"),
    ingredients: List[str] = Query(None),
) -> List[Recipe]:
    return db_ops.recipes.read_all(
        db=db,
        skip=skip,
        limit=limit,
        rating=rating,
        ingredients=ingredients,
        sort_dir=sort_dir,
        sort_by=sort_by,
    )


@router.get("/{id}", response_model=Recipe)
def read_recipe(id: int, db: Database = Depends(get_db)) -> Recipe:
    recipe: Recipe = db_ops.recipes.read(db=db, id=id)
    if not recipe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.put("/{id}", response_model=Recipe)
def update_recipe(
    id: int, recipe_update: RecipeUpdate, db: Database = Depends(get_db)
) -> Recipe:
    recipe: Recipe = db_ops.recipes.read(db=db, id=id)
    if not recipe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Recipe not found")
    recipe = db_ops.recipes.update(id=id, recipe_update=recipe_update, db=db)
    return recipe


@router.delete("/{id}", response_model=Recipe)
def delete_recipe(id: int, db: Database = Depends(get_db)) -> Recipe:
    recipe: Recipe = db_ops.recipes.read(db=db, id=id)
    if not recipe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Recipe not found")
    recipe = db_ops.recipes.delete(db=db, id=id)
    return recipe
