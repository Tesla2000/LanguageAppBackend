from itertools import takewhile, count

from Config import Config
from flask_app import app
from endpoints._return_answer import _return_answer


@app.route("/<login>", methods=["GET"])
def get_initial_question(login: str):
    file = Config.correct_answers_path(login)
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
