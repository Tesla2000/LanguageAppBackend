from functools import partial
from math import ceil
from statistics import fmean

import numpy as np

from Config import Config
from ai_component.ChangeCalculator import chance_calculator
from database.get_answers import get_answers
from database.get_user_questions import get_user_questions
from sentences.sentences import sentences


def _mean_in_percentile(input, q):
    data_sorted = sorted(input)
    index = ceil(q / 100 * len(data_sorted))
    return fmean(data_sorted[:index])


def _return_next_question(username: str, language: str) -> str:
    language_dict: dict = sentences.get(language)
    user_questions = get_user_questions(username)
    odds = tuple(map(chance_calculator, map(partial(get_answers, username=username), user_questions)))
    questions = tuple(language_dict.keys())
    next_question_index = 1 + max(map(questions.index, user_questions))
    if next_question_index >= len(questions) or all(odd > Config.required_confidence for odd in odds):
        next_question_index = np.argmin(odds)
    next_question = questions[next_question_index]
    next_sentence = f"{next_question};{language_dict[next_question]}"
    return next_sentence
