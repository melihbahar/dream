from abc import ABC, abstractmethod
from typing import Callable, TypeVar

import numpy as np
from sklearn import metrics


class Score(ABC):
    def __init__(self, ytrue, ypred: np.ndarray):
        self.ytrue = ytrue
        self.ypred = ypred

    @abstractmethod
    def __call__(self) -> float:
        pass


class RMSE(Score):
    def __call__(self) -> float:
        return np.sqrt(metrics.mean_squared_error(self.ytrue, self.ypred))

    @property
    def name(self) -> str:
        return 'RMSE'


class MAE(Score):
    def __call__(self) -> float:
        return metrics.mean_absolute_error(self.ytrue, self.ypred)

    @property
    def name(self) -> str:
        return 'MAE'


class CustomScore(Score):
    def __init__(self, score_func: Callable, ytrue, ypred):
        super().__init__(ytrue, ypred)
        self.score_func = score_func

    def __call__(self) -> float:
        return self.score_func(self.ytrue, self.ypred)


ScoreExtender = TypeVar('ScoreExtender', bound=Score)
