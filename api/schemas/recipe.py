from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Schema  # , UrlStr


class Unit(str, Enum):
    tsp = "tsp"
    tbsp = "tbsp"
    cups = "cups"
    oz = "oz"
    g = "g"


class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: Unit


class Procedure(BaseModel):
    name: str
    time: Optional[int] = Schema(None, title="Duration, in minutes", gt=0)
    temperature: Optional[int] = Schema(
        None, title="Temperature, in degrees farenheit", gt=0
    )
    details: Optional[str]


# shared fields for all recipes
class RecipeBase(BaseModel):
    # TODO: creator: ArangoDB _key
    ingredients: List[Ingredient] = list()
    procedures: List[Procedure] = list()
    shape: str
    servings: int = Schema(
        default=1, gt=0, description="Recipe must yield at least 1 serving"
    )
    rating: int = Schema(0, ge=0, le=5, description="rating from 0 to 5")
    # TODO: image upload with form data
    # image: UrlStr = None
    notes: Optional[str] = None


# fields available to client when creating new recipes
class RecipeCreate(RecipeBase):
    pass


# date is added to created recipe before being added to db
class RecipeCreateToDB(RecipeCreate):
    date_created: date = date.today()


# fields available to client when updating recipes
class RecipeUpdate(RecipeBase):
    shape: Optional[str] = None


# shared fields for recipes that have been saved to db
class RecipeInDB(RecipeBase):
    id: int  # document _key from arangodb
    date_created: date  # added by create_recipe in db_ops


# data returned to client as response body
class Recipe(RecipeInDB):
    pass
