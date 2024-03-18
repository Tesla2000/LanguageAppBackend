from datetime import datetime

import torch
from torch import nn
from torch.optim import Adam

from Config import Config
from ai_component.Encoder import Encoder
from ai_component.PredictingModel import PredictingModel
from ai_component.collect_data import collect_data
from sentences import sentences


def train_model():
    if Config.use_pretrained:
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
        model = PredictingModel(len(sentences), Config.encoder_hidden_size, encoder, fc)
    else:
        model = PredictingModel(len(sentences), Config.encoder_hidden_size)
    optimizer = Adam(model.parameters())
    loss_function = nn.BCELoss()
    data = collect_data()
    for user_sentences in data.values():
        previous_sentences = []
        for next_sentence in user_sentences:
            outputs = model(previous_sentences, next_sentence[0])
            optimizer.zero_grad()
            loss = loss_function(outputs, torch.Tensor([next_sentence[2]]))
            loss.backward()
            optimizer.step()
            previous_sentences.append(next_sentence)
    torch.save(
        model.encoder.state_dict(),
        Config.encoders.joinpath(
            datetime.now().strftime(Config.model_file_name_format)
        ).with_suffix(".pth"),
    )
    torch.save(
        model.fc.state_dict(),
        Config.fully_connected_layers.joinpath(
            datetime.now().strftime(Config.model_file_name_format)
        ).with_suffix(".pth"),
    )


if __name__ == "__main__":
    train_model()
