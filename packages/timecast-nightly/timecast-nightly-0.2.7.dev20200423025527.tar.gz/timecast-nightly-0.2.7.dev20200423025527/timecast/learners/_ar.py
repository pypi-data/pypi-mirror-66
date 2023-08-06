"""flax.nn.Module for an auto-regressive online learner.

Todo:
    * Implement offline `fit` class method for closed-form, out of core training
    * Implement strided history
    * Add link functions for GLM
    * Add checks on data and corresponding negative tests

References:
    * http://eeweb.poly.edu/iselesni/lecture_notes/least_squares/least_squares_SP.pdf
"""
from typing import Tuple
from typing import Union

import flax
import jax
import jax.numpy as jnp
import numpy as onp

from timecast.utils import historify


def _compute_kernel_bias(X: onp.ndarray, Y: onp.ndarray, fit_intercept=True, alpha: float = 0.0):
    """Compute linear regression parameters"""
    num_samples, num_features = X.shape

    if fit_intercept:
        if num_features >= num_samples:
            X -= X.mean(axis=0)
        X = jnp.hstack((jnp.ones((X.shape[0], 1)), X))

    reg = alpha * jnp.eye(X.shape[0 if num_features >= num_samples else 1])
    if fit_intercept:
        reg = jax.ops.index_update(reg, [0, 0], 0)

    if num_features >= num_samples:
        beta = X.T @ jnp.linalg.inv(X @ X.T + reg) @ Y
    else:
        beta = jnp.linalg.inv(X.T @ X + reg) @ X.T @ Y

    if fit_intercept:
        return beta[1:], beta[0]
    else:
        return beta, [0]


class AR(flax.nn.Module):
    """AR online learner"""

    def apply(
        self,
        x: onp.ndarray,
        history_len: int,
        output_features: Union[Tuple[int, ...], int] = 1,
        history: onp.ndarray = None,
    ):
        """
        Note:
            * We expect that `x` is one- or two-dimensional
            * We reshape `x` to ensure its first axis is time and its second
              axis is input_features

        Args:
            x (onp.ndarray): input data
            history_len (int): length of AR history length
            output_features (Union[Tuple[int, ...], int]): int or tuple
            describing output shape
            history (onp.ndarray, optional): Defaults to None. Optional
            initialization for history

        Returns:
            onp.ndarray: result
        """

        if x.ndim == 1:
            x = x.reshape(1, -1)

        if history is not None and history.shape == x.shape:
            x = history

        self.history = self.state(
            "history", shape=(history_len, x.shape[1]), initializer=flax.nn.initializers.zeros
        )

        if self.is_initializing() and history is not None:
            self.history.value = jnp.vstack((self.history.value, history))[history.shape[0] :]
        elif not self.is_initializing():
            self.history.value = jnp.vstack((self.history.value, x))[x.shape[0] :]

        y = flax.nn.DenseGeneral(
            inputs=self.history.value,
            features=output_features,
            axis=(0, 1),
            batch_dims=(),
            bias=True,
            dtype=jnp.float32,
            kernel_init=flax.nn.initializers.zeros,
            bias_init=flax.nn.initializers.zeros,
            precision=None,
            name="linear",
        )
        return y

    @classmethod
    def fit(
        cls,
        X: onp.ndarray,
        Y: onp.ndarray,
        history_len: int,
        alpha: float = 0.0,
        seed: int = 0,
        name: str = "ar",
        **kwargs
    ) -> flax.nn.Model:
        """Receives data as an iterable of tuples containing input time series,
        true time series

        Todo:
            * We assume input_dim is one-dimensional; we should flatten if not
            * We assume output_feature is 1, but this may not always be true

        Notes:
            * Use (1, history_len * input_dim) vectors as features (could
            consider other representations)
            * Given a time series of length N and a history of length H,
            construct N - H + 1 windows

        Args:
            X: input data
            Y: ground truth
            history_len: length of history to consider
            input_dim)
            alpha: for ridge regression
            seed: random seed for jax random
            name: name for the top-level module
            kwargs: Extra keyword arguments

        Returns:
            flax.nn.Model: initialized model
        """
        if not hasattr(X, "shape") or not hasattr(Y, "shape") or X.ndim == 0 or Y.ndim == 0:
            raise ValueError("Data must be ndarrays with at least 1 dimension")
        if X.shape[0] != Y.shape[0]:
            raise ValueError("Input and output data must have the same" "number of observations")

        # Get input/output dim
        input_dim = 1 if X.ndim == 1 else X.shape[1]
        output_dim = 1 if Y.ndim == 1 else Y.shape[1]

        # The total number of samples we will have
        num_histories = X.shape[0] - history_len + 1

        # Expand input time series X into histories, whic should result in a
        # (num_histories, history_len * input_dim)-shaped array
        history = historify(
            X, num_histories=num_histories, history_len=history_len, offset=0
        ).reshape(num_histories, -1)

        kernel, bias = _compute_kernel_bias(history, Y[-len(history) :], alpha=alpha)

        kernel = kernel.reshape(history_len, input_dim, 1)

        with flax.nn.stateful() as state:
            model_def = AR.partial(history_len=history_len, output_features=output_dim, name=name)
            _, params = model_def.init_by_shape(jax.random.PRNGKey(seed), [(1, input_dim)])
            model = flax.nn.Model(model_def, params)

        model.params["linear"]["kernel"] = kernel
        model.params["linear"]["bias"] = bias

        return model, state
