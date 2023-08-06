"""timecast.learners.Index: testing"""
import flax
import jax
import numpy as onp
import pytest

from timecast.learners import Index
from timecast.utils import random

shapes = [(4, 32), (10,), (10, 1), (1,), (1, 10)]


def create_index(shape, index):
    """Generate Index model and state"""
    with flax.nn.stateful() as state:
        model_def = Index.partial(index=index)
        _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
        model = flax.nn.Model(model_def, params)
    return model, state


@pytest.mark.parametrize("shape", shapes)
def test_index(shape):
    """Test Index"""
    model, state = create_index(shape, index=0)

    X = jax.random.uniform(random.generate_key(), shape=shape)
    with flax.nn.stateful(state) as state:
        ys = model(X)

    onp.testing.assert_array_almost_equal(X[0], ys)


@pytest.mark.parametrize("shape", shapes)
def test_index_bad_index(shape):
    """Test bad_index"""
    with pytest.raises(IndexError):
        _, _ = create_index(shape, index=-1)


def test_index_scalar():
    """Test scalar input"""
    model, state = create_index((2, 1), index=0)
    with pytest.raises(ValueError):
        with flax.nn.stateful(state) as state:
            _ = model(1)
