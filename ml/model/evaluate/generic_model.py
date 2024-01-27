import pandas as pd
from sklearn.base import clone
from sklearn.base import BaseEstimator


class GenericModel:
    def __init__(self, model: BaseEstimator):
        self.model: BaseEstimator = clone(model)

    def fit(self, X: pd.DataFrame, Y: pd.DataFrame):
        self.model.fit(X, Y)

    def predict(self, X):
        return self.model.predict(X)
