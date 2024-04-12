from .cursor import cursor

_unique_questions_query = """
SELECT DISTINCT question
FROM {}
WHERE username = ?;
"""


def get_user_questions(username: str, language: str) -> list[str]:
    cursor.execute(_unique_questions_query.format(language), (username,))
    unique_questions = cursor.fetchall()
    return [question[0] for question in unique_questions]
