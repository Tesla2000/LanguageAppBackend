from collections import defaultdict

import torch
from torch import nn


class PredictingModel(nn.Module):
    def __init__(self, n_sentences: int, encoding_size: int = 16, gru: nn.GRU = None):
        super().__init__()
        self.encoding_size = encoding_size
        self.n_sentences = n_sentences
        self.fc = nn.Linear(in_features=n_sentences * encoding_size, out_features=1)
        self.sigmoid = nn.Sigmoid()
        self.leaky_relu = nn.LeakyReLU()
        self.gru = gru
        if self.gru is None:
            self.gru = nn.GRU(2, encoding_size)

    def encode(self, user_sentences: list[tuple[int, int]], current_time: int) -> torch.Tensor:
        encoding = torch.zeros((self.n_sentences, self.encoding_size))
        sentences = defaultdict(list)
        for user_sentence in user_sentences:
            sentences[user_sentence[1]] += [user_sentence[::2]]
        for sentence_index, user_sentences in sentences.items():
            user_sentences = torch.Tensor(tuple(tuple((current_time - answer_time, is_answer_correct)) for (answer_time, is_answer_correct) in user_sentences))
            _, features = self.gru(user_sentences)
            encoding[sentence_index] = self.leaky_relu(features)
        return encoding.flatten()

    def forward(self, user_sentences: list[tuple[int, int]], current_time: int):
        if isinstance(user_sentences, list):
            user_sentences = self.encode(user_sentences, current_time)
        output = self.fc(user_sentences)
        output = self.leaky_relu(output)
        return self.sigmoid(output)
