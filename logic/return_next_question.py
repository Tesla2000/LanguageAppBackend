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
    questions = tuple(language_dict.keys())
    user_questions = set(filter(questions.__contains__, user_questions))
    if user_questions and random.random() < Config.repeat_question_at_random_chance:
        next_question_index = random.choice(tuple(map(questions.index, user_questions)))
        next_question = questions[next_question_index]
        next_sentence = f"{next_question};{language_dict[next_question][0][0]}"
        return next_sentence
    odds = np.array(tuple(
        chance_calculator.predict(get_answers(question, username, language))
        for question in user_questions
    ))
    next_question_index = 0
    if len(user_questions) == len(questions) or (user_questions and any(odd < Config.required_confidence for odd in odds)):
        probabilities = 1 / odds - 1
        probabilities /= np.sum(probabilities)
        next_question_index = np.random.choice(range(len(odds)), p=probabilities)
    elif user_questions:
        next_question_index = 1 + max(map(questions.index, user_questions))
    next_question = questions[next_question_index]
    next_sentence = f"{next_question};{language_dict[next_question][0][0]}"
    return next_sentence
