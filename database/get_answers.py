from datetime import datetime

from sqlalchemy import select

from database.session import qa_tables, session


def get_answers(question: str, username: str, language: str) -> list[tuple[int, bool]]:
    QA = qa_tables[language]
    results = session.execute(
        select(QA.time, QA.is_answer_correct).where(QA.username == username, QA.question == question)).fetchall()
    return list(((datetime.now() - time).seconds, bool(is_answer_correct)) for time, is_answer_correct in results)
