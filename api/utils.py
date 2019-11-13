from enum import Enum


# see:
# https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values
class SortDirection(str, Enum):
    asc = "asc"
    desc = "desc"
