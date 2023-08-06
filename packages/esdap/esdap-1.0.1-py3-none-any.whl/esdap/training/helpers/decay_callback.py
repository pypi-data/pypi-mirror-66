import math

from tensorflow.keras.callbacks import LearningRateScheduler


def step_decay_schedule(initial_lrate=0.1, decay_factor=0.5, decay_step_size=1):
    """Wrapper function to create a LearningRateScheduler with step decay
    schedule.

    Parameters
    ----------
    initial_lrate: float
        Initial learning rate

    decay_factor: float
        Decay factor in the step decay

    decay_step_size: int
        Amount of steps after which to apply the decay step

    Returns
    -------
    LearningRateScheduler: tf.keras.callbacks
        Learning rate scheduler
    """

    def schedule(epoch):
        lrate = initial_lrate * math.pow(
            decay_factor, math.floor((1 + epoch) / decay_step_size)
        )
        print("LR:", lrate)
        return lrate

    return LearningRateScheduler(schedule)
