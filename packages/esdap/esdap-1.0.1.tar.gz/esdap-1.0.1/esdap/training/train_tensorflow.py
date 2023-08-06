import argparse
from datetime import datetime
from distutils.util import strtobool
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
from mlflow import log_artifact, log_metrics, set_tag, start_run

from .helpers.metrics_callback import MetricsCallback
from .helpers.utils import (
    get_metrics,
    get_confusion_matrices,
    get_avg_metrics
)
from .preprocessing.data_preparation import get_dataset
from .preprocessing.preprocessing import preprocess
from .tensorflow_models import build_model


def execute_pipeline(config):
    """Executes the tensorflow training pipeline.

    Parameters
    ----------
    config: dict
        Namespace containing all the configuration needed to run a tensorflow pipeline

    Returns
        Stores the results of the pipeline on a MLflow local/remote server
    -------
    """

    with start_run(nested=True):

        set_tag("mlflow.runName", config.run_name)

        runs_metrics = []
        runs_conf_matrices = []

        # Getting dataset
        features, labels, label_names, nb_classes = get_dataset(config)
        X = features.to_numpy()
        y = labels.to_numpy()

        # Getting KFold splits
        kf = KFold(n_splits=config.n_splits, random_state=None, shuffle=True)
        i = 0
        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            
            tf.keras.backend.clear_session()

            with start_run(
                run_name=config.run_name + "_" + "Split_" + str(i), nested=True
            ):

                print("--------------------------")
                print(f"Running split {i}:")
                print()

                # Preprocess Data
                X_train, X_test, y_train, y_test = preprocess(
                    X_train, X_test, y_train, y_test, config
                )

                # Build Model
                model, summary = build_model(
                    config, X_train, y_train
                )

                # Defining Callbacks
                metrics_callback = MetricsCallback()

                callbacks = [
                    metrics_callback,
                ]

                print("--------------------------")
                print("Fitting model")
                print("Data Shapes before fit:")

                batch_size = 64

                model_history = model.fit(
                    X_train, y_train,
                    batch_size=batch_size,
                    epochs=config.epochs,
                    callbacks=callbacks,
                    validation_data=(X_test, y_test)
                )

                if label_names is not None and len(label_names) != y_train.shape[1]:
                    label_names = None

                # Evaluate/Test Model and Save Metrics
                metrics = get_metrics(model, X_test, y_test, nb_classes)

                # MLFlow log metrics
                log_metrics(metrics)

                # Confusion matrix generation and logging
                (
                    conf_matrix_all,
                    conf_matrix_pred,
                    conf_matrix_true,
                ) = get_confusion_matrices(model, X_test, y_test)

                runs_metrics.append((model_history, metrics))

                runs_conf_matrices.append(
                    (conf_matrix_all, conf_matrix_pred, conf_matrix_true)
                )
                
            i += 1

        avg_metrics = get_avg_metrics(runs_metrics)
        log_metrics(avg_metrics)
        set_tag("model_summary", summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tensorflow Classifier Training Script"
    )

    parser.add_argument(
        "--run_name",
        type=str,
        default="Run",
        metavar="N",
        help="Name to give to the run (default: Run)",
    )

    parser.add_argument(
        "--data_path",
        type=str,
        default="data",
        metavar="N",
        help="Path to data directory (default: data)",
    )

    parser.add_argument(
        "--patient_name",
        type=str,
        default="chb06",
        metavar="N",
        help="Name of patient folder (default: chb06)",
    )

    parser.add_argument(
        "--labels_filename",
        type=str,
        default="labels-pre30-post30",
        metavar="N",
        help="Labels filename (default: labels-pre30-post30)",
    )

    parser.add_argument(
        "--classifier_name",
        type=str,
        default="FCN",
        metavar="N",
        help="Classifier to use for training (default: FCN)",
    )

    parser.add_argument(
        "--binary_classification",
        type=lambda x: bool(strtobool(x)),
        default=False,
        metavar="N",
        help="Flag deciding whether to perform binary classification preictal-interictal (default: False)"
    )

    parser.add_argument(
        "--timesteps",
        type=int,
        default="10",
        metavar="N",
        help="Timesteps for LSTM and CNN (default: 10)",
    )

    parser.add_argument(
        "--n_splits",
        type=int,
        default=1,
        metavar="N",
        help="Number of 3Fold train-test splits to consider (default: 1)",
    )

    parser.add_argument(
        "--random_seed",
        type=lambda x: bool(strtobool(x)),
        default=False,
        metavar="N",
        help=(
            "Flag deciding whether to use or not a random seed in the model building (default: False)"
        ),
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=30,
        metavar="N",
        help="Training epochs (default: 30)",
    )

    parser.add_argument(
        "--ft_moments",
        type=lambda x: bool(strtobool(x)),
        default=True,
        metavar="N",
        help="Flag deciding whether to use or not the moments features class (default: True)",
    )

    parser.add_argument(
        "--ft_peak_to_peak",
        type=lambda x: bool(strtobool(x)),
        default=True,
        metavar="N",
        help="Flag deciding whether to use or not the peak_to_peak features class (default: True)",
    )

    parser.add_argument(
        "--ft_max_correlation",
        type=lambda x: bool(strtobool(x)),
        default=True,
        metavar="N",
        help="Flag deciding whether to use or not the max_correlation features class (default: True)",
    )

    parser.add_argument(
        "--ft_decorrelation_time",
        type=lambda x: bool(strtobool(x)),
        default=True,
        metavar="N",
        help="Flag deciding whether to use or not the decorrelation_time features class (default: True)",
    )

    parser.add_argument(
        "--ft_absolute_area",
        type=lambda x: bool(strtobool(x)),
        default=True,
        metavar="N",
        help="Flag deciding whether to use or not the absolute_area features class (default: True)",
    )

    parser.add_argument(
        "--ft_dwt_coeffs",
        type=lambda x: bool(strtobool(x)),
        default=True,
        metavar="N",
        help="Flag deciding whether to use or not the dwt_coeffs features class (default: True)",
    )

    parser.add_argument(
        "--ft_psd_ratio",
        type=lambda x: bool(strtobool(x)),
        default=True,
        metavar="N",
        help="Flag deciding whether to use or not the psd_ratio features class (default: True)",
    )

    parser.add_argument(
        "--ft_splv",
        type=lambda x: bool(strtobool(x)),
        default=True,
        metavar="N",
        help="Flag deciding whether to use or not the splv features class (default: True)",
    )

    config = parser.parse_args()

    execute_pipeline(config)
