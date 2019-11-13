from typing import Optional

from pydantic import BaseModel, EmailStr  # , Schema


# base class for all users
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


# base class for users that have been saved to database
class UserBaseInDB(UserBase):
    id: int
    email: EmailStr
    is_active: bool


# fields available to client when creating a new user
class UserCreate(UserBase):
    email: EmailStr
    password: str


# hashed_password added on server before saving to db
class UserCreateToDB(UserCreate):
    hashed_password: str


# fields available to client when updating existing user
class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True


# all data in database: used for internal use in api (auth)
class UserInDB(UserBaseInDB):
    hashed_password: str


# data returned to client as response body for all requests
class User(UserBaseInDB):
    pass
