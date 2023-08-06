# -*- coding: utf-8 -*-
"""A collection of useful functions from ESDaP."""

import glob
import json
import logging
from datetime import timedelta
from os import path
from pathlib import Path

import mne
import numpy as np
import numpy.ma as ma

from esdap.helpers.parsers import (
    parse_chb_summary,
    parse_gt_24_hours_time,
    parse_neonatal_annotations,
)

__all__ = [
    "parse_chb_summary",
    "parse_neonatal_annotations",
    "parse_gt_24_hours_time",
    "calculate_binary_labels",
    "calculate_seizure_start_end_timepoints",
    "get_times_until_and_since_seizures",
    "get_header_for_feature",
]

logger = logging.getLogger(name=__name__)


def get_segment_start_indexes(n_measurements, window_length, stride=None, tiling=None):
    """Compute segment start times based on window_length, stride or tiling.

    Parameters
    ----------
    n_measurements: int
        How many indexes there are to segment.
    window_length: int
        How long a window is.
    stride: int
        How much the start of consecutive windows is shifted.
    tiling: int
        How much consecutive windows overlap.

    Returns
    -------
    numpy.ndarray
        Array of indexes where segments start
    """

    if all((window_length, stride, tiling)):
        if (tiling + stride) != window_length:
            raise ValueError("Tiling, segment length and stride are incompatible.")

    if stride is None and tiling is None:
        stride = window_length

    if stride is None and tiling:
        stride = window_length - tiling

    segment_starts = np.arange(0, n_measurements - window_length + 1, stride)

    return segment_starts


def calculate_binary_labels(
    segment_start_times,
    segment_length,
    seizures,
    preictal_duration: int,
    postictal_duration: int,
):
    """Calculate segment labels based on seizure annotations for given pre- and
    postictal durations.

    Parameters
    ----------
    segment_start_times: numpy.ndarray
        Start times of segments to be labelled.
    segment_length : int
        The length of the segment in seconds.
    seizures : tuple(float)
        A tuple containing a seizure start and end time.
    preictal_duration : int
        The preictal duration in seconds.
    postictal_duration : int
        The postictal duration in seconds.

    Returns
    -------
    numpy.ndarray
        One hot encoded segment labels for ictal, preictal, postictal and interictal.
    """

    labels = np.zeros((len(segment_start_times), 3), dtype=int)
    interictal_per_seizure = np.zeros(
        (len(segment_start_times), len(seizures)), dtype=int
    )

    segment_end_times = segment_start_times + segment_length - 1

    preictal_period_in_s = preictal_duration * 60
    postictal_period_in_s = postictal_duration * 60

    for i, (segment_start, segment_end) in enumerate(
        zip(segment_start_times, segment_end_times)
    ):
        for j, seizure in enumerate(seizures):
            if (
                seizure[0] <= segment_start <= seizure[1]
                or seizure[0] <= segment_end <= seizure[1]
                or segment_start
                <= seizure[0]
                <= segment_end  # whole seizure in segment
            ):
                # ictal
                labels[i, 0] = 1
            if ((seizure[0] - preictal_period_in_s) <= segment_start < seizure[0]) or (
                (seizure[0] - preictal_period_in_s) <= segment_end < seizure[0]
            ):
                # preictal
                labels[i, 1] = 1
            if (seizure[1] < segment_start <= (seizure[1] + postictal_period_in_s)) or (
                seizure[1] < segment_end <= (seizure[1] + postictal_period_in_s)
            ):
                # postictal
                labels[i, 2] = 1
            if (
                segment_end < (seizure[0] - preictal_period_in_s)
                or (seizure[1] + postictal_period_in_s) < segment_start
            ):
                interictal_per_seizure[i, j] = 1

    # only retain interictal label for segments that are interictal for all seizures
    iil = np.prod(interictal_per_seizure, axis=1)
    fil = np.reshape(iil, (iil.size, 1))
    labels = np.append(labels, fil, axis=1)
    logger.info(
        (
            f"Number of labeled segments: ictal: {labels.sum(axis=0)[0]}, "
            f"preictal: {labels.sum(axis=0)[1]}, "
            f"postictal: {labels.sum(axis=0)[2]}, "
            f"interictal: {labels.sum(axis=0)[3]}"
        )
    )
    return labels


def recompute_labels(feature_file, preictal_duration: int, postictal_duration: int):
    """Compute labels for a feature file.

    Parameters
    ----------
    feature_file: str
        Feature file for which the labels should be computed.
    preictal_duration : int
        The preictal duration in seconds.
    postictal_duration : int
        The postictal duration in seconds.

    Returns
    -------
    numpy.ndarray
        One hot encoded segment labels for ictal, preictal, postictal and interictal.
    """

    with open(path.join(path.dirname(feature_file), "seizure_times.json")) as file:
        seizures_times = json.load(file)

    with open(feature_file + ".conf.json") as file:
        config = json.load(file)

    segment_length = config["segment_length"]

    timestamps = np.loadtxt(feature_file, skiprows=1, usecols=(0))
    labels = calculate_binary_labels(
        timestamps,
        segment_length,
        seizures_times,
        preictal_duration,
        postictal_duration,
    )
    return labels


