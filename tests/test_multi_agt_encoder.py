"""Test the multi-agents encoder."""
from typing import Tuple
# import sys
import random
import pytest

import torch
from torch.nn.utils.rnn import pack_sequence
# sys.path.append('/home/quentinb/DCA')
from settings.model import build_multi_agt_encoder


@pytest.mark.parametrize(
    "n_agents, embedding_dim, hsz, n_contextual_layers, bsz, seq_len_range",
    [(3, 64, 32, 2, 9, (20, 40))])
def test_encoder(n_agents: int, embedding_dim: int,
                 hsz: int, n_contextual_layers: int,
                 bsz: int, seq_len_range: Tuple[int, int]):
    ma_encoder = build_multi_agt_encoder(
        n_agents=n_agents,
        embedding_dim=embedding_dim,
        hidden_size=hsz,
        n_contextual_layers=n_contextual_layers,
    )

    src_len = seq_len_range[1]
    articles = [torch.rand(random.randint(*seq_len_range), embedding_dim)
                for _ in range(bsz*n_agents-1)]
    articles.append(torch.rand(src_len, embedding_dim))

    embedded_article = pack_sequence(articles, enforce_sorted=False)

    encoded_seq, state = ma_encoder(embedded_article)

    assert list(encoded_seq.shape) == [src_len, bsz, n_agents, hsz], (
        f"{encoded_seq.shape} != {[src_len, bsz, n_agents, hsz]}"
    )
    assert list(state.shape) == [bsz, hsz], (
        f"{state.shape} != {[bsz, hsz]}"
    )