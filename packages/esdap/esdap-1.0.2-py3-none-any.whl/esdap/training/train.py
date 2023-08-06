from argparse import Namespace

import tensorflow as tf
import tensorflow.keras as ks
import tensorflow.keras.layers as L
from focal_loss import BinaryFocalLoss
from sklearn.model_selection import KFold

from esdap.training.preprocessing.data_preparation import get_dataset
from esdap.training.preprocessing.preprocessing import preprocess

config = Namespace()
config.one_hot = "True"
config.task = "binary_prediction"
config.split_type = "fixed"
config.data_path = "data\\6-3"
config.patient_name = "chb06"
config.labels_filename = "labels-pre30-post30"
config.timings_filename = "timing"
config.sample_window_length = 10
config.ft_moments = "False"
config.ft_peak_to_peak = "False"
config.ft_max_correlation = "True"
config.ft_decorrelation_time = "False"
config.ft_absolute_area = "False"
config.ft_dwt_coeffs = "True"
config.ft_psd_ratio = "False"
config.ft_splv = "True"

data_cuts, _ = get_dataset(
    config, pre_minutes=120, post_minutes=30, n_buckets=6, bucket_length_min=10
)

kf = KFold(3, True)

train_index, test_index = next(kf.split(data_cuts))
data_cuts_train = [data_cuts[index] for index in train_index]
data_cuts_test = [data_cuts[index] for index in test_index]

X_train, X_test, y_train, y_test = preprocess(data_cuts_train, data_cuts_test, config)

# This could help with extremely unbalanced problems but does not play nice
# with tf.data.dataset

# training_generator, steps_per_epoch = balanced_batch_generator(
#     X_train,
#     y_train,
#     sampler=NearMiss(),
#     batch_size=64)


def focal_loss(gamma=2.0, alpha=4.0):

    gamma = float(gamma)
    alpha = float(alpha)

    def focal_loss_fixed(y_true, y_pred):
        """Focal loss for multi-classification
        FL(p_t)=-alpha(1-p_t)^{gamma}ln(p_t)
        Notice: y_pred is probability after softmax
        gradient is d(Fl)/d(p_t) not d(Fl)/d(x) as described in paper
        d(Fl)/d(p_t) * [p_t(1-p_t)] = d(Fl)/d(x)
        Focal Loss for Dense Object Detection
        https://arxiv.org/abs/1708.02002

        Arguments:
            y_true {tensor} -- ground truth labels, shape of [batch_size, num_cls]
            y_pred {tensor} -- model's output, shape of [batch_size, num_cls]

        Keyword Arguments:
            gamma {float} -- (default: {2.0})
            alpha {float} -- (default: {4.0})

        Returns:
            [tensor] -- loss.
        """

        epsilon = 1.0e-9
        y_true = tf.convert_to_tensor(y_true, tf.float32)
        y_pred = tf.convert_to_tensor(y_pred, tf.float32)

        model_out = tf.add(y_pred, epsilon)
        ce = tf.multiply(y_true, -tf.math.log(model_out))
        weight = tf.multiply(y_true, tf.pow(tf.subtract(1.0, model_out), gamma))
        fl = tf.multiply(alpha, tf.multiply(weight, ce))
        reduced_fl = tf.reduce_max(fl, axis=1)
        return tf.reduce_mean(reduced_fl)

    return focal_loss_fixed


train_data = tf.data.Dataset.from_tensor_slices((X_train, y_train))
train_data = train_data.shuffle(1000).batch(64)

test_data = tf.data.Dataset.from_tensor_slices((X_test, y_test))
test_data = test_data.batch(64)

model = ks.Sequential(
    [L.Flatten(), L.Dense(32, activation="relu"), L.Dense(1, activation="sigmoid")]
)

model.compile(
    # ks.optimizers.SGD(1e-3, momentum=0.9),
    ks.optimizers.Adam(0.5e-3),
    loss=BinaryFocalLoss(3),
    # loss=focal_loss(),
    # loss='categorical_crossentropy',
    metrics=["accuracy", ks.metrics.Precision(), ks.metrics.Recall()],
)

model.fit_generator(
    generator=train_data,
    # steps_per_epoch=steps_per_epoch,
    epochs=100,
    # validation_data=(X_test, y_test)
    validation_data=test_data,
)
