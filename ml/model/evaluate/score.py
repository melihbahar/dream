from abc import ABC, abstractmethod
from typing import Callable, TypeVar

import numpy as np
from sklearn import metrics


class Score(ABC):
    """
    An abstract class to create a scoring function for the machine learning models.
    """
    def __init__(self, ytrue, ypred: np.ndarray):
        self.ytrue = ytrue
        self.ypred = ypred

    @abstractmethod
    def __call__(self) -> float:
        pass


class RMSE(Score):
    """
    Root mean squared error.
    Uses sklearn.metrics.mean_squared_error to be calculated.
    """
    def __call__(self) -> float:
        return np.sqrt(metrics.mean_squared_error(self.ytrue, self.ypred))

    @property
    def name(self) -> str:
        return 'RMSE'


class MAE(Score):
    """
    Mean absolute error.
    Uses sklearn.metrics.mean_absolute_error to be calculated.
    """
    def __call__(self) -> float:
        return metrics.mean_absolute_error(self.ytrue, self.ypred)

    @property
    def name(self) -> str:
        return 'MAE'


class CustomScore(Score):
    """
    An example of a custom class function.
    It can either be initiated with a custom scoring function or the scoring function can be implemented
    already within with a custom name

    Attributes:
        score_func (Callable): The custom function to be used
        ytrue (np.ndarray): The true labels
        ypred (np.ndarray): The predicted labels
    """
    def __init__(self, score_func: Callable, ytrue, ypred):
        super().__init__(ytrue, ypred)
        self.score_func = score_func

    def __call__(self) -> float:
        return self.score_func(self.ytrue, self.ypred)


# The extender for the Score class for type annotations
ScoreExtender = TypeVar('ScoreExtender', bound=Score)
