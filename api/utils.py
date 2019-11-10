from enum import Enum

from passlib.context import CryptContext


# see:
# https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values
class SortDirection(str, Enum):
    asc = "asc"
    desc = "desc"


pw_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pw_ctx.hash(plain_password)


def verify_password_hash(plain_password: str, hashed_password: str):
    return pw_ctx.verify(plain_password, hashed_password)
