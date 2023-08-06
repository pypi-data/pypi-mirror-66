"""timecast.utils.statistics"""
from numbers import Real
from typing import Union

import jax.numpy as np

from timecast.utils import internalize


class OnlineStatistics:
    """Compute summary statistics online"""

    def __init__(self, input_dim: int = 1):
        """Initialize OnlineStatistics"""
        self._input_dim = input_dim
        self._mean = np.zeros((1, input_dim))
        self._var = np.zeros((1, input_dim))
        self._sum = np.zeros((1, input_dim))
        self._observations = 0

    def update(self, observation: Union[Real, np.ndarray]) -> None:
        """Update with new observation"""
        observation, is_value, self._dim, _ = internalize(observation, self._input_dim)

        num_observations = observation.shape[0]

        prev_mean = self._mean
        curr_mean = observation if is_value else observation.mean(axis=0)
        self._mean = (self._observations * prev_mean + num_observations * curr_mean) / (
            self._observations + num_observations
        )

        prev_var = self._var
        curr_var = 0 if is_value else observation.var(axis=0)

        self._var = (
            self._observations * prev_var
            + num_observations * curr_var
            + self._observations * ((prev_mean - self._mean) ** 2)
            + num_observations * ((curr_mean - self._mean) ** 2)
        ) / (self._observations + num_observations)

        self._sum += observation if is_value else observation.sum(axis=0)

        self._observations += num_observations

    def mean(self) -> Union[Real, np.ndarray]:
        """Mean"""
        return self._mean

    def var(self) -> Union[Real, np.ndarray]:
        """Variance"""
        return self._var

    def std(self) -> Union[Real, np.ndarray]:
        """Standard deviation"""
        return np.sqrt(self._var)

    def sum(self) -> Union[Real, np.ndarray]:
        """Sum"""
        return self._sum

    def observations(self) -> int:
        """Number of observations"""
        return self._observations

    def zscore(self, data: np.ndarray) -> Union[Real, np.ndarray]:
        """Zscore an observation based on current statistics"""
        data, _, _, _ = internalize(data, self._input_dim)
        return (data - self.mean()) / self.std()
