from sqlalchemy import select

from database.session import qa_tables, session


def get_common_factor(question: str, answer: str, language: str) -> float:
    QA = qa_tables[language]
    query1 = select(QA).where(QA.question == question, QA.answer == answer)
    query2 = select(QA).where(QA.question == question)
    return len(session.execute(query1).fetchall()) / len(session.execute(query2).fetchall())
