import pickle
from enum import Enum
from typing import Union, Dict, Any

from ml.model.evaluate.generic_model import GenericModel
from ml.model.score import ScoreExtender


class ScoreCriteria(Enum):
    MIN = 'min'
    MAX = 'max'


class ModelEvaluator:

    def __init__(self):
        pass

    def evaluate(self, model: GenericModel, X_valid, Y_valid, score_func: ScoreExtender) -> float:
        y_pred = model.predict(X_valid)
        return score_func(Y_valid, y_pred)()

    def choose_best_model(self, scores: Dict[str, Any], criteria: ScoreCriteria, score_type: str) -> Union[str, None]:
        specific_scores: Dict[str, float] = {key: value.get(score_type) for key, value in scores.items()}
        if criteria is ScoreCriteria.MIN:
            return min(specific_scores, key=specific_scores.get)
        elif criteria is ScoreCriteria.MAX:
            return max(specific_scores, key=specific_scores.get)

    def save_model(self, model, path: str):
        with open(path, 'wb') as f:
            pickle.dump(model, f)
