from itertools import chain

import sqlalchemy

from database.session import Users, conn
from flask_app import bcrypt


def authenticate_user(
    username: str, password: str
) -> bool:
    query = sqlalchemy.select(Users.password).where(Users.username == username)
    db_password = tuple(chain.from_iterable(conn.execute(query).fetchall()))
    if len(db_password) != 1:
        return False
    return bcrypt.check_password_hash(
        db_password[0], password
    )
