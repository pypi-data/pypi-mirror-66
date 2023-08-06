# -*- coding: utf-8 -*-
# This file is part of the ESDaP package.
"""Calculate features from EEG measurements."""

# TODO: remove hardcoding where it is marked as such

import argparse
import datetime
import json
import sys
from os import path
from pathlib import Path

import mne
import numpy as np
import scipy
import scipy.signal
import scipy.stats
from joblib import Parallel, delayed

from esdap import helpers
from esdap.processing import compute_features as cf


class Config:
    """Configuration class set-up."""

    def __init__(self, args):
        """Set-up parameters.

        Assigns parameters from the command line variables such as the data path,
        which features to compute, which channels to take into account, which
        frequencies to sample.

        Parameters
        ----------
        args : :obj:`list` of :obj:`str`
            Command line arguments passed through `argparse`
        """
        self.summary = None

        self.data_path = args.data_path
        self.tiling = args.tiling
        self.stride = args.stride

        self.output_dir = args.output_dir

        self.features_name = args.features_name
        self.segment_length = args.segment_length  # in seconds

        self.preictal_duration = int(args.preictal_duration)  # in minutes
        self.postictal_duration = int(args.postictal_duration)  # in minutes

        self.assessor = args.assessor
        self.neonate_id = args.neonate_id
        if args.unipolar:
            self.unipolar = True
            self.bipolar = False
            self.which_polar_data = "unipolar"
        elif args.bipolar:
            self.unipolar = False
            self.bipolar = True
            self.which_polar_data = "bipolar"
        else:
            raise ValueError(
                "Input to the Config class is invalid"
                " Need to know whether to use unipolar or bipolar data"
            )

        # data parameters
        self.freqs = (
            (0.1, 4),
            (4, 7),
            (7, 13),
            (13, 15),
            (14, 30),
            (30, 45),
            (65, 120),
        )
        self.freqs_numpy = np.array(self.freqs)

        self.channels_names_unipolar = [
            "EEG FP1-REF",
            "EEG FP2-REF",
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
        self.channels_names_bipolar = [
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

        if self.unipolar:
            n_channels = len(self.channels_names_unipolar)
        elif self.bipolar:
            n_channels = len(self.channels_names_bipolar)
        else:
            raise ValueError("Really shouldn't get here!")

        self.n_channels = n_channels
        self.features_len = {}
        self.features_len["max_correlation"] = int(n_channels * (n_channels - 1) / 2.0)
        # self.features_len["nonlinear_interdependence"] = int(
        #     self.n_channels * (self.n_channels - 1) / 2.0
        # )
        # self.features_len["DSTL"] = int(self.n_channels * (self.n_channels - 1) / 2.)
        self.features_len["SPLV"] = int(
            n_channels * (n_channels - 1) / 2.0 * len(self.freqs)
        )
        self.features_len["moments"] = int(n_channels * 5)
        self.features_len["peak_to_peak"] = int(n_channels * 1)
        self.features_len["absolute_area"] = int(n_channels * 1)
        self.features_len["psd_ratio"] = int(n_channels * 8)
        self.features_len["decorrelation_time"] = int(n_channels * 1)
        self.features_len["dwt_coeffs"] = int(n_channels * 8)

        self.n_features = 0
        for key in self.features_name:
            self.n_features += self.features_len[key]


class EEGData:
    """Filter EEG data, segment signals and get features."""

    def __init__(self, raw_edf, eeg_start, seizures_start, seizures_end, cfg):
        """Set-up the data and filter the signals.

        Parameters
        ----------
        raw_edf : obj
            MNE RawEDF instance
        eeg_start : int
            Start time in seconds of the EEG recording file
        seizures_start : list
            List of seizure start times
        seizures_end : list
            List of seizure end times
        cfg : :obj:
            Configuration from the Config class
        """

        self.cfg = cfg

        self.measurements_per_segment = (
            cfg.summary["sampling_rate"] * cfg.segment_length
        )

        self.tiling = None
        if cfg.tiling is not None:
            self.tiling = cfg.summary["sampling_rate"] * cfg.tiling

        self.stride = None
        if cfg.stride is not None:
            self.stride = cfg.summary["sampling_rate"] * cfg.stride

        self.raw_edf = raw_edf
        self.eeg_start = eeg_start
        self.seizures_start = seizures_start
        self.seizures_end = seizures_end
        self.raw_edf._data = self.filter_power(self.raw_edf)
        self.raw_edf._data = self.filter_low_high(self.raw_edf)
        self.segments_idx = helpers.get_segment_start_indexes(
            n_measurements=self.raw_edf.n_times,
            window_length=self.measurements_per_segment,
            stride=self.stride,
            tiling=self.tiling,
        )

    def get_feature(self, feature_name, segment_index, timestamp):
        """Get the feature for a certain segment.

        Parameters
        ----------
        feature_name : str
            Which feature to calculate
        segment_index : int
            Starting point of the data to include
        timestamp : float
            Time of the sample from the start of the file

        Returns
        -------
        feature : np.ndarray
            A numpy array for the computed segment
        """
        segment = self.raw_edf.get_data(
            start=segment_index, stop=segment_index + self.measurements_per_segment
        )
        if (
            np.argwhere(self.segments_idx == segment_index)[0][0]
            % int(self.segments_idx.size / 10)
            == 0
        ):
            print(
                datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S"),
                f"feature_name: {feature_name}",
                f"segment_index: {segment_index:>12} ",
                f"timestamp: {int(timestamp):>8d}",
                f"progress: {int(100*segment_index/self.segments_idx[-1]):3d}%",
            )
        if feature_name == "max_correlation":
            feature = cf.get_max_correlation(segment)
        # elif feature_name == "nonlinear_interdependence":
        #     feature = self.nonlinear_interdependence(segment)
        # elif (feature_name == "DSTL"):
        # 	feature = self.get_dstl(segment)
        elif feature_name == "SPLV":
            feature = cf.get_splv(
                segment, self.cfg.freqs, self.cfg.summary["sampling_rate"]
            )
        elif feature_name == "moments":
            feature = self.get_univariate_feature(segment, feature_name)
        elif feature_name == "peak_to_peak":
            feature = self.get_univariate_feature(segment, feature_name)
        elif feature_name == "absolute_area":
            feature = self.get_univariate_feature(segment, feature_name)
        elif feature_name == "psd_ratio":
            feature = cf.power_spectral_density(
                self.raw_edf, timestamp, self.cfg.segment_length, self.cfg.freqs_numpy,
            )  # 8xN
            feature = feature.ravel()
        elif feature_name == "decorrelation_time":
            feature = self.get_univariate_feature(segment, feature_name)
        elif feature_name == "dwt_coeffs":
            feature = self.get_univariate_feature(segment, feature_name)
        else:
            raise ValueError(
                (
                    f"ERROR in cfg.features_name: Unknown feature name {self.cfg.features_name}."
                    " Options are:\n"
                    "moments peak_to_peak absolute_area psd_ratio decorrelation_time dwt_coeffs "
                    "max_correlation nonlinear_interdependence"
                )
            )
        return feature

    def get_required_features_single_core(self, feature_name):
        """Computes the features corresponding to `feature_name`

        Parameters
        ----------
        feature_name : str
            Which feature to calculate

        Returns
        -------
        features : np.ndarray
            A numpy array where each row is a segment. It has a realtime timestamp
            and the other columns are the computed result for `feature_name`
        """
        n_segments = len(self.segments_idx)
        features = np.zeros(
            (n_segments, (self.cfg.features_len[feature_name] + 1))
        )  # +1 for the timestamps column

        timestamps = self.segments_idx / self.cfg.summary["sampling_rate"]

        output_timestamps = timestamps + self.eeg_start

        features[:, 0] = output_timestamps
        for i in range(n_segments):
            features[i, 1 : self.cfg.features_len[feature_name] + 1] = self.get_feature(
                feature_name, self.segments_idx[i], timestamps[i]
            )
        return features

    def get_univariate_feature(self, signal, feature_name):
        """Computes one of various univariate features from a signal.

        The description of the features can be found in:
        Tsiouris, et al. "A Long Short-Term Memory deep learning network for the prediction
        of epileptic seizures using EEG signals."
        Computers in biology and medicine 99 (2018): 24-37.

        Parameters
        ----------
        signal : numpy.ndarray, shape (n_channels, n_times)
            EEG data to compute feature with
        feature_name : str
            Which feature to calculate

        Returns
        -------
        flatarray : np.ndarray
            A flattened numpy array which is the computed result for
            `feature_name` for that `signal`
        """
        if feature_name == "moments":
            features = cf.compute_moments(signal)  # 5xN
        elif feature_name == "peak_to_peak":
            features = cf.get_peak_to_peak(signal)  # 1xN
        elif feature_name == "absolute_area":
            features = cf.compute_absolute_area(signal, self.cfg.segment_length)  # 1xN
        elif feature_name == "decorrelation_time":
            features = cf.get_decorrelation_time(
                signal, self.cfg.summary["sampling_rate"]
            )  # 1xN
        elif feature_name == "dwt_coeffs":
            features = cf.discrete_wavelet_transform(signal)  # 8xN
        else:
            raise ValueError("ERROR in get_univariate_feature: Unknown feature_name")
        return features.ravel()

    def filter_low_high(self, signals):
        """Filter frequencies.

        Notes
        -----
        We only remove frequencies above 120Hz, but we could remove low frequence
        up to 0.5Hz, but it seems to add a lot of error to the signal

        Parameters
        ----------
        signals : obj
            Signals in an MNE RawEDF instance

        Returns
        -------
        filtered_signals : np.ndarray
            The filtered signals
        """
        low_freq = 120 * 2 / self.cfg.summary["sampling_rate"]
        b_low, a_low = scipy.signal.butter(1, low_freq, btype="lowpass")
        filtered_signals = scipy.signal.filtfilt(b_low, a_low, signals._data)
        return filtered_signals

    def filter_power(self, signals):
        """Remove the power line frequencies between 59 and 61 Hz.

        Parameters
        ----------
        signals : obj
            Signals in an MNE RawEDF instance

        Returns
        -------
        filtered_signals : np.ndarray
            The filtered signals
        """
        freqs = np.array([59, 61]) * 2 / self.cfg.summary["sampling_rate"]
        order = 5  # hardcoded
        return scipy.signal.filtfilt(
            *scipy.signal.butter(order, freqs, btype="bandstop"), signals._data
        )


class PatientData:
    """Class to load all the files related to a patient.

    Takes as input the configuration and as output write all the
    calculated features to files, along with the labels, timings,
    attributes and a log file
    """

    def __init__(self, cfg):
        """Loads the configuration and fills in the EEG data.

        Parameters
        ----------
        cfg : :obj:
            Configuration object
        """
        self.cfg = cfg

        summary_filename = path.join(
            self.cfg.data_path, "annotations_2017_" + self.cfg.assessor + ".csv"
        )
        self.cfg.summary = helpers.parse_neonatal_annotations(
            summary_filename, self.cfg.which_polar_data
        )

        self.seizures_time = []
        self.current_time = 0
        self.current_day = 0

        self.eeg_data = {}
        self.load_files()  # fills in self.eeg_data

    def save_required_segments(self, feature_name):
        """Calculate all features and labels and save everything to files.

        Parameters
        ----------
        feature_name : str
            REQUIRED: which feature to calculate

        Returns
        -------
        Nothing, as we write to files
        """

        segmenting_dir = f"{self.cfg.segment_length}-{self.cfg.stride}"

        out_dir = path.join(
            self.cfg.output_dir,
            self.cfg.which_polar_data,
            segmenting_dir,
            self.cfg.assessor,
            str(self.cfg.summary["patients"][self.cfg.neonate_id]["id"]),
        )
        # Ensure output dir exists
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        feature_file = path.join(out_dir, f"{feature_name}.dat")
        abs_seizure_times_file = path.join(out_dir, "seizure_times.json")

        labels_file = path.join(
            out_dir,
            f"labels-pre{self.cfg.preictal_duration}-post{self.cfg.postictal_duration}.dat",
        )
        timing_file = path.join(out_dir, "timing.dat")
        logging_file = path.join(out_dir, f"eadap.{path.basename(__file__)}.log")
        feature_file_conf = feature_file + ".conf.json"

        with open(feature_file, "w") as file:
            column_names = helpers.get_header_for_feature(
                feature_name, self.cfg.n_channels
            )
            file.write(" ".join(column_names) + "\n")

            def get_features_labels(
                eeg_data, cfg, feature_name, i, key, seizures_time, nr_files
            ):
                print(f"Processing file {i}/{nr_files}: {key}")
                segments = eeg_data.get_required_features_single_core(feature_name)
                # Calculate all the labels for these segments
                binary_label_cols = helpers.calculate_binary_labels(
                    segments[:, 0],
                    cfg.segment_length,
                    seizures_time,
                    cfg.preictal_duration,
                    cfg.postictal_duration,
                )

                # Join the features to the labels
                return np.concatenate((segments, binary_label_cols), axis=1)
                # return 1

            with Parallel(n_jobs=-1) as par:
                results = par(
                    delayed(get_features_labels)(
                        self.eeg_data[key],
                        self.cfg,
                        feature_name,
                        i,
                        key,
                        self.seizures_time,
                        len(self.eeg_data),
                    )
                    for i, key in enumerate(self.eeg_data, 1)
                )

            np.savetxt(file, np.concatenate(results, axis=0)[:, :-4], delimiter=" ")

        with open(labels_file, mode="w") as file:
            file.write(
                " ".join(["ictal", "preictal", "postictal", "interictal"]) + "\n"
            )
            np.savetxt(file, np.concatenate(results, axis=0)[:, -4:])

        with open(timing_file, mode="w") as file:
            file.write(
                " ".join(
                    [
                        "timestamp",
                        "time_until_next_seizure_starts",
                        "time_since_last_seizure_ended",
                    ]
                )
                + "\n"
            )
            # Calculate these times using all timepoints and seizure starts and ends
            (tunss, tslse) = helpers.get_times_until_and_since_seizures(
                np.concatenate(results, axis=0)[:, 0], self.seizures_time,
            )
            np.savetxt(
                file,
                np.stack((np.concatenate(results, axis=0)[:, 0], tunss, tslse), axis=1),
            )

        # Workaround for JSON to serialize numpy integers using json.dump's default argument.
        # From https://bugs.python.org/msg244359
        def convert(o):
            if isinstance(o, np.int64):
                return int(o)
            raise TypeError

        with open(feature_file_conf, mode="w") as file:
            json.dump(
                {
                    key: getattr(self.cfg, key)
                    for key in [
                        "summary",
                        "data_path",
                        "tiling",
                        "stride",
                        "output_dir",
                        "features_name",
                        "segment_length",
                        "preictal_duration",
                        "postictal_duration",
                        "freqs",
                        "channels_names_unipolar",
                        "channels_names_bipolar",
                        "n_channels",
                        "features_len",
                        "n_features",
                    ]
                },
                file,
                default=convert,
            )

        with open(logging_file, "a") as file:
            file.write(datetime.datetime.now().isoformat(sep=" ") + ": ")
            json.dump(
                {
                    "sys.exec_prefix": sys.exec_prefix,
                    "sys.executable": sys.executable,
                    "sys.argv": sys.argv,
                    # "git_hash": ,
                    # "esdap.version": esdap.__version__,
                    "database": self.cfg.data_path,
                },
                file,
            )
            file.write("\n")

        with open(abs_seizure_times_file, "w") as file:
            json.dump(self.seizures_time, file)

        print(f"Files saved in: {out_dir}")

    def load_files(self):
        filename = self.cfg.summary["patients"][self.cfg.neonate_id]["eeg_file_name"]
        print("Loading: " + filename)
        self.eeg_data[filename] = self.load_data(filename)
        print("Loaded: " + filename)

    def load_data(self, filename):
        """Load the data from `filename`

        Parameters
        ----------
        filename : str
            REQUIRED: which filename to load

        Returns
        -------
        EEGData : obj
            An object of the EEGData class containing the EEG signal

        Raises
        ------
        ValueError
            If there is a problem picking the channels
        """
        eeg_start_time_of_day = helpers.parse_gt_24_hours_time(
            self.cfg.summary["patients"][self.cfg.neonate_id]["eeg_start_time"],
            time_of_day=True,
        ).seconds

        # The following logic works because measurements never last more than 24 hours.
        if eeg_start_time_of_day < self.current_time:
            self.current_day = self.current_day + 1

        self.current_time = eeg_start_time_of_day
        eeg_start = datetime.timedelta(
            days=self.current_day, seconds=eeg_start_time_of_day
        ).total_seconds()

        # n_seizures = int(self.summary["edf_files"][filename]["seizure_count"])

        seizures_start = []
        seizures_end = []

        seizures = self.cfg.summary["patients"][self.cfg.neonate_id]["seizures"]
        for seizure in seizures:
            start = seizures[seizure]["start"] + eeg_start
            end = seizures[seizure]["end"] + eeg_start
            seizures_start.append(start)
            seizures_end.append(end)

            self.seizures_time.append((start, end))

        filename = path.join(self.cfg.data_path, filename)

        raw_edf = mne.io.read_raw_edf(filename, preload=True, stim_channel=None)
        # Some files' channels have -REF, some -Ref, so use the same
        mne.rename_channels(raw_edf.info, str.upper)

        # Test if bipolar data is requested
        if self.cfg.bipolar:
            raw_edf = self.get_bipolar_values(raw_edf)
        elif self.cfg.unipolar:
            raw_edf.pick_channels(self.cfg.channels_names_unipolar)
            if len(raw_edf[:, 1][0]) != len(self.cfg.channels_names_unipolar):
                print("-------------------------------")
                raise ValueError(
                    f"ERROR after loading edf data."
                    " Number of channels picked in edf data: {len(raw_edf[:, 1][0])} !="
                    " number of channels requested {len(self.cfg.channels_names)}"
                )
        else:
            raise ValueError("Shouldn't get here. Error picking channels.")
        print("Number of channels:", len(raw_edf[:, 1][0]))
        print("Using channels: ", raw_edf.ch_names)
        # return the EEG signal
        return EEGData(raw_edf, eeg_start, seizures_start, seizures_end, self.cfg)

    @staticmethod
    def get_bipolar_values(raw_edf):
        """Transform the unipolar data into bipolar values.

        Transform the unipolar data into our standard bipolar representation
        by subtracting the relevant channels.

        Parameters
        ----------
        raw_edf : obj
            An MNE RawEDF instance

        Returns
        -------
        bipolar_values : obj
            An MNE RawEDF instance with the unipolar channel signals replaced
            with signals from bipolar channels

        Notes
        -----
        The raw data is overwritten by the new data through adding the new
        bipolar channels to the MNE object, and then only selecting the
        bipolar channels. This is done in case any relevant information was
        left in the original object and we don't want to replace it with a
        whole new MNE RawArray.
        """

        # Note the new names mapping (from Wikipedia): T3->T7;T4->T8;T5->P7;T6->P8
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
        new_bip_data = np.zeros((len(bipolar_channels), raw_edf.n_times))

        new_bip_data[0] = raw_edf.get_data(["EEG FP1-REF"]) - raw_edf.get_data(
            ["EEG F7-REF"]
        )
        new_bip_data[1] = raw_edf.get_data(["EEG F7-REF"]) - raw_edf.get_data(
            ["EEG T3-REF"]
        )
        new_bip_data[2] = raw_edf.get_data(["EEG T3-REF"]) - raw_edf.get_data(
            ["EEG T5-REF"]
        )
        new_bip_data[3] = raw_edf.get_data(["EEG T5-REF"]) - raw_edf.get_data(
            ["EEG O1-REF"]
        )
        new_bip_data[4] = raw_edf.get_data(["EEG FP1-REF"]) - raw_edf.get_data(
            ["EEG F3-REF"]
        )
        new_bip_data[5] = raw_edf.get_data(["EEG F3-REF"]) - raw_edf.get_data(
            ["EEG C3-REF"]
        )
        new_bip_data[6] = raw_edf.get_data(["EEG C3-REF"]) - raw_edf.get_data(
            ["EEG P3-REF"]
        )
        new_bip_data[7] = raw_edf.get_data(["EEG P3-REF"]) - raw_edf.get_data(
            ["EEG O1-REF"]
        )
        new_bip_data[8] = raw_edf.get_data(["EEG FP2-REF"]) - raw_edf.get_data(
            ["EEG F4-REF"]
        )
        new_bip_data[9] = raw_edf.get_data(["EEG F4-REF"]) - raw_edf.get_data(
            ["EEG C4-REF"]
        )
        new_bip_data[10] = raw_edf.get_data(["EEG C4-REF"]) - raw_edf.get_data(
            ["EEG P4-REF"]
        )
        new_bip_data[11] = raw_edf.get_data(["EEG P4-REF"]) - raw_edf.get_data(
            ["EEG O2-REF"]
        )
        new_bip_data[12] = raw_edf.get_data(["EEG FP2-REF"]) - raw_edf.get_data(
            ["EEG F8-REF"]
        )
        new_bip_data[13] = raw_edf.get_data(["EEG F8-REF"]) - raw_edf.get_data(
            ["EEG T4-REF"]
        )
        new_bip_data[14] = raw_edf.get_data(["EEG T4-REF"]) - raw_edf.get_data(
            ["EEG T6-REF"]
        )
        new_bip_data[15] = raw_edf.get_data(["EEG T6-REF"]) - raw_edf.get_data(
            ["EEG O2-REF"]
        )
        new_bip_data[16] = raw_edf.get_data(["EEG FZ-REF"]) - raw_edf.get_data(
            ["EEG CZ-REF"]
        )
        new_bip_data[17] = raw_edf.get_data(["EEG CZ-REF"]) - raw_edf.get_data(
            ["EEG PZ-REF"]
        )

        sampling_rate = raw_edf.info["sfreq"]

        new_bip_info = mne.create_info(bipolar_channels, sampling_rate, ch_types="eeg")

        new_bip_raw = mne.io.RawArray(new_bip_data, new_bip_info)

        raw_edf.add_channels([new_bip_raw])

        raw_edf.pick_channels(bipolar_channels)

        return raw_edf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path", help="Path to load feature files (.dat)", required=True
    )
    parser.add_argument(
        "--output_dir", help="Path to store the computed features", required=True
    )
    parser.add_argument(
        "--segment_length",
        help="Duration of segments (in seconds)",
        required=True,
        type=int,
    )
    parser.add_argument(
        "--stride",
        help="Stride for signal segmentation (in seconds)",
        required=False,
        type=int,
    )
    parser.add_argument(
        "--tiling",
        help="Tiling for signal segmentation (in seconds)",
        required=False,
        type=int,
    )
    parser.add_argument(
        "--preictal_duration",
        help="Preictal duration in minutes",
        required=True,
        type=int,
    )
    parser.add_argument(
        "--postictal_duration",
        help="Postictal duration in minutes",
        required=True,
        type=int,
    )
    parser.add_argument(
        "--features_name",
        nargs="+",
        choices=[
            "moments",
            "peak_to_peak",
            "absolute_area",
            "psd_ratio",
            "decorrelation_time",
            "dwt_coeffs",
            "max_correlation",
            "SPLV",
            # "nonlinear_interdependence",
        ],
        help=("Select the features to prepare data."),
        required=True,
    )
    parser.add_argument(
        "--assessor",
        help="Which assessor to calculate labels for",
        required=True,
        type=str,
        choices=["A", "B", "C"],
    )
    parser.add_argument(
        "--neonate_id",
        help="Which neonatal patient is of interest",
        required=True,
        type=str,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--unipolar",
        action="store_true",
        help="Calculate features using unipolar channels",
    )
    group.add_argument(
        "--bipolar",
        action="store_true",
        help="Calculate features using bipolar channels",
    )
    args = parser.parse_args()

    cfg = Config(args)

    patient_data = PatientData(cfg)

    for feature_name in args.features_name:
        patient_data.save_required_segments(feature_name)

    print("Finished extracting features.")
    sys.exit(0)


if __name__ == "__main__":
    main()