def recompute_and_store_labels(
    feature_file, preictal_duration: int, postictal_duration: int
):
    """Compute labels for a feature file.

    Parameters
    ----------
    feature_file: str
        Feature file for which the labels should be computed.
    preictal_duration : int
        The preictal duration in seconds.
    postictal_duration : int
        The postictal duration in seconds.

    Returns
    -------
    numpy.ndarray
        One hot encoded segment labels for ictal, preictal, postictal and interictal.
    """

    labels = recompute_labels(feature_file, preictal_duration, postictal_duration)

    labels_file = str(
        Path(feature_file).parent
        / f"labels-pre{preictal_duration}-post{postictal_duration}.dat"
    )

    with open(labels_file, mode="w") as file:
        file.write(" ".join(["ictal", "preictal", "postictal", "interictal"]) + "\n")
        np.savetxt(file, labels[:])

    return labels


def calculate_seizure_start_end_timepoints(summary_file):
    current_time = timedelta(seconds=0)
    start_end_times = []

    summary = parse_chb_summary(summary_file)

    for file in summary["edf_files_ordered"]:
        file_summarry = summary["edf_files"][file]  # file summary

        file_start_day = current_time.days

        eeg_start_file = parse_gt_24_hours_time(file_summarry["eeg_start_time"])
        if eeg_start_file.days != 0:
            raise ValueError("We do not handle start times >= 24 hours.")

        eeg_start = eeg_start_file + timedelta(days=file_start_day)

        if eeg_start < current_time:
            eeg_start += timedelta(days=1)
            logger.info(
                (
                    "incrementing start day",
                    file,
                    file_summarry["eeg_start_time"],
                    file_summarry["eeg_end_time"],
                )
            )

        current_time = eeg_start

        logger.info((file, eeg_start_file, eeg_start))

        eeg_end_file = parse_gt_24_hours_time(file_summarry["eeg_end_time"])
        eeg_end = eeg_end_file + timedelta(days=eeg_start.days)
        if eeg_end < eeg_start:
            eeg_end = eeg_end + timedelta(days=1)
            logger.info(
                (
                    "incrementing end day",
                    file,
                    file_summarry["eeg_start_time"],
                    file_summarry["eeg_end_time"],
                )
            )

        # Because we can only guess how long the measurement is from the start and end times,
        # we get the measurement length form the data file itself.
        measurement_duration_seconds = (
            mne.io.read_raw_edf(
                path.join(path.dirname(summary_file), file), verbose=False
            ).n_times
            / 256
        )

        logger.info(
            (
                "P:",
                file,
                eeg_start.total_seconds(),
                measurement_duration_seconds,
                eeg_end.total_seconds(),
                "current_time",
                current_time,
            )
        )

        eeg_start_seconds = eeg_start.total_seconds()
        eeg_end_seconds = eeg_end.total_seconds()

        if (eeg_start_seconds + measurement_duration_seconds) != eeg_end_seconds:
            raise ValueError(
                (
                    f"('{measurement_duration_seconds} {eeg_start}')"
                    "{int(eeg_start.total_seconds() + measurement_duration_seconds)} != "
                    "{int(eeg_end.total_seconds())}"
                )
            )

        for seizure in file_summarry["seizures"]:
            start_end = np.array(
                list(
                    map(
                        int,
                        [
                            file_summarry["seizures"][seizure]["start"],
                            file_summarry["seizures"][seizure]["end"],
                        ],
                    )
                )
            )
            start_end_from_eeg_start = start_end + current_time.total_seconds()
            start_end_times.append([start_end_from_eeg_start])

        current_time = eeg_end

    return start_end_times


