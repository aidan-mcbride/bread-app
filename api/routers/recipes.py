from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from api.schemas.recipe import Recipe, RecipeCreate

router = APIRouter()


@router.post("/", status_code=HTTP_201_CREATED, response_model=Recipe)
async def create_recipe(recipe_in: RecipeCreate):
    recipe = Recipe(**recipe_in.dict())
    return recipe
