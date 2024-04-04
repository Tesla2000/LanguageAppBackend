import sentences
from Config import Config
from endpoints._return_next_question import _return_next_question
from flask_app import app


@app.route("/<login>/<language>", methods=["GET"])
def get_initial_question(login: str, language: str):
    correctly_answered_file = Config.correct_answers_path(login, language)
    incorrectly_answered_file = Config.incorrect_answers_path(login, language)
    if not correctly_answered_file.exists():
        correctly_answered_file = correctly_answered_file.open("w")
        incorrectly_answered_file = incorrectly_answered_file.open("w")
        correctly_answered_file.close()
        incorrectly_answered_file.close()
    return _return_next_question(login, language)
