import atexit

import numpy as np
import torch
from torch import nn
from torch.optim import Adam

from Config import Config
from ai_component.ChanceCalculator import chance_calculator

bce_loss = nn.BCELoss()
optimizer = Adam(chance_calculator.parameters(), lr=1e-2)


def train_sample(samples: list[tuple[int, bool]], answer: bool):
    chance_calculator.train()
    optimizer.zero_grad()
    outputs = chance_calculator(samples)
    loss = bce_loss(outputs, torch.tensor(np.array([[float(answer)]])).float())
    loss.backward()
    optimizer.step()


@atexit.register
def save_weights():
    torch.save(chance_calculator.state_dict(), Config.model_weights)
