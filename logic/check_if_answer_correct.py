from Config import Config
from database.consecutive_answers_agree import consecutive_answers_agree
from database.get_common_factor import get_common_factor
from database.update_correct_answers import update_correct_answers


def check_if_answer_correct(
    question: str, answer: str, language_dict: dict[str, list[list[str]]], language: str, username: str
) -> bool:
    expected_answers = language_dict[question]
    normalize = (
        lambda text: text.lower().strip(".?¿!¡").replace(",", "").replace("-", " ").replace("'", "")
    )
    positive_answers = expected_answers[0]
    is_in_correct = normalize(answer) in map(
        normalize,
        positive_answers,
    )
    if is_in_correct:
        return True
    common_factor = get_common_factor(question, answer, language)
    if common_factor > Config.very_common_factor or consecutive_answers_agree(question, answer, username, language):
        positive_answers.append(answer)
        update_correct_answers(question, answer, language)
        return True
    return False
