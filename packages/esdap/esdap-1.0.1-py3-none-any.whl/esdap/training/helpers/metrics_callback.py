from mlflow import log_metric, log_metrics
from tensorflow.keras.backend import eval
from tensorflow.keras.callbacks import Callback


class MetricsCallback(Callback):
    def on_epoch_begin(self, epoch, logs=None):
        log_metric("MO_learning_rate", eval(self.model.optimizer.lr))

        # print(eval(self.model.optimizer.lr))

    def on_epoch_end(self, epoch, logs=None):
        # if (epoch-1) % _LOG_EVERY_N_STEPS == 0:
        formatted_logs = dict()
        for k, v in logs.items():
            formatted_logs["MO_" + k] = logs[k]

        log_metrics(formatted_logs, step=epoch)
