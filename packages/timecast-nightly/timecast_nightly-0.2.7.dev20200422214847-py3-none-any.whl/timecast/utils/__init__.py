"""Utility functions"""
from numbers import Real
from typing import Tuple
from typing import Union

import jax.numpy as jnp
import numpy as onp


def historify(X: onp.ndarray, num_histories: int, history_len: int, offset: int = 0):
    """Generate (num_histories, history_len, feature_dim) history from time series data

    Todo:
        * Implement striding

    Args:
        X: 2D array of features organized as (time, feature_dim)
        num_histories: number of history windows to create
        history_len: length of a history window
        offset: how many time steps to offset

    Returns:
        onp.ndarray: 3D array organized as (num_histories, history_len,
        feature_dim)
    """
    if num_histories < 1 or history_len < 1:
        raise ValueError("Must have positive history_len and at least one window")
    if X.shape[0] < offset + num_histories + history_len - 1:
        raise ValueError(
            "Not enough history ({}) to produce {} windows of length {} with offset {}".format(
                X.shape[0], num_histories, history_len, offset
            )
        )
    return jnp.swapaxes(
        jnp.stack([jnp.roll(X, shift=-(i + offset), axis=0) for i in range(history_len)]), 0, 1
    )[:num_histories]


def internalize(
    x: Union[onp.ndarray, jnp.ndarray, Real], input_dim: int
) -> Tuple[bool, jnp.ndarray, int]:
    """ Takes user input data and converts into a consistent internal form
    Args:
        x (Union[onp.ndarray, jnp.ndarray, Real]): some input data to be
        converted input_dim (int): The input dimension specified at
        instantiation
    Notes:
        * Inputs can be scalar, 0D, 1D, or 2D.
        * While internally, we may have >2D arrays, we consider that an error
        if coming from the user
        * Internal representation is 2D array where dimension 0 is time and
        dimension 1 is feature
        * Inputs can be single time series values (value) or a sequence of time
        series values (batch)
        * Scalar and 0D inputs are values if input_dim is 1
        * 1D input is a value if its length matches the input_dim
        * 1D input is a batch if input_dim is 1 (previous rule takes
        precedence)
        * 2D input is a value if dimension 0 is 1 and dimension 1 is input_dim
        * 2D input is a batch if dimension 1 equals input_dim
    Warning:
        * When x is 2D, dimensions are always (time, feature)
        * We don't check whether the NumPy array is well-formed or not (e.g.,
        single data type, np.product(x.shape) == np.len(x.ravel()))
    Returns:
        x (jnp.ndarray): internalized version of input
        is_value (bool): whether the input was a value or a batch
        dim (int): number of dimensions of original input. -1 means
        np.isscalar(x) is True
        was_jax (bool): whether or not the input array was a
        jax.numpy.DeviceArray
    Raises:
        TypeError: x is not NumPy array or real number, or has more than two
        dimensions
        ValueError: input x does not match input_dim
    """
    was_jax = isinstance(x, jnp.DeviceArray)
    is_scalar, x = jnp.isscalar(x), jnp.asarray(x)

    if len(x.shape) > 2:
        raise TypeError("Input cannot have more than two dimensions")

    # -1 if scalar, otherwise take original NumPy dimension
    dim = -1 if is_scalar else len(x.shape)

    # If Python or 0D NumPy array, x is a value
    if dim <= 0 and input_dim == 1:
        return jnp.asarray([[x]]), True, dim, was_jax

    # If 1D array and length is equal to input_dim, x is a value
    if dim == 1 and len(x.ravel()) == input_dim:
        return x.reshape(1, -1), True, dim, was_jax

    # If 1D array and input_dim is 1, x is a batch
    if dim == 1 and input_dim == 1:
        return x.reshape(-1, 1), False, dim, was_jax

    # If 2D array and dimension 1 is equal to input_dim, x is a batch
    if dim == 2 and x.shape[1] == input_dim:
        return x, x.shape[0] == 1, dim, was_jax

    raise ValueError("Input shape {} does not match input_dim {}".format(x.shape, input_dim))


def externalize(x: jnp.ndarray, dim: int, was_jax: bool = False) -> Union[onp.ndarray, jnp.ndarray]:
    """Takes internal representation of 2D (time, feature) and returns to user
    Args:
        x (Union[jnp.ndarray, Real]): some input data to be converted
        dim (int): The original number of dimensions (-1 for scalar, n for nD
        NumPy array)
        was_jax (bool): whether original array was jax.numpy.DeviceArray
    Warning:
        * Transformations may not always be from R^n to R^n, so we have to make
        some guesses
        * We don't check whether the NumPy array is well-formed or not (e.g.,
        single data type, jnp.product(x.shape) == jnp.len(x.ravel()))
    Notes:
        * We assume if the original input was less than 2, we should squeeze
        out as many dimensions as we can
        * We leave input as is if original dimension was 2
        * It's not clear when to use this, especially if users are not
        consistent with their inputs
    Returns:
        x (Union[onp.ndarray, jnp.ndarray]): externalized version of input
    Raises:
        TypeError: x is not a NumPy array with two dimensions
        ValueError: dim is not -1, 0, 1, or 2; input x does not match input_dim
        or dim
    """
    if was_jax:
        x = onp.asarray(x)
    else:
        x = jnp.asarray(x)

    if not isinstance(x, jnp.ndarray):
        raise TypeError("x has incorrect type {}".format(type(x)))
    if len(x.shape) != 2:
        raise TypeError("x does not have two dimensions")
    if dim < -1 or dim > 2:
        raise ValueError("Original dimension must be -1, 0, 1, or 2")

    # If the original dimension was 2, just return
    if dim == 2:
        return x

    # Need to be careful with x with one item
    if len(x.ravel()) == 1:

        # If the original was a scalar, return a scalar
        if dim == -1:
            return x.item()

        # If the original was 1D, return 1D
        if dim == 1:
            return x.ravel()

    # Otherwise, try to squeeze as many dimensions as we can
    if dim < 2:
        return x.squeeze()
