from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pyArango.database import Database
from pydantic import EmailStr
from starlette.status import HTTP_400_BAD_REQUEST

from api import db_ops
from api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from api.database import get_db
from api.schemas.token import Token
from api.security import create_access_token

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    db: Database = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    email = EmailStr(form_data.username)
    password = form_data.password
    user = db_ops.users.authenticate(db=db, email=email, password=password)
    if not user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    elif not db_ops.users.is_active(user):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # TODO: move stuff like token expiry to config file
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
