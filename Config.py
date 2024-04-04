from pathlib import Path


class _ModelConfig:
    use_pretrained = True
    encoder_hidden_size = 16
    model_file_name_format = "%Y%m%d%H%M%S"
    trained_language = "en_de"


class Config(_ModelConfig):
    worst_answers_percentile = 25
    maximal_repetition_rate = 0.95
    repetition_rate_factor = 1
    root = Path(__file__).parent
    data_path = root / "data"
    encoders = root / "encoders"
    fully_connected_layers = root / "fully_connected_layers"
    incorrect_answers_ending = "_incorrect_answers.txt"
    correct_answers_ending = "_correct_answers.txt"
    incorrect_answers_path = (
        lambda username, language: Config.data_path
        / f"{username}_{language}{Config.incorrect_answers_ending}"
    )
    correct_answers_path = (
        lambda username, language: Config.data_path
        / f"{username}_{language}{Config.correct_answers_ending}"
    )
    users_path = data_path / "users.txt"
    encoders.mkdir(exist_ok=True)
    fully_connected_layers.mkdir(exist_ok=True)


if not Config.users_path.exists():
    Config.users_path.write_text("")
