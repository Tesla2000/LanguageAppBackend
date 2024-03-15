from pathlib import Path


class Config:
    repetition_rate = 0.5
    root = Path(__file__).parent
    data_path = root / 'data'
    incorrect_answers_path = lambda login: Config.data_path / f"{login}_incorrect_answers.txt"
    correct_answers_path = lambda login: Config.data_path / f"{login}_correct_answers.txt"
