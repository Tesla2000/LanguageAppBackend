from collections import defaultdict

from Config import Config
from sentences import questions


def collect_data(username: str = None) -> dict[str, list[tuple[int, int]]]:
    answers = defaultdict(list)
    for file in (
        Config.data_path.iterdir()
        if username is None
        else (
            Config.incorrect_answers_path(username),
            Config.correct_answers_path(username),
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
    collect_data()
