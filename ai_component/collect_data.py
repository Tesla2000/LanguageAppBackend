from collections import defaultdict

from Config import Config
import sentences


def collect_data(
    language: str, username: str = None
) -> dict[str, list[tuple[int, int]]]:
    answers = defaultdict(list)
    language_dict: dict = getattr(sentences, language)
    questions = tuple(language_dict.keys())
    for file in (
        Config.data_path.iterdir()
        if username is None
        else (
            Config.incorrect_answers_path(username, language),
            Config.correct_answers_path(username, language),
        )
    ):
        if file == Config.users_path:
            continue
        answers[file.name.split("_")[0]] += list(
            (
                int(line.split(";")[0]),
                questions.index(line.split(";")[1]),
                int(file.name.endswith(Config.correct_answers_ending)),
            )
            for line in file.read_text().splitlines()
            if line.split(";")[1] in questions
        )
    return dict(sorted(answers.items(), key=lambda item: item[1], reverse=True))


if __name__ == "__main__":
    collect_data(getattr(sentences, Config.trained_language))
