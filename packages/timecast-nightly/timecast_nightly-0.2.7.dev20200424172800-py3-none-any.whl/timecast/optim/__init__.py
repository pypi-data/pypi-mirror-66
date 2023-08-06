"""timecast.optim

Todo:
    * Document available optimizers
"""
from flax.optim import Adam
from flax.optim import GradientDescent
from flax.optim import LAMB
from flax.optim import LARS
from flax.optim import Momentum

from timecast.optim._adagrad import Adagrad
from timecast.optim._rmsprop import RMSProp

__all__ = ["Adagrad", "Adam", "GradientDescent", "Momentum", "LAMB", "LARS", "RMSProp"]
