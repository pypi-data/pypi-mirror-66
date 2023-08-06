import argparse
from distutils.util import strtobool
from pathlib import Path
from tempfile import TemporaryDirectory

from mlflow import log_artifact, log_metrics, start_run

from .helpers.utils import (
    get_avg_metrics_sklearn,
    get_confusion_matrices,
    get_metrics,
    print_confusion_matrix,
)
from .preprocessing.data_preparation import get_dataset
from .preprocessing.preprocessing import get_KFold_splits, preprocess
from .sklearn_models import build_model


def main(config):

    with start_run(run_name="Run", nested=True):

        runs_metrics = []
        runs_conf_matrices = []

        n_buckets = 4
        pre_minutes = 100
        post_minutes = 20
        bucket_length_min = 20

        # 1. Getting dataset
        data_cuts, label_names = get_dataset(
            config,
            pre_minutes=pre_minutes,
            post_minutes=post_minutes,
            n_buckets=n_buckets,
            bucket_length_min=bucket_length_min,
        )

        for i, (train_index, test_index) in enumerate(
            get_KFold_splits(data_cuts, n_splits=config.n_splits), 1
        ):
            if i > config.n_splits:
                break

            with start_run(run_name="Split_" + str(i), nested=True):

                data_cuts_train = [data_cuts[index] for index in train_index]
                data_cuts_test = [data_cuts[index] for index in test_index]

                # 2. Preprocess Data
                X_train, X_test, y_train, y_test, sw_train, sw_test = preprocess(
                    data_cuts_train, data_cuts_test, config
                )

                # 3. Build Model
                model = build_model(config)

                print(X_train.shape, X_test.shape)

                # 4. Fit Model to Data
                model.fit(
                    X_train.reshape(X_train.shape[0], -1),
                    y_train,
                    sample_weight=sw_train,
                )

                # if label_names is not None and len(label_names) != y_train.shape[1]:
                label_names = None

                # 5. Evaluate/Test Model and Save Metrics
                metrics = get_metrics(
                    model, X_test.reshape(X_test.shape[0], -1), y_test, config.task
                )

                log_metrics(metrics)

                # if y_train.shape[1] > 1:
                (
                    conf_matrix_all,
                    conf_matrix_pred,
                    conf_matrix_true,
                ) = get_confusion_matrices(
                    model, X_test.reshape(X_test.shape[0], -1), y_test
                )

                with TemporaryDirectory() as tmpdir:
                    filename = str(Path(tmpdir) / "confusion_matrix_all.png")
                    log_artifact(
                        print_confusion_matrix(
                            conf_matrix_all, label_names, filename=filename
                        )
                    )

                    filename = str(Path(tmpdir) / "confusion_matrix_pred.png")
                    log_artifact(
                        print_confusion_matrix(
                            conf_matrix_pred, label_names, filename=filename
                        )
                    )

                    filename = str(Path(tmpdir) / "confusion_matrix_true.png")
                    log_artifact(
                        print_confusion_matrix(
                            conf_matrix_true, label_names, filename=filename
                        )
                    )

                # log_model(model, "sk_model")

                runs_metrics.append((None, metrics))

                # if y_train.shape[1] > 1:
                runs_conf_matrices.append(
                    (conf_matrix_all, conf_matrix_pred, conf_matrix_true)
                )

        avg_metrics = get_avg_metrics_sklearn(runs_metrics)
        log_metrics(avg_metrics)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Sklearn Classifier Training Script")

    parser.add_argument(
        "--data_path",
        type=str,
        default="data\\6-3",
        metavar="N",
        help="path to data directory (default: data)",
    )

    parser.add_argument(
        "--patient_name",
        type=str,
        default="chb06",
        metavar="N",
        help="name of patient folder (default: chb06)",
    )

    parser.add_argument(
        "--labels_filename",
        type=str,
        default="labels-pre30-post30",
        metavar="N",
        help="Labels filename (default: labels-pre30-post30)",
    )

    parser.add_argument(
        "--timings_filename",
        type=str,
        default="timing",
        metavar="N",
        help="Timings filename (default: timing)",
    )

    parser.add_argument(
        "--classifier_name",
        type=str,
        default="RandomForest",
        metavar="N",
        help="classifier to use for training (default: RandomForest)",
    )

    parser.add_argument(
        "--split_type",
        type=str,
        default="normal",
        metavar="N",
        help="Way of splitting (fixed amount of time or normal) (default: fixed)",
    )

    parser.add_argument(
        "--n_splits",
        type=int,
        default=1,
        metavar="N",
        help="Number of 3Fold train-test splits to consider (default: 1)",
    )

    parser.add_argument(
        "--sample_window_length",
        type=int,
        default=0,
        metavar="N",
        help="Window length for generating samples out of timesteps (default: 0)",
    )

    parser.add_argument(
        "--random_seed",
        type=lambda x: bool(strtobool(x)),
        default=False,
        metavar="N",
        help="Flag deciding whether to use or not a random seed in the model building (default: False)",
    )

    parser.add_argument(
        "--task",
        type=str,
        default="multiclass",
        metavar="N",
        help="task to work on (default: multiclass)",
    )

    parser.add_argument(
        "--one_hot",
        type=lambda x: bool(strtobool(x)),
        default=True,
        metavar="N",
        help="one hot encoding for the labels (default: True)",
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=30,
        metavar="N",
        help="training epochs (default: 30)",
    )

    parser.add_argument(
        "--ft_moments",
        type=lambda x: bool(strtobool(x)),
        default=False,
        metavar="N",
        help="Flag deciding whether to use or not the moments features class (default: True)",
    )

    parser.add_argument(
        "--ft_peak_to_peak",
        type=lambda x: bool(strtobool(x)),
        default=False,
        metavar="N",
        help="Flag deciding whether to use or not the peak_to_peak features class (default: True)",
    )

    parser.add_argument(
        "--ft_max_correlation",
        type=lambda x: bool(strtobool(x)),
        default=False,
        metavar="N",
        help="Flag deciding whether to use or not the max_correlation features class (default: True)",
    )

    parser.add_argument(
        "--ft_decorrelation_time",
        type=lambda x: bool(strtobool(x)),
        default=False,
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
        default=False,
        metavar="N",
        help="Flag deciding whether to use or not the dwt_coeffs features class (default: True)",
    )

    parser.add_argument(
        "--ft_psd_ratio",
        type=lambda x: bool(strtobool(x)),
        default=False,
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

    main(config)
