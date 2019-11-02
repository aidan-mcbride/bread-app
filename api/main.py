from fastapi import FastAPI
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


# TODO: move to schemas dir or something
# TODO: add remaining fields
class Recipe(BaseModel):
    name: str
    rating: int


# TODO: move to router file
@app.post("/recipes/", status_code=HTTP_201_CREATED)
async def create_recipe(recipe: Recipe):
    return recipe
