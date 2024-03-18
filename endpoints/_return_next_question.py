from collections import defaultdict
from itertools import filterfalse
from math import sqrt, exp
from random import random, choices
from statistics import fmean

from Config import Config
from ai_component.collect_data import collect_data
from sentences import sentences, questions


def _return_next_question(username: str) -> str:
    user_data = collect_data(username)[username]
    data_divided_to_sentences = defaultdict(list)
    for (_, question_index, is_correct) in user_data:
        data_divided_to_sentences[question_index].append(is_correct)
    del user_data
    if data_divided_to_sentences and (
        random()
        < min(fmean(
            sum(value) / len(value) for value in data_divided_to_sentences.values()
        ) * Config.repetition_rate_factor, Config.maximal_repetition_rate)
        or len(data_divided_to_sentences) == len(sentences)
    ):
        question_index = choices(
            tuple(data_divided_to_sentences.keys()),
            tuple(
                map(
                    lambda item: exp(
                        -sum(item[1])
                        / len(item[1])
                        * (
                            sqrt(sum(map(len, data_divided_to_sentences.values())))
                            / (1 + len(item[1]))
                        )
                    ),
                    data_divided_to_sentences.items(),
                ),
            ),
        )[0]
    else:
        question_index = next(
            filterfalse(data_divided_to_sentences.__contains__, range(len(questions)))
        )
    next_question = questions[question_index]
    next_sentence = f"{next_question};{sentences[next_question]}"
    return next_sentence
