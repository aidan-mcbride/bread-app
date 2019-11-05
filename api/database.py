"""
MOCK DATABASE FOR NOW
TODO: Replace with ArangoDB
"""

from pyArango.collection import Collection
from pyArango.connection import Connection
from pyArango.database import Database


def get_db(db_name: str = "breadapp") -> Database:
    conn = Connection()
    if not conn.hasDatabase(db_name):
        conn.createDatabase(name=db_name)
    db = conn[db_name]
    return db


def get_test_db(db_name: str = "breadapp_testing") -> Database:
    return get_db(db_name=db_name)


def get_collection(db: Database, collection: str) -> Collection:
    if not db.hasCollection(name=collection):
        db.createCollection(name=collection)
    return db[collection]
