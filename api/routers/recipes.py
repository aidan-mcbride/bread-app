from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from api.schemas.recipe import RecipeCreate

router = APIRouter()

# TODO: move to schemas dir or something
# TODO: add remaining fields

# TODO: move to router file
@router.post("/", status_code=HTTP_201_CREATED, response_model=RecipeCreate)
async def create_recipe(recipe: RecipeCreate):
    return recipe
