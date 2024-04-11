from flask import request

from database.insert_answer import insert_answer
from endpoints._return_next_question import _return_next_question
from flask_app import app
from sentences.sentences import sentences


@app.route("/<language>", methods=["POST"])
def post_answer(language: str):
    username, question, answer = request.data.decode().split(";")
    language_dict = sentences.get(language)
    correct = answer.lower().strip(".?¿!¡").replace(",", "") in map(
        lambda correct_version: correct_version.lower().strip(".?¿!¡").replace(",", ""),
        language_dict[question].split(";"),
    )
    insert_answer(question, answer, username, correct)
    if not correct:
        return ""
    return _return_next_question(username, language)
