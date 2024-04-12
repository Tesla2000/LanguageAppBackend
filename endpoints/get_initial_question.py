from logic.return_next_question import return_next_question
from flask_app import app


@app.route("/<login>/<language>", methods=["GET"])
def get_initial_question(login: str, language: str):
    return return_next_question(login, language)
