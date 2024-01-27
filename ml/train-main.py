import os
import sys

import pandas as pd

from ml.common.logger import logger
from ml.data.data import Data
from ml.model.evaluate.generic_model import GenericModel
from ml.model.preprocess.preprocessor import Preprocessor
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from ml.model.evaluate.model_evaluator import ModelEvaluator
from ml.model.evaluate.score import RMSE, MAE
from ml.model.preprocess.train_test_splitter import TrainTestSplitter
from ml.model.evaluate.model_evaluator import ScoreCriteria

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def train():
    # script_dir = os.path.dirname(__file__)
    # target_dir = os.path.abspath(os.path.join(script_dir, '..', 'app', 'api', 'model'))
    target_dir = 'artifacts'

    class_column = 'SalePrice'

    data = Data(class_column)
    dataset = data.dataset
    class_col_df = dataset[class_column]

    data.save_feature_columns(f'{target_dir}/feature_columns.pickle')

    set_preprocessor: Preprocessor = Preprocessor(data=dataset, class_column=class_column)
    preprocess_pipeline: Pipeline = set_preprocessor.get_preprocess_pipeline()
    fit_preprocess_pipeline = preprocess_pipeline.fit(dataset.drop([class_column], axis=1))

    set_preprocessor.save_pipeline(fit_preprocess_pipeline,
                                   f'{target_dir}/preprocess_pipeline.pickle')

    processed_df = fit_preprocess_pipeline.transform(dataset)
    processed_df = pd.concat([processed_df, class_col_df], axis=1)

    splitter = TrainTestSplitter(df=processed_df, class_column='SalePrice')
    X_train, X_valid, Y_train, Y_valid, X_test = splitter.split(test_size=0.2)

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

    # TODO: make this function accept Score object instead of string
    best_model_name: str = evaluator.choose_best_model(scores,
                                                       ScoreCriteria.MIN,
                                                       'RMSE')

    logger.info(f'[Training] - Best model is {best_model_name}')

    best_model = models.get(best_model_name)
    evaluator.save_model(best_model,
                         f'{target_dir}/final_model.pickle')


if __name__ == '__main__':
    train()
