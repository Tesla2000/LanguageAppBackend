from time import time

from flask import request

from Config import Config
from flask_app import app
from endpoints._return_next_question import _return_next_question
from sentences import sentences


@app.route("/", methods=["POST"])
def get_new_question():
    username, question, answer = request.data.decode().split(";")
    correct = answer.lower().strip(".?!").replace(",", "") in map(
        lambda correct_version: correct_version.lower().strip(".?!").replace(",", ""),
        sentences[question].split(";"),
    )
    if correct:
        file = Config.correct_answers_path(username).open("a+")
    else:
        file = Config.incorrect_answers_path(username).open("a+")
    file.write(f"{int(time())};{question};{answer}\n")
    if not correct:
        return ""
    file.close()
    return _return_next_question(username)
