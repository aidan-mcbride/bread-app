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
