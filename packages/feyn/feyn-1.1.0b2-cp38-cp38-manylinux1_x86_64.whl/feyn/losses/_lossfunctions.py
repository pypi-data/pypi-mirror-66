"""A collection of loss functions."""
import numpy as np

def mean_absolute_error(y_true, y_pred):
    """Compute the mean absolute error regression loss.

    Arguments:
        y_true {array_like} -- Ground truth (correct) target values.
        y_pred {array_like} -- Estimated target values.

    Returns:
        [float] -- The loss.
    """
    return np.mean(np.abs(y_true - y_pred))

mean_absolute_error.c_derivative = "mean_absolute_error"

def mean_squared_error(y_true, y_pred):
    """Compute the mean squared error regression loss.

    Arguments:
        y_true {array_like} -- Ground truth (correct) target values.
        y_pred {array_like} -- Estimated target values.

    Returns:
        [float] -- The loss.
    """
    return np.mean(np.power((y_pred - y_true), 2))

mean_squared_error.c_derivative = "mean_squared_error"

def categorical_cross_entropy(y_true, y_pred):
    """Compute the crossentropy loss between the labels and predictions.

    Arguments:
        y_true {array_like} -- Ground truth (correct) target values.
        y_pred {array_like} -- Estimated target values.

    Returns:
        [float] -- The loss.
    """
    epsilon = 1e-7
    y_pred = np.clip(y_pred, epsilon, 1. - epsilon)
    N = y_pred.shape[0]
    y_true = y_true.astype(int)
    if (y_true>1).any() or (y_true<0).any():
        raise Exception("Categorical loss function requires boolean truth values")

    return (1/N) * np.sum(-y_true*np.log(y_pred) - (1-y_true)*np.log(1-y_pred))


categorical_cross_entropy.c_derivative = "categorical_cross_entropy"


def _get_loss_function(name_or_func):
    # The loss function was provided instead of the name.
    # Return the function itself, if it is among the
    # known loss functions.
    if type(name_or_func).__name__ == "function":
        name_or_func = name_or_func.__name__

    if (name_or_func == "mean_absolute_error"):
        return mean_absolute_error
    if (name_or_func == "mean_squared_error"):
        return mean_squared_error
    if (name_or_func == "categorical_cross_entropy"):
        return categorical_cross_entropy

    raise ValueError("Unknown loss provided")
