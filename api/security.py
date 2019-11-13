import os
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

pw_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pw_ctx.hash(plain_password)


def verify_password_hash(plain_password: str, hashed_password: str):
    return pw_ctx.verify(plain_password, hashed_password)


SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))
ALGORITH = str(os.getenv("JWT_ALGORITHM"))


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
    return encoded_jwt
