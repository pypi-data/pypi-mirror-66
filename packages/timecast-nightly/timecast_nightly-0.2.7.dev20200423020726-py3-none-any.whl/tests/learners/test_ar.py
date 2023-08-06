"""timecast.learners.AR: testing"""
import flax
import jax
import jax.numpy as jnp
import numpy as onp
import pytest
from sklearn.linear_model import Ridge

from timecast.learners import AR
from timecast.learners._ar import _compute_kernel_bias
from timecast.utils import historify


shapes = [(32, 4), (4, 32), (10,), (10, 1), (1,), (1, 10), (10, 10)]


def create_ar(shape, output_features, history_len, history=None):
    """Create AR model"""
    model_def = AR.partial(
        output_features=output_features, history_len=history_len, history=history
    )
    with flax.nn.stateful() as state:
        _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
        model = flax.nn.Model(model_def, params)
    return model, state


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("output_features", [1, 10])
@pytest.mark.parametrize("history_len", [1, 10])
def test_ar_ys_shape(shape, output_features, history_len):
    """Test output shape"""
    model, state = create_ar(shape, output_features, history_len)
    with flax.nn.stateful(state) as _:
        ys = model(onp.random.rand(*shape))

    assert ys.shape == (output_features,)


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("output_features", [1, 10])
@pytest.mark.parametrize("history_len", [1, 10])
def test_ar_history_shape(shape, output_features, history_len):
    """Test history shape"""
    model, state = create_ar(shape, output_features, history_len)
    with flax.nn.stateful(state) as state:
        _ = model(onp.random.rand(*shape))

    print(state.as_dict())

    input_features = shape[0] if len(shape) == 1 else shape[1]
    assert state.as_dict()["/"]["history"].shape == (history_len, input_features)


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("output_features", [1, 10])
@pytest.mark.parametrize("history_len", [1, 10])
def test_ar_history(shape, output_features, history_len):
    """Test history values"""
    input_features = shape[0] if len(shape) == 1 else shape[1]
    history = onp.random.rand(history_len, input_features)
    model, state = create_ar(shape, output_features, history_len, history)

    onp.testing.assert_array_almost_equal(history, state.as_dict()["/"]["history"])


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("fit_intercept", [True, False])
@pytest.mark.parametrize("alpha", [0.0, 0.5, 1.0])
def test_compute_kernel_bias(shape, fit_intercept, alpha):
    """Test kernel and bias computation"""
    if len(shape) == 1:
        shape += (1,)
    X = onp.random.rand(*shape)
    Y = onp.random.rand(shape[0])

    # Ignore underdetermined systems for now
    if shape[0] > shape[1]:
        ridge = Ridge(alpha=alpha, fit_intercept=fit_intercept)
        expected = ridge.fit(X, Y)
        kernel, bias = _compute_kernel_bias(X, Y, alpha=alpha, fit_intercept=fit_intercept)
        onp.testing.assert_array_almost_equal(expected.coef_, kernel, decimal=2)
        onp.testing.assert_array_almost_equal(expected.intercept_, bias, decimal=2)


@pytest.mark.parametrize("shape", [(40, 1), (50, 5)])
@pytest.mark.parametrize("fit_intercept", [True, False])
@pytest.mark.parametrize("alpha", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("history_len", [1, 5, 10])
def test_ar_fit(shape, history_len, fit_intercept, alpha):
    """Test AR class method fit"""
    X = onp.random.rand(*shape)
    Y = onp.random.rand(shape[0])

    num_histories = shape[0] - history_len + 1
    history = historify(X, num_histories, history_len).reshape(num_histories, -1)

    kernel, bias = _compute_kernel_bias(history, Y[-len(history) :], alpha=alpha)
    kernel = kernel.reshape(history_len, shape[1], 1)
    bias = jnp.expand_dims(jnp.asarray(bias), 0)

    ar, state = AR.fit(X, Y, history_len=history_len, alpha=alpha)
    ar_kernel = ar.params["linear"]["kernel"]
    ar_bias = ar.params["linear"]["bias"]

    onp.testing.assert_array_almost_equal(kernel, ar_kernel)
    onp.testing.assert_array_almost_equal(bias, ar_bias)
