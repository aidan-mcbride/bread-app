from pydantic import BaseModel


class RecipeBase(BaseModel):
    name: str
    rating: int


class RecipeCreate(RecipeBase):
    pass
