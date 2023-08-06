from tensorflow.keras.initializers import constant, glorot_normal, he_normal, zeros
from tensorflow.keras.layers import (
    ELU,
    Activation,
    AvgPool1D,
    LeakyReLU,
    MaxPool1D,
    PReLU,
    ReLU,
    Softmax,
    ThresholdedReLU,
)


def add_activation_layer(model, activation, activation_param):
    """Adds the specified activation layer to the given model.

    Parameters
    ----------
    model: tf.keras.model
        Tensorflow.keras model to which to add an activation layer

    activation: str
        Activation to add to the model

    activation_param: float
        Parameter related to the activation (when needed)
    """
    if activation == "relu":
        model.add(ReLU())
    elif activation == "leaky_relu":
        model.add(LeakyReLU(alpha=activation_param))
    elif activation == "prelu":
        model.add(PReLU())
    elif activation == "elu":
        model.add(ELU(alpha=activation_param))
    elif activation == "selu":
        model.add(Activation("selu"))
    elif activation == "thresholded_relu":
        model.add(ThresholdedReLU(theta=activation_param))
    elif activation == "softmax":
        model.add(Softmax())
    elif activation == "softplus":
        model.add(Activation("softplus"))
    #    elif activation == "rrelu":
    #        model.add(tfa.activations.rrelu())
    else:
        print(f"Selected activation function ({activation}) is not available!")


def add_pooling_layer(model, pooling, pool_size, pool_stride):
    """

    Parameters
    ----------
    model: tf.keras.model
        Tensorflow.keras model to which to add the specified pooling layer

    pooling: str
        Pooling layer to add to the specified model

    pool_size: int
        Pooling size in the pooling layer

    Returns
    -------

    """
    if pooling == "max_pooling":
        model.add(MaxPool1D(pool_size=pool_size, strides=pool_stride))
    elif pooling == "avg_pooling":
        model.add(AvgPool1D(pool_size=pool_size, strides=pool_stride))
    else:
        print("Selected pooling is not available!")


def get_initializers(activation):
    """Returns the kernel and bias initializers for the given activation
    function.

    Parameters
    ----------
    activation: str
        Activation function for a given layer

    Returns
    -------
        kernel_initializer: tf.keras.initializers
            Kernel initializer for the given activation function

        bias_initializer: tf.keras.initializers
            Bias initializer for the given activation function
    """
    if activation == "relu":
        kernel_initializer = he_normal()
        bias_initializer = constant(value=0.01)
    else:
        kernel_initializer = glorot_normal()
        bias_initializer = zeros()
    return kernel_initializer, bias_initializer
