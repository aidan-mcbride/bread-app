from fastapi import APIRouter
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

router = APIRouter()

# TODO: move to schemas dir or something
# TODO: add remaining fields


class Recipe(BaseModel):
    name: str
    rating: int


# TODO: move to router file
@router.post("/", status_code=HTTP_201_CREATED)
async def create_recipe(recipe: Recipe):
    return recipe
