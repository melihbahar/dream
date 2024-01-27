import os
import pickle

import pandas as pd
from ml.common.logger import logger


class Data:
    def __init__(self, class_column: str, path: str = 'data.csv'):
        self.path: str = path
        self.class_column: str = class_column
        self.dataset: pd.DataFrame = self.get()

    def get(self) -> pd.DataFrame:
        try:
            absolute_path: str = f'{os.getcwd()}/data/{self.path}'
            df: pd.DataFrame = pd.read_csv(absolute_path)
            self.log(f"Found {self.path} locally.")
        except Exception as e:
            self.log(f"Couldn't find {self.path}, using URL instead.")
            url = 'https://drive.google.com/file/d/1kqnB4J8FuF1k8xLIvfbPE1jsqUwd3wVH/view?usp=sharing'
            path = 'https://drive.google.com/uc?export=download&id=' + url.split('/')[-2]
            df: pd.DataFrame = pd.read_csv(path)

        return df.set_index('Id')

    @property
    def features(self) -> list:
        return self.dataset.drop(self.class_column, axis=1).columns.tolist()

    def save_feature_columns(self, path: str) -> None:
        try:
            pickle.dump(self.features, open(path, 'wb'))
            self.log(f"Succesfully saved feature columns to {path}")
        except Exception as e:
            self.log(f"Error saving feature columns to {path}: {e}")

    @staticmethod
    def log(msg: str) -> str:
        return logger.info(f'[Data] - {msg}')
