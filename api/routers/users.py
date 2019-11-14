from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pyArango.database import Database
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from api import db_ops
from api.database import get_db
from api.schemas.user import User, UserCreate, UserInDB
from api.security import get_current_user

router = APIRouter()


@router.post("/", status_code=HTTP_201_CREATED, response_model=User)
def create_recipe(user_in: UserCreate, db: Database = Depends(get_db)) -> UserInDB:
    user = db_ops.users.read_by_email(db=db, email=user_in.email)
    print(user)
    if user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )
    return db_ops.users.create(db=db, user_in=user_in)


@router.get("/", response_model=List[User])
def read_users(
    db: Database = Depends(get_db), current_user: UserInDB = Depends(get_current_user)
) -> List[UserInDB]:
    return db_ops.users.read_all(db=db)


@router.get("/me", response_model=User)
def read_current_user(
    db: Database = Depends(get_db), current_user: UserInDB = Depends(get_current_user)
):
    return current_user
