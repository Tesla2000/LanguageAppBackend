from datetime import datetime

import torch
from torch import nn
from torch.optim import Adam

from Config import Config
from ai_component.PredictingModel import PredictingModel
from ai_component.collect_data import collect_data
from ai_component.get_pretrained_model import get_pretrained_model
import sentences


def train_model():
    language_dict = getattr(sentences, Config.trained_language)
    if Config.use_pretrained:
        model = get_pretrained_model()
    else:
        model = PredictingModel(len(language_dict), Config.encoder_hidden_size)
    optimizer = Adam(model.parameters())
    loss_function = nn.BCELoss()
    data = collect_data(language_dict)
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
