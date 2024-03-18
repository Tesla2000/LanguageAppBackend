import torch
from torch import nn
from torch.optim import Adam

from ai_component.PredictingModel import PredictingModel
from ai_component.collect_data import collect_data
from sentences import sentences


def train_model():
    model = PredictingModel(len(sentences))
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


if __name__ == '__main__':
    train_model()
