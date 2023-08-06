import collections
import datetime
import json
from os import path
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from mlflow import log_artifact, log_metric
from sklearn.metrics import classification_report, confusion_matrix

from ..helpers.clr_callback import CyclicLR
from ..helpers.decay_callback import step_decay_schedule
from ..helpers.oclr_callback import OneCycleLR


def flatten(d, parent_key="", sep="_"):
    """Flatten a nested dictionary.

    Parameters
    ----------
    d: dict
        Nested dictionary to flatten

    parent_key: str
        String used for the recursive concatenation of the keys

    sep: str
        Separator used between levels of the dictionary

    Returns
    -------
    items: dict
        Dictionary obtained by flattening the input dictionary (d)
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_metrics(model, X_test, y_test, nb_classes):
    """Compute and return the metrics on the trained model.

    Parameters
    ----------
    model: sklearn model
        trained sklearn model

    X_test: DataFrame
        test features

    y_test: DataFrame
        test labels

    Returns
    -------
    report: dict
        Dictionary containing all the metrics
    """

    print("--------------------------")
    print("Getting metrics")
    print()

    y_pred = model.predict(X_test)

    y_t = y_test

    # np.savetxt('y_test_metrics.txt', y_test, delimiter=' ')
    # np.savetxt('y_pred_metrics.txt', y_pred, delimiter=' ')

    if nb_classes == 2:
        y_p = y_pred.round()
    else:
        y_t = y_test.argmax(axis=1)
        y_p = y_pred.argmax(axis=1)

    report = classification_report(y_t, y_p, output_dict=True)

    flattened_report = flatten(report)
    formatted_report = dict()
    for k, v in flattened_report.items():
        formatted_report["CR_" + k] = flattened_report[k]

    return flatten(formatted_report)


def get_confusion_matrices(model, X_test, y_test):
    """Compute and return the metrics on the trained model.

    Parameters
    ----------
    model: sklearn model
        trained sklearn model

    X_test: DataFrame
        test features

    y_test: DataFrame
        test labels

    Returns
    -------
    report: dict
        Dictionary containing all the metrics
    """

    print("--------------------------")
    print("Getting confusion matrices")
    print()

    y_pred = model.predict(X_test)

    y_t = y_test
    y_p = y_pred

    if y_t.ndim > 1:
        y_t = y_test.argmax(axis=1)
        y_p = y_pred.argmax(axis=1)

    conf_matrix_true = confusion_matrix(y_t, y_p, normalize="true")
    conf_matrix_all = confusion_matrix(y_t, y_p, normalize="all")
    conf_matrix_pred = confusion_matrix(y_t, y_p, normalize="pred")

    return conf_matrix_all, conf_matrix_pred, conf_matrix_true


def get_LRCallback(config, min_lr, max_lr, train_samples):
    """Returns the specified Learning Rate Callback, if among the available
    ones, None otherwise.

    Parameters
    ----------
    config: dict
        Dictionary containing all the information required to run a tensorflow pipeline

    Returns
    -------
    lr_callback: tf.keras.callbacks
        Learning Rate Callback
    """

    if config.lr_callback == "step":
        lr_callback = step_decay_schedule(
            initial_lrate=min_lr,
            decay_factor=config.decay_factor,
            decay_step_size=config.decay_step_size,
        )
    elif config.lr_callback == "cyclic":
        step_size = config.decay_step_size * (train_samples // config.batch_size)
        lr_callback = CyclicLR(
            base_lr=min_lr,
            max_lr=max_lr,
            step_size=step_size,
            mode=config.decay_mode,
            gamma=config.decay_gamma,
        )
    elif config.lr_callback == "one_cycle":
        max_mom = None
        min_mom = None

        if config.optimizer == "SGD":
            max_mom = config.max_momentum
            min_mom = config.min_momentum

        lr_callback = OneCycleLR(
            max_lr=max_lr,
            end_percentage=config.end_percentage,
            maximum_momentum=max_mom,
            minimum_momentum=min_mom,
        )
    elif config.lr_callback == "None":
        lr_callback = None
    else:
        print("Selected learning rate callback is not available")
        lr_callback = None

    return lr_callback


def get_avg_metrics(runs_metrics):

    avg_macro_avg_f1_score = 0
    avg_macro_avg_precision = 0
    avg_macro_avg_recall = 0
    avg_val_accuracy = 0

    for run_metrics in runs_metrics:
        avg_macro_avg_f1_score += run_metrics[0].history["val_macro_average_f1-score"][
            -1
        ]
        avg_macro_avg_precision += run_metrics[0].history[
            "val_macro_average_precision"
        ][-1]
        avg_macro_avg_recall += run_metrics[0].history["val_macro_average_recall"][-1]
        avg_val_accuracy += run_metrics[0].history["val_accuracy"][-1]

    avg_macro_avg_f1_score /= len(runs_metrics)
    avg_macro_avg_precision /= len(runs_metrics)
    avg_macro_avg_recall /= len(runs_metrics)
    avg_val_accuracy /= len(runs_metrics)

    avg_metrics = {
        "avg_val_macro_avg_f1-score": avg_macro_avg_f1_score,
        "avg_val_macro_avg_precision": avg_macro_avg_precision,
        "avg_val_macro_avg_recall": avg_macro_avg_recall,
        "avg_val_accuracy": avg_val_accuracy,
    }

    return avg_metrics


def get_avg_metrics_sklearn(runs_metrics):

    avg_macro_avg_f1_score = 0
    avg_macro_avg_precision = 0
    avg_macro_avg_recall = 0
    avg_val_accuracy = 0

    for run_metrics in runs_metrics:
        avg_macro_avg_f1_score += run_metrics[1]["CR_macro avg_f1-score"]
        avg_macro_avg_precision += run_metrics[1]["CR_macro avg_precision"]
        avg_macro_avg_recall += run_metrics[1]["CR_macro avg_recall"]
        avg_val_accuracy += run_metrics[1]["CR_accuracy"]

    avg_macro_avg_f1_score /= len(runs_metrics)
    avg_macro_avg_precision /= len(runs_metrics)
    avg_macro_avg_recall /= len(runs_metrics)
    avg_val_accuracy /= len(runs_metrics)

    avg_metrics = {
        "avg_val_macro_avg_f1-score": avg_macro_avg_f1_score,
        "avg_val_macro_avg_precision": avg_macro_avg_precision,
        "avg_val_macro_avg_recall": avg_macro_avg_recall,
        "avg_val_accuracy": avg_val_accuracy,
    }

    return avg_metrics
