from torch import nn

from ai_component.Encoder import Encoder


class PredictingModel(nn.Module):
    def __init__(
        self,
        n_sentences: int,
        encoding_size: int,
        encoder: Encoder = None,
        fc: nn.Linear = None,
    ):
        super().__init__()
        self.sigmoid = nn.Sigmoid()
        self.leaky_relu = nn.LeakyReLU()
        self.fc = fc
        self.encoder = encoder
        if self.encoder is None:
            self.encoder = Encoder(n_sentences=n_sentences, hidden_size=encoding_size)
        if self.fc is None:
            self.fc = nn.Linear(in_features=n_sentences, out_features=1)
        self.encoding_size = self.encoder.hidden_size
        self.n_sentences = n_sentences

    def forward(self, user_sentences: list[tuple[int, int]], current_time: int):
        if isinstance(user_sentences, list):
            user_sentences = self.encoder(user_sentences, current_time)
        output = self.fc(user_sentences)
        output = self.leaky_relu(output)
        return self.sigmoid(output)
