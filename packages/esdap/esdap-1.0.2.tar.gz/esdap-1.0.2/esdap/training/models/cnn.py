import tensorflow as tf

from .utils import add_activation_layer, add_pooling_layer, get_initializers


def CNN(
    X_train,
    y_train,
    activation,
    out_activation,
    num_layers=3,
    num_units=128,
    kernel_size=3,
    stride=1,
    padding="same",
    activation_param=0.3,
    pooling=None,
    pool_size=2,
    pool_stride=2,
    dropout=False,
    dropout_value=0,
    batch_norm=True,
):

    """Build a Fully Connected Neural Network according to the given
    parameters.

    Parameters
    ----------
    num_layers: int
        Number of hidden layers

    num_units: int
        Number of units per hidden layer

    activation: str
        Activation function for the hidden layers

    dropout: bool
        boolean indicating whether to add dropout layers after each dense layer

    dropout_value: float
        Dropout value for the dropout layers (if used)

    batch_norm: bool
        boolean indicating whether to add batch_normalization layers after each dense layer

    Returns
    -------
    model: tf.keras.models.Sequential
    """

    # print(X_train.shape[1:])

    model = tf.keras.models.Sequential()

    # Input Layer
    model.add(tf.keras.layers.Input(X_train.shape[1:]))

    # Get initializers
    kernel_initializer, bias_initializer = get_initializers(activation)

    # Hidden Layers
    for i in range(num_layers):
        model.add(
            tf.keras.layers.Conv1D(
                filters=num_units * pow(2, i),
                kernel_size=kernel_size,
                kernel_initializer=kernel_initializer,
                bias_initializer=bias_initializer,
                strides=stride,
                padding=padding,
            )
        )

        # Activation Function
        add_activation_layer(model, activation, activation_param)

        # Pooling Layer
        if pooling == "True":
            add_pooling_layer(model, pooling, pool_size, pool_stride)

        # Dropout Layer
        if dropout:
            model.add(tf.keras.layers.Dropout(dropout_value))

        # Batch Normalization Layer
        if batch_norm:
            model.add(tf.keras.layers.BatchNormalization())

    # Pre - Output Layer
    model.add(tf.keras.layers.Flatten())

    # Output Layer
    model.add(
        tf.keras.layers.Dense(
            units=y_train.shape[1],
            activation=out_activation,
            kernel_initializer=kernel_initializer,
            bias_initializer=bias_initializer,
        )
    )

    return model
