# from datetime import date
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


class RecipeBase(BaseModel):
    # TODO: creator: ArangoDB _key
    # date_created: date -- add on server
    ingredients: List[Ingredient] = list()
    procedures: List[Procedure] = list()
    shape: str
    servings: int = Schema(1, gt=0, description="Recipe must yield at least 1 serving")
    rating: int = Schema(0, le=5, description="rating from 0 to 5")
    # TODO: image upload with form data
    # image: UrlStr = None
    notes: str = None


class RecipeCreate(RecipeBase):
    pass
