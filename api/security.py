import os
from datetime import datetime, timedelta

import jwt

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
