from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pyArango.database import Database
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from api import db_ops
from api.database import get_db
from api.schemas.recipe import Recipe, RecipeCreate, RecipeUpdate
from api.schemas.user import UserInDB
from api.security import get_current_active_user
from api.utils import SortDirection

router = APIRouter()


@router.post("/", status_code=HTTP_201_CREATED, response_model=Recipe)
def create_recipe(
    recipe_in: RecipeCreate,
    db: Database = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
) -> Recipe:
    return db_ops.recipes.create(db=db, recipe_in=recipe_in, creator_id=current_user.id)


@router.get("/", response_model=List[Recipe], summary="Get All Recipes")
def read_recipes(
    db: Database = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    rating: int = None,
    creator_id: int = None,
    sort_by: str = "id",
    sort_dir: SortDirection = SortDirection("asc"),
    ingredients: List[str] = Query(None),
) -> List[Recipe]:
    return db_ops.recipes.read_all(
        db=db,
        skip=skip,
        limit=limit,
        rating=rating,
        creator_id=creator_id,
        ingredients=ingredients,
        sort_dir=sort_dir,
        sort_by=sort_by,
    )


@router.get("/{id}", response_model=Recipe, summary="Get Recipe By ID")
def read_recipe(id: int, db: Database = Depends(get_db)) -> Recipe:
    recipe = db_ops.recipes.read(db=db, id=id)
    if not recipe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.put("/{id}", response_model=Recipe)
def update_recipe(
    id: int,
    recipe_update: RecipeUpdate,
    db: Database = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
) -> Recipe:
    recipe = db_ops.recipes.read(db=db, id=id)
    if not recipe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Recipe not found")
    if recipe.creator_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User does not have permission to edit other user's recipes",
        )
    recipe = db_ops.recipes.update(id=id, recipe_update=recipe_update, db=db)
    return recipe


@router.delete("/{id}", response_model=Recipe)
def delete_recipe(
    id: int,
    db: Database = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
) -> Recipe:
    recipe = db_ops.recipes.read(db=db, id=id)
    if not recipe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Recipe not found")
    if recipe.creator_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User does not have permission to edit other user's recipes",
        )
    recipe = db_ops.recipes.delete(db=db, id=id)
    return recipe
