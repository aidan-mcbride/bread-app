from typing import Optional

from pydantic import BaseModel, EmailStr  # , Schema


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


# data added to created recipe before being added to db
class UserCreateToDB(UserBase):
    hashed_password: str
    is_active: bool = True


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True


# data returned to client as response body
class User(UserBase):
    id: int
    is_active: bool