def get_times_until_and_since_seizures(timestamps, seizures):
    """Compute the times relative to seizure start and end times.

    From the real `timestamps` (i.e. those representing a time of day),
    compute the *t*ime *u*ntil *n*ext *s*eizure *s*tarts and
    the *t*ime *s*ince *l*ast *s*eizure *e*nded.

    Parameters
    ----------
    timestamps : array_like
        Array of timestamps.
    seizures : list of tuples
        Each element in the list is a 2-tuple, the first tuple element
        being a seizure start time, the 2nd a seizure end time.

    Returns
    -------
    times : tuple
        A 2-tuple of numpy.ndarrays. The first array contains the time until next
        seizure starts, the 2nd contains the time since last seizure ended.

    Notes
    -----
    Any values that are too early or late to be calculated are returned
     with a fill value of np.nan
    """

    seizures_start, seizures_end = zip(*seizures)

    # Broadcast the seizure_start array to get the differences between time and seizures
    tunss = timestamps - np.asarray(seizures_start).reshape((len(seizures_start), 1))
    # Mask any values > 0 i.e. time is after a previous seizure had started
    masked_tunss = ma.masked_where(tunss > 0, tunss)
    # For each timepoint, find the max which corresponds to the nearest seizure
    # Using .filled will return a numpy.ndarray rather than the masked array
    unmasked_tunss_max = masked_tunss.max(axis=0).filled(fill_value=np.nan)

    tslse = timestamps - np.asarray(seizures_end).reshape((len(seizures_end), 1))
    masked_tslse = ma.masked_where(tslse < 0, tslse)
    unmasked_tslse_min = masked_tslse.min(axis=0).filled(fill_value=np.nan)

    return unmasked_tunss_max, unmasked_tslse_min


def generate_labels_files(config):
    times = [5, 10, 15, 20, 25]
    for time in times:
        patient_path = Path(config.data_path) / config.patient_name
        feature_file = glob.glob(str(patient_path / "moments.dat"))

        recompute_and_store_labels(feature_file[0], patient_path, time, time)


def get_header_for_feature(feature_name, num_channels):
    """Make the header for the feature file.

    Parameters:
    ----------
    feature_name : str
        REQUIRED: which feature to make the header for
    num_channels : int
        REQUIRED: How many channels are used in calculating feature `feature_name`

    Returns
    -------
    column_names : list
        A list of column names that will make the header
    """

    if feature_name == "moments":
        moments_names = [
            [
                "mean_" + str(i),
                "var_" + str(i),
                "skew_" + str(i),
                "kurtosis_" + str(i),
                "stdev_" + str(i),
            ]
            for i in range(1, num_channels + 1)
        ]
        moments_names = [item for sublist in moments_names for item in sublist]
        column_names = [["timepoints"], moments_names]
    elif feature_name == "peak_to_peak":
        column_names = [
            ["timepoints"],
            ["peak_to_peak_" + str(i) for i in range(1, num_channels + 1)],
        ]
    elif feature_name == "absolute_area":
        column_names = [
            ["timepoints"],
            ["absolute_area_" + str(i) for i in range(1, num_channels + 1)],
        ]
    elif feature_name == "psd_ratio":
        ratio_header = [
            "psd_ratio_band_" + str(i) + "_channel_" + str(j)
            for j in range(1, num_channels + 1)
            for i in range(8)  # hardcoding
        ]
        column_names = [
            ["timepoints"],
            [x.replace("ratio_band_0", "total_EEG_energy") for x in ratio_header],
        ]
    elif feature_name == "decorrelation_time":
        column_names = [
            ["timepoints"],
            ["decorrelation_time_" + str(i) for i in range(1, num_channels + 1)],
        ]
    elif feature_name == "dwt_coeffs":
        column_names = [
            ["timepoints"],
            [
                "dwt_coeffs_" + str(i) + "_channel_" + str(j)
                for j in range(1, num_channels + 1)
                for i in range(1, 9)  # hardcoding
            ],
        ]
    elif feature_name == "max_correlation":
        corr_names = []
        n_channels = num_channels
        for channel_a in range(1, n_channels + 1):
            for channel_b in range(channel_a + 1, n_channels + 1):
                corr_names.append(
                    "correlation_between_channel_"
                    + str(channel_a)
                    + "_and_"
                    + str(channel_b)
                )
        column_names = [["timepoints"], corr_names]
    elif feature_name == "SPLV":
        n_channels = num_channels
        len_hilbert_signals = 7  # hardcoding: 7 should be len(hilbert_signals)
        splv_names = (
            [None] * int(n_channels * (n_channels - 1) / 2) * len_hilbert_signals
        )
        idx = 0
        for i in range(len_hilbert_signals):
            for channel_a in range(1, n_channels + 1):
                for channel_b in range(channel_a + 1, n_channels + 1):
                    splv_names[idx] = (
                        "SPLV_signal_"
                        + str(i)
                        + "_between_channel_"
                        + str(channel_a)
                        + "_and_"
                        + str(channel_b)
                    )
                    idx += 1
        column_names = [["timepoints"], splv_names]
    else:
        raise ValueError(
            f"ERROR in feature_name: Unknown feature name {feature_name}. Options are:\n"
            "moments peak_to_peak absolute_area psd_ratio decorrelation_time dwt_coeffs "
            "max_correlation SPLV"
        )

    column_names = [item for sublist in column_names for item in sublist]
    return column_names
