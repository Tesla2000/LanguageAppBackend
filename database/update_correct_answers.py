from sqlalchemy import update

from database.session import qa_tables, session


def update_correct_answers(question: str, answer: str, language: str):
    QA = qa_tables[language]
    query = update(QA).where(QA.question == question, QA.answer == answer).values(is_answer_correct=True)
    session.execute(query)
    session.commit()
