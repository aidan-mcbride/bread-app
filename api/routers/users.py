from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pyArango.database import Database
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from api import db_ops
from api.database import get_db
from api.schemas.user import User, UserCreate, UserInDB
from api.security import get_current_active_user

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
    db: Database = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
) -> List[UserInDB]:
    return db_ops.users.read_all(db=db)


@router.get("/me", response_model=User)
def read_current_user(
    db: Database = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    return current_user


@router.get("/{id}", response_model=User)
def read_user(
    id: int,
    db: Database = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    user = db_ops.users.read(db=db, id=id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    if user != current_user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="The user does not have sufficient privileges to access other users",
        )
    return user
