"""A collection of loss functions."""
from ._lossfunctions import categorical_cross_entropy, mean_absolute_error, mean_squared_error, _get_loss_function

__all__ = [
    "categorical_cross_entropy",
    "mean_absolute_error",
    "mean_squared_error",
]
