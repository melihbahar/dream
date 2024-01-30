import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

from ml.common.logger import logger
from ml.data.data import Data
from ml.model.evaluate.generic_model import GenericModel
from ml.model.preprocess.preprocessor import Preprocessor
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from ml.model.evaluate.model_evaluator import ModelEvaluator, ScoreType
from ml.model.evaluate.score import RMSE, MAE
from ml.model.preprocess.train_test_splitter import TrainTestSplitter
from ml.model.evaluate.model_evaluator import ScoreCriteria


def train():
    class_column: str = 'SalePrice'
    test_size: float = 0.2

    # Load the data
    data: Data = Data(class_column)
    dataset: pd.DataFrame = data.dataset
    class_col_df: pd.DataFrame = dataset[class_column]

    # Preprocessing
    set_preprocessor: Preprocessor = Preprocessor(data=dataset,
                                                  class_column=class_column)
    preprocess_pipeline: Pipeline = set_preprocessor.get_preprocess_pipeline()
    fit_preprocess_pipeline = preprocess_pipeline.fit(dataset.drop([class_column], axis=1))

    # Save the pipeline - we will need it for prediction later
    # That's why we only save the "fit" pipeline before the "transform" step
    set_preprocessor.save_pipeline(fit_preprocess_pipeline,
                                   f'preprocess_pipeline.pickle')

    # Transform the dataset
    processed_df = fit_preprocess_pipeline.transform(dataset)
    processed_df = pd.concat([processed_df, class_col_df], axis=1)

    # Split the dataset
    splitter = TrainTestSplitter(df=processed_df,
                                 class_column=class_column)
    X_train, X_valid, Y_train, Y_valid, X_test = splitter.split(test_size=test_size)

    models = {
        'SVR': GenericModel(svm.SVR()),
        'RFR': GenericModel(RandomForestRegressor(n_estimators=10)),
        'LR': GenericModel(LinearRegression())
    }

    evaluator: ModelEvaluator = ModelEvaluator()

    scores = {}
    for model_name, model in models.items():
        model_scores = scores[model_name] = {}

        logger.info(f'[Training] - Training the {model_name} model')
        model.fit(X_train, Y_train)

        model_scores['RMSE'] = evaluator.evaluate(model, X_valid, Y_valid, RMSE)
        model_scores['MAE'] = evaluator.evaluate(model, X_valid, Y_valid, MAE)

    best_model_name: str = evaluator.choose_best_model(scores,
                                                       ScoreCriteria.MIN,
                                                       ScoreType.RMSE)

    logger.info(f'[Training] - Best model is {best_model_name}')

    best_model: GenericModel = models.get(best_model_name)
    evaluator.save_model(best_model,
                         f'final_model.pickle')


if __name__ == '__main__':
    train()
