"""flax.nn.Module for taking an index from input"""
import flax
import jax.numpy as jnp
import numpy as onp


class Index(flax.nn.Module):
    """Identity index online learner"""

    def apply(self, x: onp.ndarray, index: int):
        """
        Note:
            * Returns `x[index]` as the prediction for the next time step
            * This is a workaround for the case where we have a blackbox series
            of predictions (see documentation)

        Args:
            x (onp.ndarray): input data
            index (int): index to take

        Returns:
            onp.ndarray: result
        """

        if jnp.isscalar(x):
            raise ValueError("Input x must be an array for Index learner")

        # We don't check for index < x.shape[0] because this confuses flax's
        # init_by_shape
        if not isinstance(index, int) or index < 0:
            raise IndexError("Index must be positive. Got index {}".format(index))

        return x[index]
