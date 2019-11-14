import os
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from pyArango.database import Database
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from api import db_ops
from api.database import get_db

# from api.schemas.token import TokenPayload

# ---------------------------------------------


pw_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pw_ctx.hash(plain_password)


def verify_password_hash(plain_password: str, hashed_password: str):
    return pw_ctx.verify(plain_password, hashed_password)


# ---------------------------------------------

# TODO: move to some config file
SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))
ALGORITHM = str(os.getenv("JWT_ALGORITHM"))


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ---------------------------------------------


# tokenUrl: the url where the client submits their credentials to get a token
# https://fastapi.tiangolo.com/tutorial/security/first-steps/#fastapis-oauth2passwordbearer
get_token = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(db: Database = Depends(get_db), token: str = Depends(get_token)):
    """
    decodes the given JWT token to obtain a user id,
    then returns that user in the database
    """
    # decode JWT token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["user_id"]
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    # read and return user in db
    user = db_ops.users.read(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user
