from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from numpy.linalg import norm
from utils.utils import construct_user_item_matrix
import torch.nn as nn

def ucf_s(filter_interaction, knear=2):
    user_item_matrix = construct_user_item_matrix(filter_interaction)
    user_sim_matrix = cosine_similarity(user_item_matrix)
    # user_topk: (user #,  knear)
    user_topk = np.argpartition(user_sim_matrix, -knear, axis=1)[-knear:]
    new_user_item_matrix = np.empty(user_item_matrix.shape)
    for user, topk in enumerate(user_topk):
        weights = user_sim_matrix[user, topk]
        weights /= norm(weights)
        new_user_item_matrix[user, :] = weights @ user_item_matrix[topk, :]
    return new_user_item_matrix

def ucf_p(filter_interaction, knear=2):
    user_item_matrix = construct_user_item_matrix(filter_interaction)
    user_sim_matrix = np.corrcoef(user_item_matrix.todense())
    # user_topk: (user #,  knear)
    user_topk = np.argpartition(user_sim_matrix, -knear, axis=1)[-knear:]
    new_user_item_matrix = np.empty(user_item_matrix.shape)
    for user, topk in enumerate(user_topk):
        weights = user_sim_matrix[user, topk]
        weights /= norm(weights)
        new_user_item_matrix[user, :] = weights @ user_item_matrix[topk, :]
    return new_user_item_matrix

def icf_s(filter_interaction, knear=2):
    item_user_matrix = construct_user_item_matrix(filter_interaction).transpose()
    item_sim_matrix = cosine_similarity(itemm_user_matrix)
    # item_topk: (item #,  knear)
    item_topk = np.argpartition(item_sim_matrix, -knear, axis=1)[-knear:]
    new_item_user_matrix = np.empty(item_user_matrix.shape)
    for item, topk in enumerate(item_topk):
        weights = item_sim_matrix[item, topk]
        weights /= norm(weights)
        new_item_user_matrix[user, :] = weights @ item_user_matrix[topk, :]
    return new_item_user_matrix

def icf_p(filter_interaction, knear=2):
    item_user_matrix = construct_user_item_matrix(filter_interaction).transpose()
    item_sim_matrix = np.corrcoef(itemm_user_matrix.todense())
    # item_topk: (item #,  knear)
    item_topk = np.argpartition(item_sim_matrix, -knear, axis=1)[-knear:]
    new_item_user_matrix = np.empty(item_user_matrix.shape)
    for item, topk in enumerate(item_topk):
        weights = item_sim_matrix[item, topk]
        weights /= norm(weights)
        new_item_user_matrix[user, :] = weights @ item_user_matrix[topk, :]
    return new_item_user_matrix

class MatrixFactorization(nn.Module):
    def __init__(self, user_num, item_num, factor_num=20):
        super().__init__()
        # create X, theta matrix
        self.user_factors = nn.Embedding(user_num, factor_num)
        self.item_factors = nn.Embedding(item_num, factor_num)

    def forward(self, user, item):
        return (self.user_factors(user) * self.item_factors(item)).sum(1)

class FactorizationMachine(nn.Module):
    def __init__(self, feature_num, factor_num=20):
        super().__init__()
        # create X, theta matrix
        self.V = nn.Parameter(torch.randn((feature_num, factor_num)))
        self.W = nn.Linear(feature_num, 1, bias=True)

    def forward(self, x):
        linear_term = self.W(x)
        interaction_term = torch.mm(
            torch.mm(x, self.V), torch.mm(self.V.T, x.T)
        )
        return linear_term + interaction_term
