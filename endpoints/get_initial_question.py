from itertools import takewhile, count
from pathlib import Path

from flask import request, abort

from app import app
from authentication import authenticate_token
from endpoints._return_answer import _return_answer


@app.route("/<login>", methods=["GET"])
def get_initial_question(login: str):
    token = request.headers['Authorization'].split("Bearer ")[-1]
    auth_login = authenticate_token(token)
    if not auth_login or auth_login != login:
        abort(401)
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
