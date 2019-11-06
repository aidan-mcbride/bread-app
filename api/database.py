from pyArango.collection import Collection
from pyArango.connection import Connection
from pyArango.database import Database


def get_db() -> Database:
    db_name = "breadapp"
    conn = Connection()
    if not conn.hasDatabase(db_name):
        conn.createDatabase(name=db_name)
    db = conn[db_name]
    return db


def get_test_db() -> Database:
    db_name = "breadapp_testing"
    conn = Connection()
    if not conn.hasDatabase(db_name):
        conn.createDatabase(name=db_name)
    db = conn[db_name]
    return db


def get_collection(db: Database, collection: str) -> Collection:
    if not db.hasCollection(name=collection):
        db.createCollection(name=collection)
    return db[collection]
