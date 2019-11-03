"""
MOCK DATABASE FOR NOW
TODO: Replace with ArangoDB
"""

db: dict = dict(recipes=list(), users=list())


def get_db():
    return db
