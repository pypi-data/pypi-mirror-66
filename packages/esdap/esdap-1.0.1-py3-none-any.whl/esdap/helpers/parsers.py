"""Parsers for various files and strings."""

import datetime
import os
import re

import pandas as pd


def parse_gt_24_hours_time(time_string, time_of_day: bool = False):
    """Parses a time string and returns the time-of-day.
    Code partially from https://stackoverflow.com/a/24432718
    The rationale is exemplified in the following error message:
        ValueError: time data '25:12:12' does not match format '%H:%M:%S'

    Args:
        str: a time string of the format hours:minutes:seconds
        time_of_day: remove full days from timespan

    Returns:
        datetime.timedelta
    """

    hours, minutes, seconds = map(int, time_string.split(":"))
    time_delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    if time_of_day:
        time_delta = datetime.timedelta(seconds=time_delta.seconds)
    return time_delta


def parse_chb_summary(filename):
    """Parses summary files from the physionet.org CHB-MIT dataset.

    Args:
        file (str), REQUIRED: path to summary file

    Returns:
        dict: {'patient': {'id': 'chb06'},
               'sampling_rate': 256},
               'edf_files': {'chb06_01.edf': {'edf_file_name': [basename],
                                              'eeg_end_time': str,
                                              'eeg_start_time': str,
                                              'file_number': '01',
                                              'seizure_count': 3,
                                              'seizures': {'1': {'end': 7811,
                                                                 'start': 7799}, ...},
                                              'channels': {'1': 'FP1-F7', ...}
                                             }, ... },
                'edf_files_ordered'
    """

    patient_id = os.path.basename(filename).split("-")[0]
    chb_summary = {"patient": {"id": patient_id}, "edf_files": {}}
    with open(filename, "r") as file:
        sampling_chk, *file_chks = file.read().split("\n\n")

    sampling_rate_search = re.search(
        r"^Data Sampling Rate: (\d+) Hz$", sampling_chk, re.MULTILINE
    )
    if sampling_rate_search:
        chb_summary["sampling_rate"] = int(sampling_rate_search.group(1))
    else:
        raise ValueError(f"Unable to retrieve sampling rate from {filename}.")

    chb_summary["edf_files_ordered"] = []

    for file_chk in file_chks:

        if file_chk == "":
            # ignore empty file chunks
            continue

        # Handle channel changes
        if file_chk.startswith("Channels"):
            channels = dict(re.findall(r"Channel (\d+): (.+$)", file_chk, re.MULTILINE))
            continue

        match = re.search(
            (
                r"^File Name: (?P<edf_file_name>.+\.edf)\n"
                r"File Start Time: (?P<eeg_start_time>\d{1,2}:\d{2}:\d{2})\n"
                r"File End Time: (?P<eeg_end_time>\d{1,2}:\d{2}:\d{2})\n"
                r"Number of Seizures in File: (?P<seizure_count>\d+)$"
            ),
            file_chk,
            re.MULTILINE | re.DOTALL,
        )

        if match:
            edf_file_name = match.group(1)
            chb_summary["edf_files_ordered"].append(edf_file_name)
            file_number = edf_file_name.rstrip(".edf").split("_")[-1]
            chb_summary["edf_files"][edf_file_name] = match.groupdict()
            chb_summary["edf_files"][edf_file_name]["file_number"] = file_number
            chb_summary["edf_files"][edf_file_name]["seizure_count"] = int(
                match.groupdict()["seizure_count"]
            )
        else:
            raise ValueError(
                f"Unable to parse file chunk '{file_chk}' from {filename}."
            )

        chb_summary["edf_files"][edf_file_name]["channels"] = channels

        if match.groupdict()["seizure_count"] != "0":
            seizures = re.findall(
                (
                    r"Seizure (?P<s_n>\d+) Start Time: (?P<s_start>\d+) seconds\n"
                    r"Seizure \d+ End Time: (?P<s_end>\d+) seconds"
                ),
                file_chk,
                re.MULTILINE,
            )
            chb_summary["edf_files"][edf_file_name]["seizures"] = {
                seizure[0]: {"start": int(seizure[1]), "end": int(seizure[2])}
                for seizure in seizures
            }
        else:
            chb_summary["edf_files"][edf_file_name]["seizures"] = {}

    return chb_summary


