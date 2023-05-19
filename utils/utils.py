from scipy.sparse import csr_matrix
import numpy as np


def construct_user_item_matrix(filter_interaction):
    user_num = filter_interaction["remain_user_number"]
    item_num = filter_interaction["remain_item_number"]
    new_usermap = filter_interaction['new_usermap']
    triples = np.array(filter_interaction)
    users = triples[:, 0]
    items = triples[:, 1]
    scores = triples[:, 2]
    users = np.array( list(
        map(lambda user: new_usermap[user], users)
    ))
    user_item_matrix = csr_matrix((scores, (users, items)), shape=(user_num, item_num))
    return user_item_matrix
