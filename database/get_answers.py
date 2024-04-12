from Config import Config
from database.cursor import cursor

_select_query = f'''
SELECT julianday(CURRENT_TIMESTAMP) - julianday(time) AS time_diff, is_answer_correct
FROM {Config.question_answers_table}
WHERE username = ? AND question = ?
ORDER BY time;
'''



def get_answers(question: str, username: str) -> list[tuple[int, bool]]:
    cursor.execute(_select_query, (question, username,))
    return cursor.fetchall()



if __name__ == '__main__':
    get_answers("Cześć.", "filip")
