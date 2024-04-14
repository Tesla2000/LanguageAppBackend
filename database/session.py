from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import atexit

from Config import Config

engine = create_engine(f"sqlite+pysqlite:///{Config.database.absolute()}", echo=True)
conn = engine.connect()

Base = declarative_base()
qa_tables = {}
for file in Config.sentences.glob("*.json"):
    qa_tables[file.with_suffix('').name] = type(file.with_suffix('').name, (Base,), {
        "__tablename__": file.with_suffix('').name,
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "time": Column(TIMESTAMP, nullable=False, server_default='CURRENT_TIMESTAMP'),
        "question": Column(String, nullable=False),
        "answer": Column(String, nullable=False),
        "username": Column(String, nullable=False),
        "is_answer_correct": Column(Boolean, nullable=False),
    })
    if not engine.dialect.has_table(conn, file.with_suffix('').name):
        Base.metadata.create_all(engine)
    else:
        Base.metadata.clear()


class Users(Base):
    __tablename__ = "Users"
    username = Column(String, nullable=False, primary_key=True)
    password = Column(String, nullable=False)


if not engine.dialect.has_table(conn, "Users"):
    Base.metadata.create_all(engine)
else:
    Base.metadata.clear()

Session = sessionmaker(bind=engine)
session = Session()


@atexit.register
def close_connection():
    session.close()
    conn.close()
