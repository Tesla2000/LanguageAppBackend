from itertools import takewhile, count, filterfalse
from pathlib import Path
from time import time
from random import random, choice
from typing import IO

from sentences import sentences
from Config import Config

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_new_question():
    login, question, answer = request.data.decode().split(";")
    correct = answer.lower().strip(".?!").replace(",", "") == sentences[
        question
    ].lower().strip(".?!").replace(",", "")
    if correct:
        file = (
            Path(__file__)
            .parent.joinpath(f"data/{login}_correct_answers.txt")
            .open("a+")
        )
    else:
        file = (
            Path(__file__)
            .parent.joinpath(f"data/{login}_incorrect_answers.txt")
            .open("a+")
        )
    file.write(f"{int(time())};{question};{answer}\n")
    if not correct:
        return ""
    file.seek(0)
    previous_questions = tuple(
        set(
            line.split(";")[1]
            for line in takewhile(bool, (file.readline() for _ in count()))
        )
    )
    return _return_answer(previous_questions, file)


@app.route("/<login>", methods=["GET"])
def get_initial_question(login: str):
    file = Path(__file__).parent.joinpath(f"data/{login}_correct_answers.txt")
    if file.exists():
        file = file.open()
        previous_questions = tuple(
            set(
                line.split(";")[1]
                for line in takewhile(bool, (file.readline() for _ in count()))
            )
        )
    else:
        file = file.open("a")
        previous_questions = tuple()
    return _return_answer(previous_questions, file)


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


if __name__ == "__main__":
    app.run(debug=True)
