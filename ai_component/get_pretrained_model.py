import torch
from torch import nn

from Config import Config
from ai_component.Encoder import Encoder
from ai_component.PredictingModel import PredictingModel
from sentences import sentences


def get_pretrained_model() -> PredictingModel:
    encoder = Encoder(len(sentences), Config.encoder_hidden_size)
    encoder.load_state_dict(
        torch.load(max(Config.encoders.iterdir(), key=lambda file: file.name))
    )
    fc = nn.Linear(len(sentences), 1)
    fc.load_state_dict(
        torch.load(
            max(Config.fully_connected_layers.iterdir(), key=lambda file: file.name)
        )
    )
    return PredictingModel(len(sentences), Config.encoder_hidden_size, encoder, fc)
