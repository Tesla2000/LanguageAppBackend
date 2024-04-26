from pathlib import Path


class _ModelConfig:
    worst_answers_percentile = 25
    maximal_repetition_rate = 0.95
    required_confidence = 0.8
    repetition_rate_factor = 1
    use_pretrained = True
    model_hidden_size = 16
    trained_language = "en_de"


class Config(_ModelConfig):
    recent_answer_count_to_accept = 1
    recent_answer_time_threshold = 20
    repeat_question_at_random_chance = .25
    very_common_factor = 0.25
    common_factor = 0.15
    root = Path(__file__).parent
    sentences = root / "sentences"
    data_path = root / "data"
    open_ai_api_key = root / "api_key"
    database = root / "database" / "app.db"
    model_weights = root / "model_weights.pth"
