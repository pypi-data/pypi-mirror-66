import numpy as np
import pandas as pd


def assert_equal(value1, value2):
    assert value1 == value2, "Values are different " + str(value1) + " " + str(value2)


def assert_contains_nan(data):
    if isinstance(data, pd.DataFrame):
        assert not data.isnull().values.any(), "Data contains NaN"
    elif isinstance(data, np.ndarray):
        assert not np.isnan(data).any(), "Data contains NaN"
