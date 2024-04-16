from sqlalchemy import text

from database.session import conn

_select_query = """
SELECT julianday(CURRENT_TIMESTAMP) - julianday(time) AS time_diff, is_answer_correct
FROM {}
WHERE username = :username AND question = :question
ORDER BY time;
"""


def get_answers(question: str, username: str, language: str) -> list[tuple[int, bool]]:
    result = conn.execute(
        text(_select_query.format(language)),
        {
            "username": username,
            "question": question,
        },
    )
    return result.fetchall()
