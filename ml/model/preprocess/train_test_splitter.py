import pandas as pd
from sklearn.model_selection import train_test_split

from ml.common.logger import logger


class TrainTestSplitter:
    def __init__(self, df: pd.DataFrame, class_column: str):
        self.df = df
        self.class_column = class_column

        if class_column not in df.columns:
            raise ValueError(f"Target column '{class_column}' does not exist in the DataFrame.")

    def _create_test_set(self) -> pd.DataFrame:
        class_is_na: pd.Series = self.df[self.class_column].isna()
        self.log(f"Creating test set with {class_is_na.sum()} rows.")
        return self.df[class_is_na].drop([self.class_column], axis=1)

    def split(self, test_size: float, seed: int = None):
        if test_size < 0 or test_size > 1:
            raise ValueError(f"Test size must be between 0 and 1, but got {test_size}.")

        class_not_na: pd.Series = self.df[self.class_column].notna()

        X: pd.DataFrame = self.df[class_not_na].drop([self.class_column], axis=1)
        Y: pd.Series = self.df.loc[class_not_na, self.class_column]

        X_train, X_valid, Y_train, Y_valid = train_test_split(X, Y,
                                                              test_size=test_size,
                                                              random_state=seed)
        self.log(f"Split data into train and test sets with")

        # Get the test set from the rows where the class is missing
        X_test: pd.DataFrame = self._create_test_set()

        return X_train, X_valid, Y_train, Y_valid, X_test

    @staticmethod
    def log(msg: str) -> str:
        return logger.info(f'[Data] - {msg}')
