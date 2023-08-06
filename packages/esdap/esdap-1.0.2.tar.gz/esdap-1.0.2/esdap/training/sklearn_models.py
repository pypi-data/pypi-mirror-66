from argparse import Namespace

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier


def build_model(config: Namespace):
    """Build a sklearn model according to the configuration dictionary.

    Parameters
    ----------
    config: dict
        Dictionary containing the all arguments used as configuration

    Returns
    -------
    model: sklearn model
        Model costructed according to configuration
    """
    if config.classifier_name == "RandomForest":
        model = RandomForestClassifier(n_jobs=-1, n_estimators=150)
    elif config.classifier_name == "XGBoost":
        model = XGBClassifier(n_jobs=6, n_estimators=5)
    elif config.classifier_name == "GradientBoosting":
        model = GradientBoostingClassifier(n_estimators=500)
    elif config.classifier_name == "SVM":
        model = SVC()
    else:
        # TODO Error handling
        print("Classifier name does not match no available classifier")
        model = None

    return model
