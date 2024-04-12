from pathlib import Path


class _ModelConfig:
    worst_answers_percentile = 25
    maximal_repetition_rate = 0.95
    required_confidence = .8
    repetition_rate_factor = 1
    use_pretrained = True
    model_hidden_size = 16
    trained_language = "en_de"


class _DatabaseConfig:
    question_answers_table = "QuestionAnswers"


class Config(_ModelConfig, _DatabaseConfig):
    very_common_factor = .35
    common_factor = .15
    root = Path(__file__).parent
    sentences = root / "sentences"
    data_path = root / "data"
    open_ai_api_key = root / "api_key"
    database = root / "database" / 'app.db'
    users_path = data_path / "users.txt"
    model_weights = root / "model_weights.pth"


if not Config.users_path.exists():
    Config.users_path.write_text("")
