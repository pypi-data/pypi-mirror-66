"""flax.nn.Module for an auto-regressive online learner.

Todo:
    * Implement batching; right now, passing in a batch skips to the end and
    predicts one value, rather than predict one value per example or some sort
    of averaging
    * Implement strided history
    * Add link functions for GLM

References:
    * http://eeweb.poly.edu/iselesni/lecture_notes/least_squares/least_squares_SP.pdf
"""
from typing import Iterable
from typing import Tuple
from typing import Union

import flax
import jax
import jax.numpy as jnp
import numpy as onp

from timecast.utils import historify
from timecast.utils import internalize
from timecast.utils.gram import OnlineGram


def _compute_kernel_bias_gram(XTX: onp.ndarray, XTY: onp.ndarray, alpha: float = 0.0):
    """Compute linear regression parameters from gram matrix

    Notes:
        * Assumes fit_intercept=True
        * Assumes over-determined systems
    """
    reg = alpha * jnp.eye(XTX.shape[0])
    reg = jax.ops.index_update(reg, [0, 0], 0)
    beta = jnp.linalg.inv(XTX + reg) @ XTY

    return beta[1:], beta[0]


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
        output_dim: Union[Tuple[int, ...], int] = 1,
        history: onp.ndarray = None,
        loc: Union[onp.ndarray, float] = None,
        scale: Union[onp.ndarray, float] = None,
    ):
        """
        Note:
            * We expect that `x` is one- or two-dimensional
            * We reshape `x` to ensure its first axis is time and its second
              axis is input_features

        Args:
            x (onp.ndarray): input data
            history_len (int): length of AR history length
            output_dim (Union[Tuple[int, ...], int]): int or tuple
            describing output shape
            history (onp.ndarray, optional): Defaults to None. Optional
            initialization for history
            loc: mean for centering data
            scale: std for normalizing data

        Returns:
            onp.ndarray: result
        """

        if jnp.isscalar(x):
            x = [[x]]
        if x.ndim == 1:
            x = x.reshape(1, -1)

        self.history = self.state(
            "history", shape=(history_len, x.shape[1]), initializer=flax.nn.initializers.zeros
        )

        if self.is_initializing() and history is not None:
            self.history.value = jnp.vstack((self.history.value, history))[history.shape[0] :]
        elif not self.is_initializing():
            self.history.value = jnp.vstack((self.history.value, x))[x.shape[0] :]

        inputs = self.history.value.ravel().reshape(1, -1)

        if loc is not None:
            inputs -= loc

        if scale is not None:
            inputs /= scale

        y = flax.nn.DenseGeneral(
            inputs=inputs,
            features=output_dim,
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
        data: Iterable[Tuple[onp.ndarray, onp.ndarray]],
        input_dim: int,
        history_len: int,
        output_dim: int = 1,
        normalize: bool = True,
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
            * output_dim defaults to 1 and is ignored for now
            * Really intended for passing in timeseries at a time, not
            individual time series observations; is this the right general API?
            * Shape is (1, input_dim); what about mini-batches?

        Notes:
            * Use (1, history_len * input_dim) vectors as features (could
            consider other representations)
            * Given a time series of length N and a history of length H,
            construct N - H + 1 windows
            * We could infer input_dim from data, but for now, require
            users to explicitly provide
            * Assumes we get tuples of time series, not individual time series observations

        Args:
            data: an iterable of tuples containing input/truth pairs of time
            series
            input_dim: number of feature dimensions in input
            history_len: length of history to consider
            output_dim: number of feature dimensions in output
            normalize: zscore data or not
            alpha: for ridge regression
            seed: random seed for jax random
            name: name for the top-level module
            kwargs: Extra keyword arguments

        Returns:
            flax.nn.Model: initialized model
        """
        num_features = input_dim * history_len
        XTX = OnlineGram(num_features, normalize=normalize)
        XTY = OnlineGram(num_features, output_dim, normalize=normalize)

        for X, Y in data:
            X = internalize(X, input_dim)[0]
            Y = internalize(Y, output_dim)[0]

            if X.shape[0] != Y.shape[0]:
                raise ValueError(
                    "Input and output data must have the same" "number of observations"
                )

            # The total number of samples we will have
            num_histories = X.shape[0] - history_len + 1

            # Expand input time series X into histories, whic should result in a
            # (num_histories, history_len * input_dim)-shaped array
            history = historify(
                X, num_histories=num_histories, history_len=history_len, offset=0
            ).reshape(num_histories, -1)

            XTX.update(history)
            XTY.update(history, Y[-len(history) :])

        if XTX.observations > 0:
            kernel, bias = _compute_kernel_bias_gram(XTX.matrix, XTY.matrix, alpha=alpha)
            kernel = kernel.reshape(1, num_features, 1)

        loc = XTX.mean if (XTX.observations > 0 and normalize) else None
        scale = XTX.std if (XTX.observations > 0 and normalize) else None

        with flax.nn.stateful() as state:
            model_def = AR.partial(
                history_len=history_len, output_dim=output_dim, loc=loc, scale=scale, name=name
            )
            _, params = model_def.init_by_shape(jax.random.PRNGKey(seed), [(1, input_dim)])
            model = flax.nn.Model(model_def, params)

        if XTX.observations > 0:
            model.params["linear"]["kernel"] = kernel
            model.params["linear"]["bias"] = bias

        return model, state
