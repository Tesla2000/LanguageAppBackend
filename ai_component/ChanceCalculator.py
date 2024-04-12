import torch
from torch import nn, no_grad

from Config import Config


class ChanceCalculator(nn.Module):
    def __init__(self, hidden_size: int):
        super().__init__()
        self.hidden_size = hidden_size
        self.sigmoid = nn.Sigmoid()
        self.leaky_relu = nn.LeakyReLU(1e-4)
        self.gru = nn.GRU(2, hidden_size)
        self.fc = nn.Linear(in_features=hidden_size, out_features=1)

    def forward(self, samples: list[tuple[int, bool]]) -> torch.Tensor:
        samples = torch.Tensor(samples).unsqueeze(1)
        hn = torch.zeros((1, self.hidden_size))
        for sample in samples:
            _, hn = self.gru(sample, hn)
        return self.sigmoid(self.fc(hn))

    @no_grad()
    def predict(self, samples: list[tuple[int, bool]]) -> float:
        self.eval()
        return self.forward(samples).item()


chance_calculator = ChanceCalculator(Config.model_hidden_size)
if Config.model_weights.exists():
    chance_calculator.load_state_dict(torch.load(Config.model_weights))
