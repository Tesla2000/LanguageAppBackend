from .cursor import conn, cursor

_insert_query = """
INSERT INTO {} (question, answer, username, is_answer_correct)
VALUES (?, ?, ?, ?);
"""


def insert_answer(
    question: str, answer: str, username: str, is_answer_correct: bool, language: str
):
    cursor.execute(
        _insert_query.format(language), (question, answer, username, is_answer_correct)
    )
    conn.commit()
