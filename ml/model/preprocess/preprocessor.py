from typing import List, Tuple

import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


class CategoricalPreprocessor:
    def __init__(self, categorical_features: List[str]):
        self.categorical_features: List[str] = categorical_features

    @staticmethod
    def _one_hot_encoder() -> Tuple[str, OneHotEncoder]:
        return ("one-hot_encoder", OneHotEncoder(sparse_output=False))

    @staticmethod
    def _category_imputer() -> Tuple[str, SimpleImputer]:
        return ("imputer", SimpleImputer(strategy="most_frequent"))

    def preprocess(self) -> Pipeline:
        return Pipeline(steps=[self._category_imputer(),
                               self._one_hot_encoder()]) \
            .set_output(transform="pandas")


class NumericalPreprocessor:
    def __init__(self, numerical_features: List[str]):
        self.numerical_features: List[str] = numerical_features

    @staticmethod
    def _numeric_imputer() -> Tuple[str, SimpleImputer]:
        return ("imputer", SimpleImputer())

    def preprocess(self) -> Pipeline:
        return Pipeline(steps=[self._numeric_imputer()]) \
            .set_output(transform="pandas")


class Preprocessor:
    def __init__(self, data: pd.DataFrame, class_column: str):
        self.data: pd.DataFrame = data
        self.class_column: str = class_column

        if class_column not in data.columns:
            raise ValueError(f"Class column '{class_column}' does not exist in the DataFrame.")

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

    def _filter_class_column(self, features: List[str]) -> List[str]:
        return [f for f in features if f != self.class_column]

    def preprocess(self) -> pd.DataFrame:
        # Class column should not be included in the preprocessing
        cat_features: List[str] = self._filter_class_column(self.cat_features)
        num_features: List[str] = self._filter_class_column(self.num_features)

        cat_processor: CategoricalPreprocessor = CategoricalPreprocessor(cat_features)
        num_processor: NumericalPreprocessor = NumericalPreprocessor(num_features)

        column_transformer: ColumnTransformer = \
            ColumnTransformer(transformers=[('categorical', cat_processor.preprocess(), cat_features),
                                            ('numerical', num_processor.preprocess(), num_features)],
                              remainder='passthrough',
                              verbose_feature_names_out=False)

        preprocess_pipeline: Pipeline = Pipeline(steps=[('column_transformer', column_transformer)]) \
            .set_output(transform="pandas")

        return preprocess_pipeline.fit_transform(self.data)
