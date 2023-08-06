import tensorflow as tf
from tensorflow.keras.optimizers import SGD, Adam

from .helpers.metrics import F1Score, Precision, Recall
from .models.fcn import FCN
from .models.lstm import LSTM
from .models.cnn import CNN


def get_model(config, X_train, y_train, out_activation, activation="softplus"):

    print("--------------------------")
    print("Getting model")
    print()

    if config.classifier_name == "FCN":
        model = FCN(
            X_train,
            y_train,
            activation=activation,
            out_activation=out_activation,
            # num_layers=config.num_layers,
            # num_units=config.num_units,
            # dropout=config.dropout,
            # dropout_value=config.dropout_value,
            # batch_norm=config.batch_norm,
        )
    elif config.classifier_name == "LSTM":
        model = LSTM(
            X_train,
            y_train,
            activation=activation,
            out_activation=out_activation,
            # num_layers=config.num_layers,
            # num_units=config.num_units,
            # dropout=config.dropout,
            # dropout_value=config.dropout_value,
            # batch_norm=config.batch_norm,
        )
    elif config.classifier_name == "CNN":
        model = CNN(
            X_train,
            y_train,
            activation=activation,
            out_activation=out_activation,
            # num_layers=config.num_layers,
            # num_units=config.num_units,
            # kernel_size=kernel_size,
            # pooling=pooling,
            # pool_size=pool_size,
            # dropout=config.dropout,
            # dropout_value=config.dropout_value,
            # batch_norm=config.batch_norm,
        )
    else:
        # TODO Error handling
        print("Classifier name does not match no available classifier")
        model = None

    return model


def get_optimizer(config):
    """
    Returns the specified optimizer

    Parameters
    ----------
    optimizer: str
        Optimizer as string

    lr: float
        Optimizer's initial learning rate

    max_momentum: float
        Optimizer's initial momentum

    Returns
    -------
    opt: tf.keras.optimizers
        Tensorflow.keras optimizer

    """
    if config.optimizer == "Adam":
        opt = Adam(lr=config.lr)
    elif config.optimizer == "SGD":
        opt = SGD(lr=config.lr, momentum=config.max_momentum)
    #    elif optimizer == "RAdam":
    #        opt = tfa.optimizers.RectifiedAdam(learning_rate=lr)
    #    elif optimizer == "AdaMod":
    #        opt = AdaMod(learning_rate=lr)
    else:
        opt = None
    return opt


def build_model(config: dict, X_train, y_train):
    """
    Build a tensorflow (keras) model according to the configuration dictionary

    Parameters
    ----------
    config: dict
        Dictionary containing the all arguments used as configuration

    Returns
    -------
    model: sklearn model
        Model constructed according to configuration
    """

    print("--------------------------")
    print("Building model")
    print()

    if not config.random_seed:
        tf.random.set_seed(42)

    if y_train.shape[1] > 1:
        loss = "categorical_crossentropy"
        out_activation = "softmax"
        activation = "softplus"
    else:
        loss = "binary_crossentropy"
        out_activation = "sigmoid"
        activation = "softplus"

    model = get_model(config, X_train, y_train, out_activation, activation)

    # TODO: to add this back in: add optimizer argument in script
    # opt = get_optimizer(config)

    opt = SGD(lr=0.5e-3, momentum=0.9)

    print("--------------------------")
    print("Compiling model")
    print()

    metrics = [
        "accuracy",
        Precision(y_train.shape[1], average="macro"),
        Recall(y_train.shape[1], average="macro"),
        F1Score(y_train.shape[1], average="macro"),
    ]

    model.compile(optimizer=opt, loss=loss, metrics=metrics)

    # Storing model summary into a string list
    stringlist = []
    model.summary(print_fn=lambda x: stringlist.append(x))
    summary = "\n".join(stringlist)

    print("--------------------------")
    print(summary)

    return model, summary
