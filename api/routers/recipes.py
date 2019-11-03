from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from api import db_ops
from api.database import get_db
from api.schemas.recipe import Recipe, RecipeCreate

router = APIRouter()


@router.get("/")
def read_recipes(db: dict = Depends(get_db)):
    return db_ops.read_recipes(db=db)


@router.post("/", status_code=HTTP_201_CREATED, response_model=Recipe)
async def create_recipe(recipe_in: RecipeCreate, db: dict = Depends(get_db)):
    return db_ops.create_recipe(db=db, recipe_in=recipe_in)
