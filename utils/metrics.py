from sklearn.metrics import mean_squared_error, recall_score, ndcg_score
import numpy as np
from math import sqrt

class Metrics:
    def __init__(self, topk=10, threshold=3.5):
        self.topk = topk
        self.threshold = threshold
        self.y_true, self.y_pred = None, None
        self.valid_idices = None

    def feed(y_true, y_pred, valid_idices):
        if self.y_true is not None:
            self.y_true = np.array(y_true)
            self.y_pred = np.array(y_pred)
            self.valid_idices = valid_idices
        else:
            print("You have already feed the values!!")

    def get_score(self):
        score_dict = {
            "rmse": self._calculate_rmse(),
            "recall": self._calculate_recall(),
            "ndcg": self._calculate_ndcg()
        }
        return score_dict

    def _calculate_rmse(self):
        y_true = self.y_true[self.valid_idices]
        y_pred = self.y_pred[self.valid_idices]
        return sqrt(mean_squared_error(y_true, y_pred))

    def _calculate_recall(self):
        top_indices = np.argsort(self.y_pred)[:self.topk]
        top_indices = list( set(top_indices).intersection(set(self.valid_idices)) )
        y_pred = np.where(
            self.y_pred[top_indices] >= self.threshold, 1, 0
        )
        y_true = np.where(
            self.y_true[top_indices] >= self.threshold, 1, 0
        )
        return sqrt(recall_score(y_true, y_pred))

    def _calculate_ndcg(self):
        top_indices = np.argsort(self.y_pred)[:self.topk]
        top_indices = list( set(top_indices).intersection(set(self.valid_idices)) )
        y_pred = np.where(
            self.y_pred[top_indices] >= self.threshold, 1, 0
        )
        y_true = np.where(
            self.y_true[top_indices] >= self.threshold, 1, 0
        )
        return sqrt(ndcg_score(y_true, y_pred))
