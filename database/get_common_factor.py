from Config import Config
from database.cursor import cursor

_is_answer_common_query = f'''
SELECT COUNT(*) / (10 + SELECT COUNT(*) FROM {Config.question_answers_table} WHERE question = ?)
FROM {Config.question_answers_table}
WHERE question = ? AND aswer = ? 
'''


def get_common_factor(question: str, answer: str) -> float:
    cursor.execute(_is_answer_common_query, (question, question, answer,))
    return cursor.fetchall()[0][0]
