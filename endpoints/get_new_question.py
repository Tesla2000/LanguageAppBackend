from flask import request

from ai_component.train_sample import train_sample
from database.get_answers import get_answers
from database.insert_answer import insert_answer
from flask_app import app
from logic.check_if_answer_correct import check_if_answer_correct
from logic.return_next_question import return_next_question
from sentences.sentences import sentences


@app.route("/<language>", methods=["POST"])
def post_answer(language: str):
    username, question, answer = request.data.decode().split(";")
    language_dict = sentences.get(language)
    is_answer_correct = check_if_answer_correct(question, answer, language_dict, language)
    train_sample(get_answers(question, username), is_answer_correct)
    insert_answer(question, answer, username, is_answer_correct)
    if not is_answer_correct:
        return ""
    return return_next_question(username, language)