def parse_neonatal_annotations(filename, which_polar_data):
    """Parses annotation files from the neonatal dataset.

    Args:
        file (str), REQUIRED: path to annotation file
        which_polar_data (str), REQUIRED: Either 'unipolar' or 'bipolar'

    Returns:
        dict: {'sampling_rate': 256,
               'channels': {'1':'EEG Fp1-REF', '2': 'EEG Fp2-REF', ...}
               OR 'channels': {'1': 'FP1-F7', '2': 'F7-T7', ... '18': 'CZ-PZ'},
               'patients': {str : {'id': int,
                                  'eeg_start_time': str,
                                  'eeg_end_time': str,
                                  'eeg_end_time_in_seconds': int,
                                  'eeg_file_name': 'eeg[id].edf',
                                  'seizure_count': int,
                                  'total_ictal_seconds': int,
                                  'seizures': {1: {'start': int, 'end': int},
                                               2: {'start': int, 'end': int},
                                               ...
                                              }
                                  },
                            str : {'id': int,
                                   ...as above...,
                                  },
                           }
               }
    """

    annotations = pd.read_csv(filename, dtype="float64")

    df = annotations.copy()

    # get the lagged differences between (0,1)-annotated rows
    dfdiff = df.diff()
    # The second where a seizure starts will have a difference of 1
    seizure_starts = annotations[dfdiff == 1].copy()
    # The second where a seizure ends will have a difference of -1
    seizure_ends = annotations[dfdiff == -1].copy()

    # For every patient only keep the second a seizure starts
    seizure_starts_dict = {col: seizure_starts[col].dropna() for col in seizure_starts}
    # Get the timepoints as a list for each patient
    for col in seizure_starts_dict:
        seizure_starts_dict[str(col)].index.name = "Time"
        seizure_starts_dict[str(col)] = seizure_starts_dict[str(col)].reset_index()
        seizure_starts_dict[str(col)] = list(
            seizure_starts_dict[str(col)].loc[:, "Time"]
        )

    # Equivalent for seizure end but note that we must subtract one from the
    # timepoint found because it represents the first non-ictal second,
    # rather than the required last ictal second
    seizure_ends_dict = {col: seizure_ends[col].dropna() for col in seizure_ends}
    for col in seizure_ends_dict:
        seizure_ends_dict[str(col)].index.name = "Time"
        seizure_ends_dict[str(col)] = seizure_ends_dict[str(col)].reset_index()
        seizure_ends_dict[str(col)] = list(
            seizure_ends_dict[str(col)].loc[:, "Time"] - 1
        )

    # the last annotated second of each patients' recording
    eeg_end_time = dict(df.apply(pd.Series.last_valid_index))

    # some recordings start with a seizure which is missed by the lagged differences
    # method so we need to add them back in.
    # First count the number of seizure starts and ends per patient
    seizure_count_starts = [len(x) for x in seizure_starts_dict.values()]
    seizure_count_ends = [len(x) for x in seizure_ends_dict.values()]
    seizure_count = {
        i + 1: max(seizure_count_starts[i], seizure_count_ends[i])
        for i, _ in enumerate(seizure_count_starts)
    }

    # locate patients where the first row is annotated as 1 i.e. ictal
    patients_who_begin_with_ictal = df.loc[0, df.loc[0,] == 1.0]
    for key in seizure_starts_dict.keys():
        if key in patients_who_begin_with_ictal:
            # insert a seizure start from time=0
            seizure_starts_dict[key].insert(0, 0)

    # Sometimes recordings end with an ictal second
    # Find if any final annotated values are ictal
    final_annotation_value = {
        col: df.loc[eeg_end_time[str(col)], str(col)]
        for col in range(1, len(df.columns) + 1)
    }
    patients_who_end_with_ictal = [
        key for key, value in final_annotation_value.items() if value == 1.0
    ]
    if patients_who_end_with_ictal:
        for k in seizure_ends_dict.keys():
            if int(k) in patients_who_end_with_ictal:
                # insert a seizure end at the final annotated timepoint
                seizure_ends_dict[str(k)].append(eeg_end_time[str(k)])

    # check we now have equal lengths for start and end
    assert [len(x) for x in seizure_starts_dict.values()] == [
        len(x) for x in seizure_ends_dict.values()
    ]

    # total seconds scored as ictal
    cumsum_df = df.cumsum()
    total_ictal = {
        col: cumsum_df.loc[annotations[col].last_valid_index(), col]
        for col in annotations
    }

    unipolar_channels = [
        "EEG Fp1-REF",
        "EEG Fp2-REF",
        "EEG F3-REF",
        "EEG F4-REF",
        "EEG C3-REF",
        "EEG C4-REF",
        "EEG P3-REF",
        "EEG P4-REF",
        "EEG O1-REF",
        "EEG O2-REF",
        "EEG F7-REF",
        "EEG F8-REF",
        "EEG T3-REF",
        "EEG T4-REF",
        "EEG T5-REF",
        "EEG T6-REF",
        "EEG Fz-REF",
        "EEG Cz-REF",
        "EEG Pz-REF",
    ]
    bipolar_channels = [
        "FP1-F7",
        "F7-T7",
        "T7-P7",
        "P7-O1",
        "FP1-F3",
        "F3-C3",
        "C3-P3",
        "P3-O1",
        "FP2-F4",
        "F4-C4",
        "C4-P4",
        "P4-O2",
        "FP2-F8",
        "F8-T8",
        "T8-P8",
        "P8-O2",
        "FZ-CZ",
        "CZ-PZ",
    ]

    if which_polar_data == "unipolar":
        channels = unipolar_channels
    elif which_polar_data == "bipolar":
        channels = bipolar_channels
    else:
        raise ValueError(
            "Error in specifying the required data."
            " Need to know whether to use 'unipolar' or 'bipolar' data"
        )

    neonatal_summary = {}
    neonatal_summary["sampling_rate"] = 256
    neonatal_summary["channels"] = {str(i + 1): j for i, j in enumerate(channels)}
    neonatal_summary["patients"] = {
        str(x): {"id": x} for x in range(1, len(df.columns) + 1)
    }

    for patient_id in range(1, len(df.columns) + 1):
        neonatal_summary["patients"][str(patient_id)]["eeg_start_time"] = "11:11:11"
        neonatal_summary["patients"][str(patient_id)]["eeg_end_time"] = str(
            datetime.timedelta(seconds=40271)  # hardcoded time above in seconds
            + datetime.timedelta(seconds=int(eeg_end_time[str(patient_id)]))
        )
        neonatal_summary["patients"][str(patient_id)][
            "eeg_end_time_in_seconds"
        ] = eeg_end_time[str(patient_id)]
        neonatal_summary["patients"][str(patient_id)]["eeg_file_name"] = (
            "eeg" + str(patient_id) + ".edf"
        )
        neonatal_summary["patients"][str(patient_id)]["seizure_count"] = seizure_count[
            patient_id
        ]
        neonatal_summary["patients"][str(patient_id)][
            "total_ictal_seconds"
        ] = total_ictal[str(patient_id)]

    for patient_id, value in seizure_count.items():
        neonatal_summary["patients"][str(patient_id)]["seizures"] = {
            str(i + 1): {
                "start": int(seizure_starts_dict[str(patient_id)][i]),
                "end": int(seizure_ends_dict[str(patient_id)][i]),
            }
            for i in range(value)
        }

    return neonatal_summary
