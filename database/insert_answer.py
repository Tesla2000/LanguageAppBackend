from .cursor import conn, cursor

_insert_query = '''
INSERT INTO QuestionAnswers (question, answer, username, is_answer_correct)
VALUES (?, ?, ?, ?);
'''


def insert_answer(question: str, answer: str, username: str, is_answer_correct: bool):
    cursor.execute(_insert_query, (question, answer, username, is_answer_correct))
    conn.commit()
