"""Functions to calculate features."""

import mne
import numpy as np
import pywt
import scipy
from numba import njit


def filter_signal(signals, freqs, sampling_frequency):
    """Filter a signal.

    Parameters
    ----------
    signals: obj
        The EEG signal in RawEDF format. Possibly preprocessed.
    freqs : tuple of 2-tuples
        The frequencies defined in Config
    sampling_frequency : int
        Data sampling rate

    Returns
    -------
    numpy.ndarray
        Array of len(freq) signals, filtered by fir

    Notes
    -----
    The ntaps is defined as ~4 observations.
    The signals are filtered between frequencies defined in Config
    """
    filtered_signals = [None] * len(freqs)
    for i, freq in enumerate(freqs):
        avg_freq = np.average(freq)
        t_ms = 1000 / avg_freq
        ntaps = int(sampling_frequency * t_ms / 1000 * 4)
        # ~ ntaps = 1000
        fir = scipy.signal.firwin(
            ntaps,
            [freq[0], freq[1]],
            width=2,
            pass_zero=False,
            nyq=sampling_frequency / 2.0,
        )
        filtered_signals[i] = scipy.signal.convolve(
            signals, fir[np.newaxis, :], mode="valid"
        )
    return filtered_signals


def get_max_correlation(signal):
    """Computes the maximum of correlations between the channels of a signal.

    Parameters
    ----------
    signal: obj
        The EEG signal in RawEDF format. Possibly preprocessed.

    Returns
    -------
    numpy.ndarray
        1-D correlation matrix
    """
    n_channels = signal.shape[0]
    corr_coeffs = np.empty(int(n_channels * (n_channels - 1) / 2))
    auto_corr_coeffs = get_auto_corr_coeffs(signal)
    idx = 0
    for channel_a in range(n_channels - 1):
        for channel_b in range(channel_a + 1, n_channels):
            corr_coeffs[idx] = channel_correlation(
                signal, auto_corr_coeffs, channel_a, channel_b
            )
            idx += 1
    return corr_coeffs


def get_auto_corr_coeffs(signal):
    n_channels = signal.shape[0]
    auto_corr_coeffs = np.zeros(n_channels)
    for channel in range(n_channels):
        auto_corr_coeffs[channel] = scipy.correlate(
            signal[channel], signal[channel], "valid"
        )
    return auto_corr_coeffs


def channel_correlation(signal, auto_corr_coeffs, channel_1, channel_2):
    signal_1 = signal[channel_1]
    signal_2 = signal[channel_2]
    corr_1 = auto_corr_coeffs[channel_1]
    corr_2 = auto_corr_coeffs[channel_2]
    corr = scipy.correlate(signal_1, signal_2, "full")
    max_corr = np.max(corr)
    max_corr = max_corr / np.sqrt(corr_1 * corr_2)
    return max_corr


def embed_signals(signal, dimensoin=10, lag=6):
    """Delay embedding of a signal.

    Parameters
    ----------
    signal:
        The EEG signal in RawEDF format. Possibly preprocessed.
    dimension : int
        The embedding dimension.
    lag : int
        Time delay of the embedding.

    Returns
    -------
    numpy.ndarray
        embedded signal
    """
    n_channels = len(signal.ch_names)
    len_signal = len(signal[0])
    embedded_signals = np.empty(
        [n_channels, len_signal - (dimensoin - 1) * lag, dimensoin]
    )
    for channel in range(n_channels):
        for i in range(len_signal - (dimensoin - 1) * lag):
            for j in range(dimensoin):
                idx = i - j * lag + (dimensoin - 1) * lag
                embedded_signals[channel, i, j] = signal[channel][idx]
    return embedded_signals


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle(x1, x2):
    """Computes the angle between two n-vectors.

    Parameters
    ----------
    x1 : array_like
        First argument.
    x2 : array_like
        Second argument.

    Returns
    -------
    numpy.float
        Absolute value of the angle.
    """
    x1_u = unit_vector(x1)
    x2_u = unit_vector(x2)
    return abs(np.arccos(np.clip(np.dot(x1_u, x2_u), -1.0, 1.0)))


