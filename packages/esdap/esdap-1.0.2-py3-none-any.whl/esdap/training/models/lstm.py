import numpy as np
import tensorflow as tf

from .utils import add_activation_layer, get_initializers


def LSTM(
    X_train,
    y_train,
    activation,
    out_activation,
    num_layers=3,
    num_units=128,
    activation_param=0.3,
    dropout=True,
    dropout_value=0.1,
    batch_norm=True,
):

    """Build a LSTM Neural Network according to the given parameters.

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
        model.add(tf.keras.layers.LSTM(num_units, return_sequences=True))

        # Activation Function
        add_activation_layer(model, activation, activation_param)

        # Dropout Layer
        if dropout:
            model.add(tf.keras.layers.Dropout(dropout_value))

        # Batch Normalization Layer
        if batch_norm:
            model.add(tf.keras.layers.BatchNormalization())

    # Output Layer
    model.add(
        tf.keras.layers.LSTM(
            units=y_train.shape[1],
            activation=out_activation,
            kernel_initializer=kernel_initializer,
            bias_initializer=bias_initializer,
        )
    )

    return model
