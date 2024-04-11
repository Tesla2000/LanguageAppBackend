from collections import defaultdict

import torch
from torch import nn

from Config import Config


class ChanceCalculator(nn.Module):
    def __init__(self, hidden_size: int):
        super().__init__()
        self.hidden_size = hidden_size
        self.sigmoid = nn.Sigmoid()
        self.leaky_relu = nn.LeakyReLU(1e-4)
        self.gru = nn.GRU(2, hidden_size)
        self.fc = nn.Linear(in_features=hidden_size, out_features=1)

    def forward(
        self,
    ) -> torch.Tensor:
        pass


chance_calculator = ChanceCalculator(Config.model_hidden_size)
