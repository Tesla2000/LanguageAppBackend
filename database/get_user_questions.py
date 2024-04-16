import sqlalchemy

from .session import qa_tables, session


def get_user_questions(username: str, language: str) -> list[str]:
    QA = qa_tables[language]
    query = sqlalchemy.select(QA.question).filter(QA.username == username).distinct()
    return [question[0] for question in session.execute(query).fetchall()]
