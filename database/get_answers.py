from .cursor import cursor

_select_query = '''
SELECT (time, is_answer_correct)
FROM QuestionAnswers
WHERE username = ? AND question = ?
ORDER BY time;
'''


def get_answers(question: str, username: str) -> list[int, bool]:
    cursor.execute(_select_query, (question, username,))
    return cursor.fetchall()
