import pytest
import pandas as pd

from ml.model.preprocess.train_test_splitter import TrainTestSplitter


@pytest.fixture
def sample_dataframe():
    data = {
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'class': [0, 1, 0, 1, 0]
    }
    return pd.DataFrame(data)


def test_invalid_class_column(sample_dataframe):
    with pytest.raises(ValueError) as e:
        splitter = TrainTestSplitter(sample_dataframe, 'nonexistent_column')
    assert str(e.value) == "Target column 'nonexistent_column' does not exist in the DataFrame."

def test_split(sample_dataframe):
    splitter = TrainTestSplitter(sample_dataframe, 'class')
    X_train, X_valid, Y_train, Y_valid, X_test = splitter.split(test_size=0.2, seed=42)

    assert len(X_train) == len(Y_train)
    assert len(X_valid) == len(Y_valid)
