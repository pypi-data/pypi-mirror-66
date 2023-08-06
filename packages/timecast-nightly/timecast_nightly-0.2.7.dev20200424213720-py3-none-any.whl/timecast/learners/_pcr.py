"""flax.nn.Module for a principal component regression online learner."""
from typing import Iterable
from typing import Tuple
from typing import Union

import flax
import jax
import jax.numpy as jnp
import numpy as onp

from timecast.learners._ar import _compute_kernel_bias_gram
from timecast.learners.base import FitMixin
from timecast.utils import historify
from timecast.utils import internalize
from timecast.utils.gram import OnlineGram


def _compute_pca_projection(X: onp.ndarray, k: int, center=False) -> onp.ndarray:
    """Compute PCA projection"""

    if center:
        X = X - X.mean(axis=0)
        # X /= X.shape[0] - 1

    # Compute SVD
    # X: (steps - history_len + 1, history_len * input_dim) -> (H, d)
    # U: (H, H), but because full_matrices=False, (H, d)
    # S: (min(H, d),)
    # VT: (d, d)
    U, S, VT = jnp.linalg.svd(X, full_matrices=False, compute_uv=True)

    # Get index of top K eigen values
    top_k = (-jnp.square(S)).argsort()[:k]

    # Get projection
    # projection: (d, k)
    projection = VT[top_k].T

    return projection


class PCR(FitMixin, flax.nn.Module):
    """PCR online learner"""

    def apply(
        self,
        x: onp.ndarray,
        history_len: int,
        projection: onp.ndarray,
        output_dim: Union[Tuple[int, ...], int] = 1,
        history: onp.ndarray = None,
        loc: Union[onp.ndarray, float] = None,
        scale: Union[onp.ndarray, float] = None,
    ):
        """
        Todo:
            * AR doesn't take any history
        output_dim (Union[Tuple[int, ...], int]): int or tuple describing
        output shape

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

        inputs = self.history.value.reshape(1, -1) @ projection

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
        k: int = None,
        normalize: bool = True,
        alpha: float = 0.0,
        seed: int = 0,
        name: str = "pcr",
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
            * Ignore true value (i.e., look at features only) (should we
            consider impact of features on dependent variable?)
            * Given a time series of length N and a history of length H,
            construct N - H + 1 windows
            * We could infer input_dim from data, but for now, require
            users to explicitly provide
            * Assumes we get tuples of time series, not individual time series
            observations

        Args:
            data: an iterable of tuples containing input/truth pairs of time
            series
            input_dim: number of feature dimensions in input
            history_len: length of history to consider
            output_dim: number of feature dimensions in output
            k: number of PCA components to keep. Default is min(num_histories,
            normalize: zscore data or not
            input_dim)
            alpha: Parameter to pass to ridge regression for AR fit
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

        if XTX.observations == 0:
            raise IndexError("No data to fit")

        # Compute k
        k = num_features if k is None else min(k, num_features)
        # TODO: check
        projection = _compute_pca_projection(XTX.matrix, k)

        # TODO: check
        # X: (n, d)
        # XTX.matrix: (d, d)
        # projection: (d, k)
        # X @ projection: (n, k)
        # (X @ projection).T @ (X @ projection): (k, k)
        # projection.T @ X.T @ X @ projection = (k, d) @ (d, n) @ (n, d) @ (d, k)
        kernel, bias = _compute_kernel_bias_gram(
            projection.T @ XTX.matrix @ projection,
            projection.T @ XTY.matrix,
            fit_intercept=True,
            alpha=alpha,
        )
        kernel = kernel.reshape(1, k, 1)

        loc = XTX.mean if normalize else None
        scale = XTX.std if normalize else None

        with flax.nn.stateful() as state:
            model_def = PCR.partial(
                history_len=history_len,
                projection=projection,
                output_dim=output_dim,
                loc=loc,
                scale=scale,
                name=name,
            )
            _, params = model_def.init_by_shape(jax.random.PRNGKey(seed), [(1, input_dim)])
            model = flax.nn.Model(model_def, params)

        model.params["linear"]["kernel"] = kernel
        model.params["linear"]["bias"] = bias

        return model, state
