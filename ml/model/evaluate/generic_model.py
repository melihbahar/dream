import pandas as pd
from sklearn.base import clone
from sklearn.base import BaseEstimator


class GenericModel:
    """
    A generic model class to make sure we can use any machine learning model with the necessary methods.

    Methods:
        fit(X: pd.DataFrame, Y: pd.DataFrame): Fit the model
        predict(X: pd.DataFrame): Predict on the given X
    """

    def __init__(self, model: BaseEstimator):
        self.model: BaseEstimator = clone(model)

    def fit(self, X: pd.DataFrame, Y: pd.DataFrame):
        self.model.fit(X, Y)

    def predict(self, X):
        return self.model.predict(X)
