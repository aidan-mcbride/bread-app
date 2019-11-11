"""
Functions for performing database operations(db ops) on users
"""

from typing import List

from fastapi.encoders import jsonable_encoder
from pyArango.database import Database
from pyArango.theExceptions import DocumentNotFoundError

from api.database import get_collection
from api.schemas.user import User, UserCreate, UserCreateToDB
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


def read(id: int, db: Database) -> User:
    collection = get_collection(db=db, collection="Users")
    try:
        results = collection[id]
        user_data = results.getStore()
        id = user_data["_key"]
        user = User(**user_data, id=id)
    except DocumentNotFoundError:
        user = None
    return user
