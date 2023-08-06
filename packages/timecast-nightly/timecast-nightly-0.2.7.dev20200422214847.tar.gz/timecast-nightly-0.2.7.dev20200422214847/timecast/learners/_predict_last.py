"""flax.nn.Module for predicting last value

Todo:
    * Implement last value n steps ago (requires state)
"""
import flax
import jax
import numpy as onp

from timecast.learners.base import FitMixin


class PredictLast(FitMixin, flax.nn.Module):
    """Identity online learner"""

    def apply(self, x: onp.ndarray):
        """
        Note:
            * Returns `x` as the prediction for the next time step

        Args:
            x (onp.ndarray): input data

        Returns:
            onp.ndarray: result
        """
        # TODO: Remove this once flax updates
        _ = self.param("dummy", (), jax.nn.initializers.zeros)
        return x
