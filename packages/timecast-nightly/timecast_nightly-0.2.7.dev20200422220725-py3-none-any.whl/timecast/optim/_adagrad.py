"""timecast.optim._adagrad"""
import jax.numpy as jnp
import numpy as onp
from flax import struct
from flax.optim import OptimizerDef


@struct.dataclass
class _AdagradHyperParams:
    """Adagrad hyper parameters"""

    learning_rate: float


@struct.dataclass
class _AdagradParamState:
    """Adagrad parameter state"""

    G: onp.ndarray


class Adagrad(OptimizerDef):
    """Adagrad optimizer"""

    def __init__(self, learning_rate: float = 1.0):
        """Initialize hyper parameters"""
        hyper_params = _AdagradHyperParams(learning_rate)
        super().__init__(hyper_params)

    def init_param_state(self, param):
        """Initialize parameter state"""
        return _AdagradParamState(jnp.zeros_like(param))

    def apply_param_gradient(self, step, hyper_params, param, state, grad):
        """Apply per-parameter gradients"""

        new_G = state.G + jnp.square(grad)
        new_param = param - hyper_params.learning_rate * grad / jnp.sqrt(new_G)
        new_state = _AdagradParamState(new_G)

        return new_param, new_state
