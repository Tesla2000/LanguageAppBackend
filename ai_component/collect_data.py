from collections import defaultdict

from Config import Config
from sentences import sentences


def collect_data() -> dict[str, list[tuple[int, int]]]:
    questions = tuple(sentences.keys())
    answers = defaultdict(list)
    for file in Config.data_path.iterdir():
        if file == Config.users_path:
            continue
        answers[file.name.split('_')[0]] += list(
            (int(line.split(';')[0]), questions.index(line.split(';')[1]), int(file.name.endswith(Config.correct_answers_ending))) for line in file.read_text().splitlines() if line.split(';')[1] in questions)
    return dict(sorted(answers.items(), key=lambda item: -item[1]))


if __name__ == '__main__':
    collect_data()
