from pathlib import Path


class Config:
    repetition_rate = 0.5
    root = Path(__file__).parent
    data_path = root / 'data'
    incorrect_answers_ending = '_incorrect_answers.txt'
    correct_answers_ending = '_correct_answers.txt'
    incorrect_answers_path = lambda login: Config.data_path / f"{login}{Config.incorrect_answers_ending}"
    correct_answers_path = lambda login: Config.data_path / f"{login}{Config.correct_answers_ending}"
    users_path = data_path / 'users.txt'


if not Config.users_path.exists():
    Config.users_path.write_text('')
