"""timecast.utils.gram"""
import jax
import jax.numpy as jnp

from timecast.utils import internalize
from timecast.utils.statistics import OnlineStatistics


class OnlineGram:
    """Compute gram matrix of observations online

    Notes:
        * Computes X.T @ X, where axis 0 is time and axis 1 is
        features
        * In the case where we supply a second matrix, this is no
        longer a gram matrix; X.T @ Y
    """

    def __init__(self, input_dim: int = 1, output_dim: int = None) -> None:
        """Initialize OnlineGram

        Args:
            input_dim (int): feature dimension (typically X.shape[1])
            output_dim(int): same as input_dim unless we supply a
            second matrix with different dimensions
        """
        self._input_dim = input_dim
        self._output_dim = output_dim or input_dim
        self._matrix = jnp.zeros((self._input_dim, self._output_dim))

    @property
    def matrix(self):
        """Property to retrieve gram matrix"""
        return self._matrix

    def update(self, X: jnp.ndarray, Y: jnp.ndarray = None) -> None:
        """Update Gram matrix bassed on new data"""
        X = internalize(X, self._input_dim)[0]
        if Y is not None:
            Y = internalize(Y, self._output_dim)[0]
        else:
            Y = X

        if X.shape[0] != Y.shape[0]:
            raise ValueError(
                "Inputs must have the same number of observations; got {}, {}".format(
                    X.shape[0], Y.shape[0]
                )
            )
        self._matrix += X.T @ Y

    def normalize(self, X_stats: OnlineStatistics, Y_stats: OnlineStatistics = None) -> None:
        """Z-score across feature dimensions"""
        Y_stats = Y_stats or X_stats

        if X_stats.observations != Y_stats.observations:
            raise ValueError(
                "Inputs must have the same number of observations; got {}, {}".format(
                    X_stats.observations, Y_stats.observations
                )
            )

        n = X_stats.observations

        self._matrix = (
            self._matrix
            + n * jnp.outer(X_stats.mean, Y_stats.mean)
            - jnp.outer(X_stats.mean, Y_stats.sum)
            - jnp.outer(X_stats.sum, Y_stats.mean)
        ) / jnp.outer(X_stats.std, Y_stats.std)

        # Replace nans with 0s because std of some columns may be 0
        self._matrix = jnp.nan_to_num(self._matrix)

    def intercept(
        self, X_stats: OnlineStatistics, Y_stats: OnlineStatistics = None, normalize: bool = False
    ) -> jnp.ndarray:
        """Add an intercept to X for X.T @ Y

        Notes:
            * This method returns rather than modifies _matrix because
            the change in dimension would mean we can no longer update
        """
        result = jnp.concatenate((jnp.zeros((1, self._matrix.shape[1])), self._matrix), axis=0)

        if Y_stats is None:
            result = jnp.concatenate((jnp.zeros((result.shape[0], 1)), result), axis=1)

        stats = X_stats if Y_stats is None else Y_stats
        sumcol = stats.sum

        if normalize:
            sumcol = jnp.zeros_like(sumcol)

        if Y_stats is None:
            result = jax.ops.index_update(result, jax.ops.index[0, 0], stats.observations)
            result = jax.ops.index_update(result, jax.ops.index[:1, 1:], sumcol)
            result = jax.ops.index_update(result, jax.ops.index[1:, :1], sumcol.T)
        else:
            result = jax.ops.index_update(result, jax.ops.index[:1, :], sumcol)

        return result
