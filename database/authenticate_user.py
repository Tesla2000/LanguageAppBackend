import sqlalchemy

from database.session import Users, conn
from flask_app import bcrypt


def authenticate_user(
    username: str, password: str
) -> bool:
    query = sqlalchemy.select(Users.password).filter(Users.username == username)
    db_password = conn.execute(query).all()
    if len(db_password) != 1:
        return False
    return bcrypt.check_password_hash(
        db_password[0][0], password
    )
