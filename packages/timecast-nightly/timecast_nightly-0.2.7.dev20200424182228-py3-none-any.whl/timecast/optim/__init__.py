"""timecast.optim

Todo:
    * Document available optimizers
"""
import flax
from flax.optim import Adam
from flax.optim import GradientDescent
from flax.optim import LARS
from flax.optim import Momentum

from timecast.optim._adagrad import Adagrad
from timecast.optim._rmsprop import RMSProp

# from flax.optim import LAMB


class DummyGrad(flax.optim.OptimizerDef):
    """Dummy optimizer for testing"""

    def __init__(self):
        """Initialize hyper parameters"""
        super().__init__({})

    def init_param_state(self, param):
        """Initialize parameter state"""
        return {}

    def apply_param_gradient(self, step, hyper_params, param, state, grad):
        """Apply per-parametmer gradients"""
        return param, state


__all__ = ["Adagrad", "Adam", "GradientDescent", "Momentum", "LAMB", "LARS", "RMSProp"]
