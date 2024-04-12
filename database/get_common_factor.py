from database.cursor import cursor

_is_answer_common_query = """
SELECT COUNT(*) / (10.0 + (SELECT COUNT(*) FROM {language} WHERE question = ?))
FROM {language}
WHERE question = ? AND answer = ? 
"""


def get_common_factor(question: str, answer: str, language: str) -> float:
    cursor.execute(
        _is_answer_common_query.format(language=language),
        (
            question,
            question,
            answer,
        ),
    )
    return cursor.fetchall()[0][0]
