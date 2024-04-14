import sqlalchemy

from database.session import Users, conn


def create_user(
    username: str, password: str
):
    query = sqlalchemy.select(Users.username).filter(Users.username == username)
    assert not conn.execute(query).all()
    query = sqlalchemy.insert(Users).values({"username": username, "password": password})
    conn.execute(query)
    conn.commit()
