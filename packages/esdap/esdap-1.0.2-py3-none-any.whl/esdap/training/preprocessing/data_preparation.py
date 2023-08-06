from pathlib import PurePath
from typing import List

import numpy as np
import pandas as pd

from .data_loader import load_data_from_config


def get_dataset(config, verbose=0):

    print("--------------------------")
    print("Getting dataset")
    print()

    ##########################################
    # 1.1. Loading data
    ##########################################
    features, labels, label_names, nb_classes = load_data_from_config(config)

    return features, labels, label_names, nb_classes
