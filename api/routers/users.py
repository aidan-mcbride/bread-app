from fastapi import APIRouter, Depends
from pyArango.database import Database
from starlette.status import HTTP_201_CREATED

from api import db_ops
from api.database import get_db
from api.schemas.user import User, UserCreate, UserInDB
from api.security import get_current_user

router = APIRouter()


@router.post("/", status_code=HTTP_201_CREATED, response_model=User)
def create_recipe(user_in: UserCreate, db: Database = Depends(get_db)) -> User:
    user: UserInDB = db_ops.users.create(db=db, user_in=user_in)
    response_data = User(**user.dict())
    return response_data


@router.get("/me", response_model=User)
def read_current_user(
    db: Database = Depends(get_db), current_user: UserInDB = Depends(get_current_user)
):
    return current_user
