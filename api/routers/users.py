from fastapi import APIRouter, Depends
from pyArango.database import Database
from starlette.status import HTTP_201_CREATED

from api import db_ops
from api.database import get_db
from api.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/", status_code=HTTP_201_CREATED, response_model=User)
def create_recipe(user_in: UserCreate, db: Database = Depends(get_db)) -> User:
    return db_ops.users.create(db=db, user_in=user_in)
