"""timecast.optim._rmsprop"""
import jax.numpy as jnp
import numpy as onp
from flax import struct
from flax.optim import OptimizerDef


@struct.dataclass
class _RMSPropHyperParams:
    """RMSProp hyper parameters"""

    learning_rate: float
    beta2: float
    eps: float


@struct.dataclass
class _RMSPropParamState:
    """RMSProp parameter state"""

    v: onp.ndarray


class RMSProp(OptimizerDef):
    """RMSProp optimizer"""

    def __init__(self, learning_rate: float = 1.0, beta2=0.999, eps=1e-8):
        """Initialize hyper parameters"""
        hyper_params = _RMSPropHyperParams(learning_rate, beta2, eps)
        super().__init__(hyper_params)

    def init_param_state(self, param):
        """Initialize parameter state"""
        return _RMSPropParamState(jnp.zeros_like(param))

    def apply_param_gradient(self, step, hyper_params, param, state, grad):
        """Apply per-parameter gradients"""

        new_v = hyper_params.beta2 * state.v + (1.0 - hyper_params.beta2) * jnp.square(grad)
        new_param = param - hyper_params.learning_rate * grad / (jnp.sqrt(new_v) + hyper_params.eps)
        new_state = _RMSPropParamState(new_v)

        return new_param, new_state
