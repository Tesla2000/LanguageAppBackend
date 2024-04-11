from Config import Config
from .cursor import cursor

_select_query = f'''
SELECT (CURRENT_TIMESTAMP - time, is_answer_correct)
FROM {Config.question_answers_table}
WHERE username = ? AND question = ?
ORDER BY time;
'''


def get_answers(question: str, username: str) -> list[tuple[int, bool]]:
    cursor.execute(_select_query, (question, username,))
    return cursor.fetchall()
