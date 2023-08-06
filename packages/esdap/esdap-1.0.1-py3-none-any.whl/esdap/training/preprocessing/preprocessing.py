from typing import List, Tuple

import numpy as np
import pandas as pd
from numba import njit


def preprocess(
    X_train, X_test, y_train, y_test, config
):

    print("--------------------------")
    print("Preprocessing")
    print()

    # generate sequence data 
    if config.classifier_name == "LSTM" or config.classifier_name == "CNN":
        X_train, y_train = generate_sequence_data(X_train, y_train, config)
        X_test, y_test = generate_sequence_data(X_test, y_test, config)

    # Standardize train and test data
    X_train, X_test = standardize(X_train, X_test, axis=(0, 1))

    return X_train, X_test, y_train, y_test


def standardize(X_train, X_test, axis=(0, 1)):

    print("--------------------------")
    print("Standardizing features")
    print()

    X = X_train.reshape(-1, X_train.shape[-1])

    mean = X.mean(axis=0)
    std = X.std(axis=0)
    std[std == 0.0] = 1.0

    X_train = (X_train - mean) / (std)
    X_test = (X_test - mean) / (std)

    return X_train, X_test


def normalize(y_train, y_test, axis=0):

    print("--------------------------")
    print("Normalizing labels")
    print()

    min = y_train.min(axis=axis)
    max = y_train.max(axis=axis)
    y_train = (y_train - min) / (max - min)
    y_test = (y_test - min) / (max - min)
    return y_train, y_test


def generate_sequence_data(X, y, config):

    if not X.ndim == 2:
        raise ValueError("X should be of dimensions [timestamp, features]")

    if not y.ndim == 2:
        raise ValueError("y should be of dimensions [timestamp, nr_classes]")

    stride = 1
    option = "majority"

    new_X = np.empty(
        (int((X.shape[0] - config.timesteps) / stride) + 1, config.timesteps, X.shape[1]),
        dtype=np.float32,
    )
    new_y = np.zeros(
        (int((X.shape[0] - config.timesteps) / stride) + 1, y.shape[1]), dtype=np.float32
    )

    sequence_ind = 0

    for i in range(0, X.shape[0] - config.timesteps + 1, stride):
        # extract sequence from sliding window over time series data
        new_X[sequence_ind] = X[i : i + config.timesteps]

        # Options to generate labels for sequence
        if option == "last":
            # 1. Take the last label of sequence
            new_y[sequence_ind] = y[i + config.timesteps - 1]

        elif option == "majority":
            # 2. Take the majority
            class_freq = y[i : i + config.timesteps].sum(axis=0)
            new_class_ind = class_freq.argmax()

        new_y[sequence_ind, new_class_ind] = 1

        # Increase sequence index counter
        sequence_ind += 1

    return new_X, new_y