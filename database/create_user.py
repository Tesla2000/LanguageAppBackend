from itertools import chain

import sqlalchemy

from database.session import Users, session


def create_user(
    username: str, password: str
) -> bool:
    query = sqlalchemy.select(Users.username).where(Users.username == username)
    if tuple(chain.from_iterable(session.execute(query).fetchall())):
        return False
    session.add(Users(username=username, password=password))
    session.commit()
    return True
