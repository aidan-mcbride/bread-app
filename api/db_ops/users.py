"""
Functions for performing database operations(db ops) on users
"""

from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from pyArango.database import Database
from pyArango.theExceptions import DocumentNotFoundError
from pydantic import EmailStr

from api.database import get_collection
from api.schemas.user import User, UserCreate, UserCreateToDB, UserUpdate
from api.utils import hash_password


def create(db: Database, user_in: UserCreate) -> User:
    collection = get_collection(db=db, collection="Users")
    hashed_password = hash_password(plain_password=user_in.password)
    user_to_db = UserCreateToDB(**user_in.dict(), hashed_password=hashed_password)
    user_dict = jsonable_encoder(user_to_db)

    db_record = collection.createDocument(initDict=user_dict)
    db_record.save()

    response_data = User(**db_record.getStore(), id=db_record["_key"])
    return response_data


def read_all(db: Database) -> List[User]:
    collection = get_collection(db=db, collection="Users")
    users: List[User] = list()

    results = collection.fetchAll()
    for user in results:
        user_data = user.getStore()
        id = user_data["_key"]
        users.append(User(**user_data, id=id))

    return users


def read(id: int, db: Database) -> Optional[User]:
    collection = get_collection(db=db, collection="Users")
    try:
        results = collection[id]
    except DocumentNotFoundError:
        return None
    user_data = results.getStore()
    id = user_data["_key"]
    user = User(**user_data, id=id)
    return user


def read_by_email(email: EmailStr, db: Database) -> Optional[User]:
    collection = get_collection(db=db, collection="Users")
    try:
        # https://pyarango.readthedocs.io/en/latest/collection/#pyArango.collection.Collection.fetchFirstExample
        results = collection.fetchFirstExample({"email": email})[0]
    except IndexError:
        # use IndexError here since fetchFirstExample returns a list
        return None
    user_data = results.getStore()
    id = user_data["_key"]
    user = User(**user_data, id=id)
    return user


def update(id: int, user_update: UserUpdate, db: Database) -> User:
    collection = get_collection(db=db, collection="Users")

    db_record = collection[id]
    update_data = user_update.dict(skip_defaults=True)
    for field in db_record.getStore():
        if field in update_data:
            db_record[field] = update_data[field]
    if user_update.password:
        hashed_password = hash_password(plain_password=user_update.password)
        db_record["hashed_password"] = hashed_password
    db_record.save()

    response_data = User(**db_record.getStore(), id=db_record["_key"])
    return response_data


def delete(id: int, db: Database) -> User:
    collection = get_collection(db=db, collection="Users")
    db_record = collection[id]
    user = User(**db_record.getStore(), id=id)
    db_record.delete()
    return user
