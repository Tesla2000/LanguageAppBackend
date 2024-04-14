import sqlalchemy

from database.session import qa_tables, conn


def insert_answer(
    question: str, answer: str, username: str, is_answer_correct: bool, language: str
):
    QA = qa_tables[language]
    query = sqlalchemy.insert(QA).values(
        question=question, answer=answer, username=username, is_answer_correct=is_answer_correct)
    conn.execute(query)
    conn.commit()
