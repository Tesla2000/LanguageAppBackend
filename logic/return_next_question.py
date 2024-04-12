import random

import numpy as np

from Config import Config
from ai_component.ChanceCalculator import chance_calculator
from database.get_answers import get_answers
from database.get_user_questions import get_user_questions
from sentences.sentences import sentences


def return_next_question(username: str, language: str) -> str:
    language_dict: dict = sentences.get(language)
    user_questions = get_user_questions(username, language)
    odds = tuple(
        chance_calculator.predict(get_answers(question, username, language))
        for question in user_questions
    )
    questions = tuple(language_dict.keys())
    next_question_index = 0
    if user_questions and random.random() < Config.repeat_question_at_random_chance:
        next_question_index = random.choice(tuple(map(questions.index, filter(questions.__contains__, user_questions))))
    elif user_questions:
        next_question_index = 1 + max(map(questions.index, filter(questions.__contains__, user_questions)))
    elif user_questions and (
        next_question_index >= len(questions)
        or any(odd < Config.required_confidence for odd in odds)
    ):
        next_question_index = np.argmin(odds)
    next_question = questions[next_question_index]
    next_sentence = f"{next_question};{language_dict[next_question][0][0]}"
    return next_sentence
