from src.histographer.analysis.ranking.algorithms import balanced_rank_estimation, elo, rank_centrality, iterate_active_elo, active_elo
from src.histographer.analysis.ranking.mock import generate_mock_comparisons, generate_mock_comparisons_btl, save_dummy_gradient
from src.histographer.analysis.ranking.error import e_vs_error_rate, e_vs_n_comparisons, e_vs_n_objects
from src.histographer.analysis.ranking.high_level import suggest_pair
from random import sample
import numpy as np

N_COMPARISONS = 500
N_OBJECTS = 10
ERROR_RATE = 0.05

suggestion = suggest_pair([0, 1, 2], [(1, 2), (1, 2), (1, 0), (1, 0)], [(0, 2)])
print(suggestion)