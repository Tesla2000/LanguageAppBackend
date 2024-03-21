from time import time

from flask import request

import sentences
from Config import Config
from flask_app import app
from endpoints._return_next_question import _return_next_question


@app.route("/<language>", methods=["POST"])
def post_answer(language: str):
    username, question, answer, language_dict = request.data.decode().split(";")
    language_dict = getattr(sentences, language_dict)
    correct = answer.lower().strip(".?¿!¡").replace(",", "") in map(
        lambda correct_version: correct_version.lower().strip(".?¿!¡").replace(",", ""),
        language_dict[question].split(";"),
    )
    if correct:
        file = Config.correct_answers_path(username, language).open("a+")
    else:
        file = Config.incorrect_answers_path(username, language).open("a+")
    file.write(f"{int(time())};{question};{answer}\n")
    if not correct:
        return ""
    file.close()
    return _return_next_question(username, language)
