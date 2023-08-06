"""Helper functions and classes for timecast.learners"""
from typing import Iterable
from typing import Tuple

import flax
import jax
import numpy as onp


class FitMixin:
    """Mixin class that provides a fit function for offline training / learner
    initialization"""

    @classmethod
    def fit(
        cls,
        data: Iterable[Tuple[onp.ndarray, onp.ndarray]],
        input_dim: int,
        output_dim: int = 1,
        seed: int = 0,
        **kwargs
    ) -> flax.nn.Model:
        """Fit and initialize learner on training data

        Notes:
            * We could infer input_dim from data, but for now, require
            users to explicitly provide
            * output_dim defaults to 1 and is ignored for now

        Todo:
            * Really intended for passing in timeseries at a time, not
            individual time series observations; is this the right general API?
            * Shape is (1, input_dim); what about mini-batches?

        Args:
            data: an iterable of tuples containing input/truth pairs of time
            series
            input_dim: number of feature dimensions in input
            output_dim: number of feature dimensions in output
            seed: random seed for jax random
            kwargs: Extra keyword arguments

        Returns:
            flax.nn.Model: initialized model
        """
        with flax.nn.stateful() as state:
            model_def = cls.partial(name=cls.__name__, **kwargs)
            _, params = model_def.init_by_shape(jax.random.PRNGKey(seed), [(1, input_dim)])
            model = flax.nn.Model(model_def, params)

        return model, state
