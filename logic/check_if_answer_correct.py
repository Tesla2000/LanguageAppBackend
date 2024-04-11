from Config import Config
from database.get_common_factor import get_common_factor
from langchain_component.llm_check_answer_correct import llm_check_answer_correct


def check_if_answer_correct(question: str, answer: str, language_dict: dict[str, list[list[str]]], language: str) -> bool:
    expected_answers = language_dict[question]
    normalize = lambda text: answer.lower().strip(".?¿!¡").replace(",", "")
    positive_answers = expected_answers[0]
    negative_answers = expected_answers[1]
    is_in_correct = normalize(answer) in map(
        normalize, positive_answers,
    )
    if is_in_correct:
        return True
    common_factor = get_common_factor(question, answer)
    if common_factor < Config.common_factor:
        return False
    judged_correct = common_factor > Config.very_common_factor or (normalize(answer) not in map(
        normalize, negative_answers,
    ) and llm_check_answer_correct(question, answer, language))
    (positive_answers if judged_correct else negative_answers).append(answer)
    return judged_correct
