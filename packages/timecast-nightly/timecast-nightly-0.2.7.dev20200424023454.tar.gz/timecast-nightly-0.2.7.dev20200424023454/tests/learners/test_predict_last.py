"""timecast.learners.PredictLast: testing"""
import flax
import jax
import numpy as onp
import pytest

from timecast.learners import PredictLast

shapes = [(4, 32), (10,), (10, 1), (1,), (1, 10)]


def create_predict_last(shape):
    """Generate PredictLast model and state"""
    with flax.nn.stateful() as state:
        _, params = PredictLast.init_by_shape(jax.random.PRNGKey(0), [shape])
        model = flax.nn.Model(PredictLast, params)
    return model, state


@pytest.mark.parametrize("shape", shapes)
def test_predict_last(shape):
    """Test PredictLast"""
    model, state = create_predict_last(shape)

    X = onp.random.rand(*shape)
    with flax.nn.stateful(state) as state:
        ys = model(X)

    onp.testing.assert_array_almost_equal(X, ys)
