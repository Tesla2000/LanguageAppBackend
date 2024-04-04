from collections import defaultdict
from itertools import filterfalse
from math import sqrt, exp, ceil
from random import random, choices
from statistics import fmean

import sentences
from Config import Config
from ai_component.collect_data import collect_data


def _mean_in_percentile(input, q):
    data_sorted = sorted(input)
    index = ceil(q / 100 * len(data_sorted))
    return fmean(data_sorted[:index])


def _return_next_question(username: str, language: str) -> str:
    language_dict: dict = getattr(sentences, language)
    user_data = collect_data(language, username)[username]
    data_divided_to_sentences = defaultdict(list)
    for (_, question_index, is_correct) in user_data:
        data_divided_to_sentences[question_index].append(is_correct)
    del user_data
    if data_divided_to_sentences and (
        min(
            _mean_in_percentile(
                tuple(
                    sum(value) / len(value)
                    for value in data_divided_to_sentences.values()
                ),
                Config.worst_answers_percentile,
            )
            * Config.repetition_rate_factor,
            Config.maximal_repetition_rate,
        )
        < random()
        or len(data_divided_to_sentences) == len(language_dict)
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
            filterfalse(
                data_divided_to_sentences.__contains__, range(len(language_dict.keys()))
            )
        )
    next_question = tuple(language_dict.keys())[question_index]
    next_sentence = f"{next_question};{language_dict[next_question]}"
    return next_sentence
