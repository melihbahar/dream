import pytest
import pandas as pd

from ml.model.preprocess.preprocessor import Preprocessor

@pytest.fixture
def mock_dataframe():
    # Creating a mock DataFrame with numerical and categorical features
    data = {
        'numeric_feature_1': [1, 2, 3, 4],
        'numeric_feature_2': [5, 6, 7, 8],
        'categorical_feature_1': ['A', 'B', 'C', 'D'],
        'categorical_feature_2': ['X', 'Y', 'Z', 'W']
    }
    return pd.DataFrame(data)


def test_num_features(mock_dataframe):
    preprocessor = Preprocessor(mock_dataframe)
    num_features = preprocessor.num_features
    expected_num_features = ['numeric_feature_1', 'numeric_feature_2']

    assert num_features == expected_num_features


def test_cat_features(mock_dataframe):
    preprocessor = Preprocessor(mock_dataframe)
    cat_features = preprocessor.cat_features
    expected_cat_features = ['categorical_feature_1', 'categorical_feature_2']

    assert cat_features == expected_cat_features
