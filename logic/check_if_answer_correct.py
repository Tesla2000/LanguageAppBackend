from Config import Config
from database.get_common_factor import get_common_factor


def check_if_answer_correct(
    question: str, answer: str, language_dict: dict[str, list[list[str]]], language: str
) -> bool:
    expected_answers = language_dict[question]
    normalize = (
        lambda text: text.lower().strip(".?¿!¡").replace(",", "").replace("-", " ")
    )
    positive_answers = expected_answers[0]
    is_in_correct = normalize(answer) in map(
        normalize,
        positive_answers,
    )
    if is_in_correct:
        return True
    common_factor = get_common_factor(question, answer, language)
    if common_factor < Config.common_factor:
        return False
    # judged_correct = common_factor > Config.very_common_factor or (
    #     normalize(answer)
    #     not in map(
    #         normalize,
    #         negative_answers,
    #     )
    #     and llm_check_answer_correct(question, answer, language)
    # )
    judged_correct = common_factor > Config.very_common_factor
    positive_answers.append(answer)
    return judged_correct
