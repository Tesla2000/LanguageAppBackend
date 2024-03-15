from itertools import filterfalse
from random import random, choice
from typing import IO

from Config import Config
from sentences import sentences


def _return_answer(previous_questions: tuple[str, ...], file: IO):
    if previous_questions and (
        random() < Config.repetition_rate or len(previous_questions) == len(sentences)
    ):
        next_question = choice(previous_questions)
    else:
        next_question = choice(
            tuple(filterfalse(previous_questions.__contains__, sentences.keys()))
        )
    next_sentence = f"{next_question};{sentences[next_question]}"
    file.close()
    return next_sentence
