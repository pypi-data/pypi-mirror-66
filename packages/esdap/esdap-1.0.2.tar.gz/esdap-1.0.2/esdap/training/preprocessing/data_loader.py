import glob
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd


def load_data_from_config(config: dict, verbose=False):
    """Load features and labels into panda DataFrames (X, Y)

    Parameters
    ----------
    config: dict
        Dictionary containing all the required information for the current execution

    Returns
    -------
    X: DataFrame
        DataFrame containing the features for the specified patient in the form [timestep, features]

    Y: DataFrame
        DataFrame containing the labels in the form (ictal, preictal, postictal, interictal)

    label_names: list
        List containing the class names
    """

    print("--------------------------")
    print("Loading features and labels")
    print()

    patient_path = Path(config.data_path) / config.patient_name
    feature_files = glob.glob(str(patient_path / "*.dat"))

    df_list = []
    for file in feature_files:
        if (
            ("moments" in file and config.ft_moments)
            or ("peak_to_peak" in file and config.ft_peak_to_peak)
            or ("max_correlation" in file and config.ft_max_correlation)
            or ("decorrelation_time" in file and config.ft_decorrelation_time)
            or ("absolute_area" in file and config.ft_absolute_area)
            or ("dwt_coeffs" in file and config.ft_dwt_coeffs)
            or ("psd_ratio" in file and config.ft_psd_ratio)
            or ("SPLV" in file and config.ft_splv)
        ):
            features = pd.read_csv(
                file, header=0, index_col=0, sep=" ", dtype=np.float32
            )
            df_list.append(features)
            if verbose:
                print("Included: ", file)
        elif config.labels_filename in file:
            Y = pd.read_csv(file, sep=" ", dtype=np.float32)
            if verbose:
                print("Labels loaded")
        elif verbose:
            print("Excluded: ", file)

    # Features
    X = pd.concat(df_list, axis=1)

    # Extract label names
    label_names = list(Y)
    nb_classes = len(label_names)
    print(label_names)

    # Select only 2 classes of segments
    if config.binary_classification:
        class1 = config.first_class
        class2 = config.second_class
        label_names_sel = [label_names[class1], label_names[class2]]
        df_list = []
        df_list.append(Y[label_names[class1]])
        df_list.append(Y[label_names[class2]])
        Y = pd.concat(df_list, axis=1)
        label_names = list(Y)
        nb_classes = len(label_names)
        print(label_names)
        X.reset_index(drop=True, inplace=True)
        Y.reset_index(drop=True, inplace=True)
        temp = pd.concat([X, Y], axis=1)
        mask = (temp[label_names[0]] == 1) | (temp[label_names[1]] == 1)
        temp = temp.loc[
            mask,
        ]
        X = temp.iloc[:, : len(X.columns)]
        Y = temp.iloc[:, len(X.columns) :]

    # Assigns only one class to each segment with the priority
    # ictal > preictal > postictal > interictal
    for i in range(nb_classes - 1):
        for j in range(i + 1, nb_classes):
            mask = Y[label_names[i]] == 1
            Y.loc[mask, [label_names[j]]] = 0

    return X, Y, label_names, nb_classes
