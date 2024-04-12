from database.cursor import cursor

_select_query = """
SELECT julianday(CURRENT_TIMESTAMP) - julianday(time) AS time_diff, is_answer_correct
FROM {}
WHERE username = ? AND question = ?
ORDER BY time;
"""


def get_answers(question: str, username: str, language: str) -> list[tuple[int, bool]]:
    cursor.execute(
        _select_query.format(language),
        (
            username,
            question,
        ),
    )
    return cursor.fetchall()