def get_splv(signals, freqs, sampling_frequency):
    """Computes phase-locking synchrony between all channels.

    Parameters
    ----------
    signals: obj
        The EEG signal in RawEDF format. Possibly preprocessed.
    freqs : tuple of 2-tuples
        The frequencies defined in Config
    sampling_frequency : int
        Data sampling rate

    Returns
    -------
    splv : numpy.ndarray
        SPLV matrix

    Notes
    -----
    Note that we use hilbert transform rather than Gabor, as suggested in
    Mirowski, Piotr, et al. "Classification of patterns of EEG synchronization for seizure
    prediction." Clinical neurophysiology 120.11 (2009): 1927-1940.
    """
    n_channels = len(signals)
    filtered_signals = filter_signal(signals, freqs, sampling_frequency)
    hilbert_signals = get_hilbert_signals(filtered_signals)
    splv = np.empty(int(n_channels * (n_channels - 1) / 2) * len(hilbert_signals))
    idx = 0
    for i in range(len(hilbert_signals)):
        for channel_a in range(n_channels - 1):
            for channel_b in range(channel_a + 1, n_channels):
                splv[idx] = get_plv(hilbert_signals[i], channel_a, channel_b)
                idx += 1
    return splv


def get_plv(hilbert_signal, channel_a, channel_b):
    """Computes phase-locking synchrony between two channels.

    Parameters
    ----------
    hilbert_signal: obj
        Hilbert transform of a signal
    channel_a : int
        Which is the first channel to consider
    channel_b : int
        Which is the second channel to consider

    Returns
    -------
    plv : float
        PLV value
    """
    phase_a = np.unwrap(np.angle(hilbert_signal[channel_a, :]))
    phase_b = np.unwrap(np.angle(hilbert_signal[channel_b, :]))
    plv = np.exp(1j * (phase_a - phase_b))
    return np.absolute(np.sum(plv) / len(plv))


def get_hilbert_signals(filtered_signals):
    """Computes the Hilbert signals.

    Parameters
    ----------
    filtered_signals: numpy.ndarray
        Prefiltered signals

    Returns
    -------
    numpy.ndarray
        The Hilbert transformed signals
    """
    hilbert_signals = [None] * len(filtered_signals)
    for i in range(len(filtered_signals)):
        hilbert_signals[i] = np.empty(filtered_signals[i].shape)
        for channel in range(len(filtered_signals[i])):
            hilbert_signals[i][channel, :] = np.imag(
                scipy.signal.hilbert(filtered_signals[i][channel, :])
            )
    return hilbert_signals


def compute_moments(signal):
    """Computes statistical moments from a signal.

    Parameters
    ----------
    signal : numpy.ndarray
        EEG data to compute moments of

    Returns
    -------
    np.ndarray
        A 5xN numpy array which holds the signal's mean, variance, skewness,
        kurtosis and standard deviation.
    """
    mean = np.mean(signal, 1)
    variance = np.var(signal, 1)
    skewness = scipy.stats.skew(signal, 1)
    kurtosis = scipy.stats.kurtosis(signal, 1)
    return np.transpose(
        np.array([mean, variance, skewness, kurtosis, np.sqrt(variance)])
    )


@njit
def get_peak_to_peak(signal):
    """Computes difference between highest and lowest amplitude.

    Parameters
    ----------
    signal : numpy.ndarray
        EEG data to compute the feature for

    Returns
    -------
    np.ndarray
        A 1xN numpy array which holds the peak-to-peak values
    """
    n_channels = signal.shape[0]
    peak_to_peak = np.zeros((n_channels, 1))
    for channel in range(n_channels):
        signal_max = np.max(signal[channel])
        signal_min = np.min(signal[channel])
        peak_to_peak[channel] = signal_max - signal_min
    return peak_to_peak


