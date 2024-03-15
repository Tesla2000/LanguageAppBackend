from itertools import takewhile, count
from time import time

from flask import request

from Config import Config
from app import app
from endpoints._return_answer import _return_answer
from sentences import sentences


@app.route("/", methods=["POST"])
def get_new_question():
    login, question, answer = request.data.decode().split(";")
    correct = answer.lower().strip(".?!").replace(",", "") in map(
        lambda correct_version: correct_version.lower().strip(".?!").replace(",", ""), sentences[
            question
        ].split(';'))
    if correct:
        file = Config.correct_answers_path(login).open("a+")
    else:
        file = Config.incorrect_answers_path(login).open("a+")
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
