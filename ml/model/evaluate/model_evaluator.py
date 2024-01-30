import pickle
from enum import Enum
from typing import Union, Dict, Any, Type

from ml.common.logger import logger
from ml.model.evaluate.generic_model import GenericModel
from ml.model.evaluate.score import ScoreExtender


class ScoreCriteria(Enum):
    """
    Enum for Scoring Criteria.
    Important to give predefined options for criteria to prevent logic or analytical bugs.
    """
    MIN = 'min'
    MAX = 'max'


class ScoreType(Enum):
    # Add here any new score type
    RMSE = 'RMSE'
    MAE = 'MAE'
    CUSTOM_SCORE = 'CUSTOM_SCORE'


class ModelEvaluator:
    """
    Class for evaluating machine learning models.

    Methods:
        evaluate(model: GenericModel, X_valid, Y_valid, score_func: Type[ScoreExtender]):
            Evaluate the model using the specified scoring function.
        choose_best_model(scores: Dict[str, Any], criteria: ScoreCriteria, score_type: ScoreType):
            Choose the best model based on a specific scoring criterion.
        save_model(model, path: str):  Save the model to a file.
    """

    def __init__(self):
        pass

    def evaluate(self, model: GenericModel, X_valid, Y_valid, score_func: Type[ScoreExtender]) -> float:
        """
        Evaluate the model using the specified scoring function.

        Args:
            model (GenericModel): The trained machine learning model.
            X_valid: Validation dataset features.
            Y_valid: Validation dataset class.
            score_func (Type[ScoreExtender]): The scoring function to use.

        Returns:
            float: The evaluation metric.
        """

        self.log('Evaluating the model')
        y_pred = model.predict(X_valid)
        return score_func(Y_valid, y_pred)()

    @staticmethod
    def choose_best_model(scores: Dict[str, Any], criteria: ScoreCriteria, score_type: ScoreType) -> Union[str, None]:
        """
        Choose the best model based on a specific scoring criterion.

        Args:
            scores (Dict[str, Any]): Dictionary containing model names as keys and their scores as values.
            criteria (ScoreCriteria): The scoring criteria to use for selection.
            score_type (ScoreType): The type of score to consider. Needs to be one of the keys of each model in the scores dictionary.

        Returns:
            Union[str, None]: The name of the best model.
        """

        specific_scores: Dict[str, float] = {key: value.get(score_type.value) for key, value in scores.items()}
        if criteria is ScoreCriteria.MIN:
            return min(specific_scores, key=specific_scores.get)
        elif criteria is ScoreCriteria.MAX:
            return max(specific_scores, key=specific_scores.get)

    def save_model(self, model, path: str):
        """
        Save the model to a file.

        Args:
            model: The trained machine learning model.
            path (str): The path to save the model.
        """

        try:
            pickle.dump(model, open(path, 'wb'))
            self.log(f'Model saved successfully to {path}')
        except Exception as e:
            self.log(f'Failed to save model: {e}')

    @staticmethod
    def log(msg: str) -> str:
        return logger.info(f'[Evaluator] - {msg}')
