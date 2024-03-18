from collections import defaultdict

import torch
from torch import nn


class Encoder(nn.Module):
    def __init__(self, n_sentences: int, hidden_size: int):
        super().__init__()
        self.hidden_size = hidden_size
        self.n_sentences = n_sentences
        self.sigmoid = nn.Sigmoid()
        self.leaky_relu = nn.LeakyReLU(1e-4)
        self.gru = nn.GRU(2, hidden_size)
        self.fc = nn.Linear(in_features=hidden_size, out_features=1)

    def forward(
        self, user_sentences: list[tuple[int, int]], current_time: int
    ) -> torch.Tensor:
        encoding = torch.zeros(self.n_sentences)
        sentences = defaultdict(list)
        for user_sentence in user_sentences:
            sentences[user_sentence[1]] += [user_sentence[::2]]
        for sentence_index, user_sentences in sentences.items():
            hidden_state = torch.zeros((1, self.hidden_size))
            for (answer_time, is_answer_correct) in user_sentences:
                _, hidden_state = self.gru(
                    torch.Tensor(((current_time - answer_time, is_answer_correct),)),
                    hidden_state,
                )
                hidden_state = self.leaky_relu(hidden_state)
            encoding[sentence_index] = self.leaky_relu(self.fc(hidden_state))
        return self.sigmoid(encoding)
