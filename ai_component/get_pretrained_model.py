import torch
from torch import nn

from Config import Config
from ai_component.Encoder import Encoder
from ai_component.PredictingModel import PredictingModel
import sentences


def get_pretrained_model() -> PredictingModel:
    language_dictionary = getattr(sentences, Config.trained_language)
    encoder = Encoder(len(language_dictionary), Config.encoder_hidden_size)
    encoder.load_state_dict(
        torch.load(max(Config.encoders.iterdir(), key=lambda file: file.name))
    )
    fc = nn.Linear(len(language_dictionary), 1)
    fc.load_state_dict(
        torch.load(
            max(Config.fully_connected_layers.iterdir(), key=lambda file: file.name)
        )
    )
    return PredictingModel(
        len(language_dictionary), Config.encoder_hidden_size, encoder, fc
    )
