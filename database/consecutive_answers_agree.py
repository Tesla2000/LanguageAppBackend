from collections import Counter
from datetime import datetime, timedelta
from itertools import chain

from sqlalchemy import select

from Config import Config
from database.session import qa_tables, session


def consecutive_answers_agree(question: str, answer: str, username: str, language: str) -> bool:
    QA = qa_tables[language]
    query = select(QA.answer).where(QA.question == question, QA.username == username, QA.time > datetime.utcnow() - timedelta(seconds=Config.recent_answer_time_threshold))
    answers = Counter(chain.from_iterable(session.execute(query).fetchall()))
    if answers[answer] >= Config.recent_answer_count_to_accept and sum(answers.values()) >= Config.recent_answer_count_to_accept + 1:
        return True
    return False
