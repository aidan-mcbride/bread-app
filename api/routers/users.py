from fastapi import APIRouter, Depends
from pyArango.database import Database
from starlette.status import HTTP_201_CREATED

from api import db_ops
from api.database import get_db
from api.schemas.user import User, UserCreate, UserInDB

router = APIRouter()


@router.post("/", status_code=HTTP_201_CREATED, response_model=User)
def create_recipe(user_in: UserCreate, db: Database = Depends(get_db)) -> User:
    user: UserInDB = db_ops.users.create(db=db, user_in=user_in)
    response_data = User(**user.dict())
    return response_data
