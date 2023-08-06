"""timecast top-level API"""
from functools import partial
from typing import Callable
from typing import Tuple
from typing import Union

import flax
import jax
import jax.numpy as jnp
import numpy as onp


def smap(
    X: Union[onp.ndarray, Tuple[onp.ndarray, ...]],
    Y: Union[onp.ndarray, Tuple[onp.ndarray, ...]],
    optimizer: flax.optim.Optimizer,
    loss_fn: Callable[[onp.ndarray, onp.ndarray], onp.ndarray] = lambda true, pred: jnp.square(
        true - pred
    ).mean(),
    state: flax.nn.base.Collection = None,
    objective: Callable[
        [
            onp.ndarray,
            onp.ndarray,
            Callable[[onp.ndarray, onp.ndarray], onp.ndarray],
            flax.nn.base.Model,
        ],
        Tuple[onp.ndarray, onp.ndarray],
    ] = None,
):
    """Take gradients steps performantly on one data item at a time

    Args:
        X: onp.ndarray or tuple of onp.ndarray of inputs
        Y: onp.ndarray or tuple of onp.ndarray of outputs
        optimizer: initialized optimizer
        loss_fn: loss function to compose
        state: state required by flax
        objective: function composing loss functions

    Returns:
        onp.ndarray: result
    """

    def _smap(optstate, xy):
        """Helper function"""
        x, y = xy
        optimizer, state = optstate
        with flax.nn.stateful(state) as state:
            if objective is None:

                def func(model):
                    """Default objective function"""
                    y_hat = model(x)
                    return loss_fn(y, y_hat), y_hat

            else:
                func = partial(objective, x, y, loss_fn)
            (loss, y_hat), grad = jax.value_and_grad(func, has_aux=True)(optimizer.target)
            return (optimizer.apply_gradient(grad), state), y_hat

    (optimizer, state), pred = jax.lax.scan(_smap, (optimizer, state), (X, Y))
    return pred, optimizer, state