@njit
def compute_absolute_area(signal, segment_length):
    """Computes absolute area under the signal.

    Parameters
    ----------
    signal : numpy.ndarray
        EEG data to compute the feature for
    segment_length : int
        Duration of segments (in seconds)

    Returns
    -------
    np.ndarray
        A 1xN numpy array which holds the areas
    """
    n_channels = signal.shape[0]
    absolute_areas = np.zeros((n_channels, 1))
    for channel in range(n_channels):
        absolute_areas[channel] = (
            np.sum(np.abs(signal[channel, :])) * segment_length / signal.shape[1]
        )
    return absolute_areas


def power_spectral_density(signal_rawedf, timestamp, segment_length, freqs):
    """Computes frequency domain power spectral density.

    Parameters
    ----------
    signal_rawedf : obj
        An MNE RawEDF instance
    timestamp : float
        Time of the sample from the start of the file
    segment_length : int
        Duration of segments (in seconds)
    freqs : np.ndarray
        The frequencies defined in Config as a numpy array

    Returns
    -------
    psd_ratio : np.ndarray
        A 8xN numpy array which in the first column holds the total EEG signal
        energy. The other columns have the energy ratios within the
        different bands specified in `freqs`.
    """
    n_channels = len(signal_rawedf.ch_names)
    freqs_lb = freqs[:, 0]
    freqs_ub = freqs[:, 1]
    psds, frequencies = mne.time_frequency.psd_multitaper(
        signal_rawedf,
        tmin=timestamp,
        tmax=timestamp + segment_length,
        fmin=freqs_lb[0],
        fmax=freqs_ub[-1],
        picks=np.arange(n_channels),
        verbose=False,
    )
    idx_lb = np.searchsorted(frequencies, freqs_lb)
    idx_ub = np.searchsorted(frequencies, freqs_ub)
    psd_channels = np.sum(psds, 1)

    psd_ratio = np.zeros((n_channels, len(idx_lb) + 1))

    # First total EEG energy
    for channel in range(n_channels):
        sum_freq = np.sum(psds[channel, :])
        psd_ratio[channel, 0] = sum_freq

    for channel in range(n_channels):
        for i in range(len(idx_lb)):
            sum_freq = np.sum(psds[channel, idx_lb[i] : idx_ub[i]])
            ratio = sum_freq / psd_channels[channel]
            psd_ratio[channel, i + 1] = ratio
    return psd_ratio


def get_decorrelation_time(signal, sampling_frequency):
    """Computes decorrelation time.

    Parameters
    ----------
    signal : numpy.ndarray
        EEG data to compute the feature for
    sampling_frequency : int
        Data sampling rate

    Returns
    -------
    np.ndarray
        A 1xN numpy array of decorrelation times
    """
    n_channels = signal.shape[0]
    decorrelation_time = np.zeros((n_channels, 1))
    for channel in range(n_channels):
        decorr_idx = 0
        corr = scipy.correlate(signal[channel], signal[channel], "full")
        corr = np.roll(corr, len(signal[channel]))
        for i in range(len(corr)):
            if corr[i] < 0:
                decorr_idx = i
                break
        decorrelation_time[channel] = decorr_idx / sampling_frequency
    return decorrelation_time


def discrete_wavelet_transform(signal):
    """Computes the discrete wavelet transform in the frequency domain.

    Parameters
    ----------
    signal : numpy.ndarray
        EEG data to compute the feature for

    Returns
    -------
    np.ndarray, shape (n_channels, 8)
        The first column is the approximation coefficients array followed by
        the 7-level decomposition coefficients
    """
    n_channels = signal.shape[0]
    level = 7
    coeffs = np.zeros((n_channels, level + 1))
    # returns list of arrays of different size -> cannot use numpy vectorization
    decomposition = pywt.wavedec(signal, "db4", mode="symmetric", level=level, axis=-1)

    for i in range(level + 1):
        coeffs[:, i] = decomposition[i][:, 0]

    return coeffs
