from sqlalchemy import text

from database.session import conn

_is_answer_common_query = """
SELECT COUNT(*) / (10.0 + (SELECT COUNT(*) FROM {language} WHERE question = :question))
FROM {language}
WHERE question = :question AND answer = :answer
"""


def get_common_factor(question: str, answer: str, language: str) -> float:
    result = conn.execute(
        statement=text(_is_answer_common_query.format(language=language)),
        parameters={
            "question": question,
            "answer": answer,
        },
    )
    return result.fetchall()[0][0]
