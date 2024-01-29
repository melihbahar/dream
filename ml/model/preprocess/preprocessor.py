import pickle
from typing import List, Tuple

import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from ml.common.logger import logger


class CategoricalPreprocessor:
    """
    Preprocessor class for categorical features.
    For now there are basic options but can be added more or different options.

    Attributes:
        categorical_features (List[str]): the list of categorical features to preprocess

    Methods:
        preprocess(): Creates the preprocessing pipeline with everything included.
    """
    def __init__(self, categorical_features: List[str]):
        self.categorical_features: List[str] = categorical_features

    @staticmethod
    def _one_hot_encoder() -> Tuple[str, OneHotEncoder]:
        """
        One hot encoder.
        """
        return ("one-hot_encoder", OneHotEncoder(sparse_output=False))

    @staticmethod
    def _category_imputer() -> Tuple[str, SimpleImputer]:
        """
        Imputer.for categorical features.
        Uses most_frequent strategy.
        """
        return ("imputer", SimpleImputer(strategy="most_frequent"))

    def preprocess(self) -> Pipeline:
        """
        Creates the preprocessing pipeline with everything included.

        Returns:
            Pipeline: The preprocess pipeline
        """
        return Pipeline(steps=[self._category_imputer(),
                               self._one_hot_encoder()]) \
            .set_output(transform="pandas")


class NumericalPreprocessor:
    """
    Preprocessor class for numeric features.
    For now there are basic options but can be added more or different options.

    Attributes:
        numerical_features (List[str]): the list of numeric features to preprocess

    Methods:
        preprocess(): Creates the preprocessing pipeline with everything included.
    """
    def __init__(self, numerical_features: List[str]):
        self.numerical_features: List[str] = numerical_features

    @staticmethod
    def _numeric_imputer() -> Tuple[str, SimpleImputer]:
        """
        Imputer.
        Only as an example here as wasn't really used in the given example.
        """
        return ("imputer", SimpleImputer())

    def preprocess(self) -> Pipeline:
        """
        Creates the preprocessing pipeline with everything included.

        Returns:
            Pipeline: The preprocess pipeline
        """
        return Pipeline(steps=[self._numeric_imputer()]) \
            .set_output(transform="pandas")


class Preprocessor:
    """
    The complete preprocessor that takes into account different preproccesing pipeline for different types (and possibly)
    groups of categories.

    Attributes:
        data (pd.DataFrame): The dataset to preprpcess
        class_column (str): The name of the class column to be taken into account when preprocessing.
    """
    def __init__(self, data: pd.DataFrame, class_column: str = None):
        self.data: pd.DataFrame = data
        self.class_column: str = class_column

        # If the class_column exists, check that it's in the columns and then remove from preprocessing.
        if self.class_column:
            if class_column not in self.data.columns:
                raise ValueError(f"Class column '{class_column}' does not exist in the DataFrame.")
            self.class_col = self.data[class_column]
            self.data = self.data.drop([class_column], axis=1)

    @property
    def cat_features(self) -> List[str]:
        return self._get_categorical_features()

    @property
    def num_features(self) -> List[str]:
        return self._get_numerical_features()

    def _get_categorical_features(self) -> List[str]:
        cat_features_df: pd.DataFrame = self.data.select_dtypes(include=['object'])
        return cat_features_df.columns.tolist()

    def _get_numerical_features(self) -> List[str]:
        num_features_df: pd.DataFrame = self.data.select_dtypes(include=['int64', 'float64'])
        return num_features_df.columns.tolist()

    def get_preprocess_pipeline(self) -> Pipeline:
        cat_features: List[str] = self.cat_features
        num_features: List[str] = self.num_features

        cat_processor: CategoricalPreprocessor = CategoricalPreprocessor(cat_features)
        num_processor: NumericalPreprocessor = NumericalPreprocessor(num_features)

        column_transformer: ColumnTransformer = \
            ColumnTransformer(transformers=[('categorical', cat_processor.preprocess(), cat_features),
                                            ('numerical', num_processor.preprocess(), num_features)],
                              remainder='passthrough',
                              verbose_feature_names_out=False)

        preprocess_pipeline: Pipeline = Pipeline(steps=[('column_transformer', column_transformer)]) \
            .set_output(transform="pandas")
        return preprocess_pipeline

    def save_pipeline(self, pipeline: Pipeline, path: str) -> None:
        try:
            pickle.dump(pipeline, open(path, 'wb'))
            self.log(f"Successfully saved pipeline to {path}")
        except Exception as e:
            self.log(f"Error saving pipeline to {path}: {e}")

    @staticmethod
    def log(msg: str) -> str:
        return logger.info(f'[PreProcessor] - {msg}')
