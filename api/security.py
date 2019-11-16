from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from pyArango.database import Database
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from api import db_ops
from api.config import JWT_ALGORITHM, JWT_SECRET_KEY
from api.database import get_db
from api.schemas.user import UserInDB

# from api.schemas.token import TokenPayload

# ---------------------------------------------


pw_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pw_ctx.hash(plain_password)


def verify_password_hash(plain_password: str, hashed_password: str):
    return pw_ctx.verify(plain_password, hashed_password)


# ---------------------------------------------


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


# ---------------------------------------------


# tokenUrl: the url where the client submits their credentials to get a token
# https://fastapi.tiangolo.com/tutorial/security/first-steps/#fastapis-oauth2passwordbearer
get_token = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    db: Database = Depends(get_db), token: str = Depends(get_token)
) -> UserInDB:
    """
    decodes the given JWT token to obtain a user id,
    then returns that user in the database
    """
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # decode JWT token
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    # read and return user in db
    user = db_ops.users.read(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if not db_ops.users.is_active(current_user):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
