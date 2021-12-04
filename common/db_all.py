import typing

from flask_sqlalchemy import SQLAlchemy

db: typing.Optional[SQLAlchemy] = None


def init_db(_db: SQLAlchemy):
    global db
    if db is None:
        db = _db

    return db


def get_db():
    global db
    return db
