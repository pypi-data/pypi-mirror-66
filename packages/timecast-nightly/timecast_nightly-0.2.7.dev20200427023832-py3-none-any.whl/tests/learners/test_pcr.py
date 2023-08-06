"""timecast.learners.pcr: testing"""
import flax
import jax
import jax.numpy as jnp
import numpy as onp
import pytest
from sklearn.decomposition import PCA

from timecast.learners import PCR
from timecast.learners._ar import _compute_kernel_bias
from timecast.learners._pcr import _compute_pca_projection
from timecast.utils import historify
from timecast.utils import internalize
from timecast.utils import random


@pytest.mark.parametrize("shape", [(1, 1), (10, 1), (2, 10), (10, 2)])
def test_compute_pca_projection(shape):
    """Test PCA projection of X vs X.T @ X"""
    X = jax.random.uniform(random.generate_key(), shape=shape)
    XTX = X.T @ X

    k = 1 if X.ndim == 1 else min(X.shape)
    p1 = _compute_pca_projection(X, k)
    p2 = _compute_pca_projection(XTX, k)

    onp.testing.assert_array_almost_equal(abs(p1), abs(p2), decimal=3)


@pytest.mark.parametrize("shape", [(1, 1), (10, 1), (1, 10), (10, 10)])
def test_compute_pca_projection_sklearn(shape):
    """Test PCA projection of X vs sklearn"""
    X = jax.random.uniform(random.generate_key(), shape=shape)

    projection = _compute_pca_projection(X, 1, center=True)

    pca = PCA(n_components=1)
    pca.fit(X)

    onp.testing.assert_array_almost_equal(abs(projection), abs(pca.components_.T), decimal=3)


def test_pcr_fit_index_error():
    """Test PCR fit with no data"""
    with pytest.raises(IndexError):
        PCR.fit([], input_dim=1, history_len=1)


@pytest.mark.parametrize("shape", [(100, 1), (200, 5)])
@pytest.mark.parametrize("history_len", [1, 2, 5])
def test_pcr_fit(shape, history_len):
    """Test PCR fit"""
    X = jax.random.uniform(random.generate_key(), shape=shape)
    Y = jax.random.uniform(random.generate_key(), shape=(shape[0],))

    pcr, state = PCR.fit(
        [(X, Y, None)], input_dim=shape[1], history_len=history_len, normalize=False
    )

    X = internalize(X, shape[1])[0]
    Y = internalize(Y, 1)[0]

    num_histories = X.shape[0] - history_len + 1
    X = historify(X, num_histories=num_histories, history_len=history_len).reshape(
        num_histories, -1
    )
    Y = Y[-len(X) :]

    k = shape[1] * history_len

    projection = _compute_pca_projection(X, k)
    kernel, bias = _compute_kernel_bias(X @ projection, Y)
    kernel = kernel.reshape(1, k, 1)

    onp.testing.assert_array_almost_equal(
        abs(kernel), abs(pcr.params["linear"]["kernel"]), decimal=3
    )
    onp.testing.assert_array_almost_equal(abs(bias), abs(pcr.params["linear"]["bias"]), decimal=3)


def test_pcr_apply():
    """Test PCR apply shapes"""
    pcr, state = PCR.new(
        shape=(1, 1), history_len=2, projection=jnp.eye(2), loc=0, scale=1, history=jnp.ones((2, 1))
    )

    with flax.nn.stateful(state) as state:
        scalar = pcr(1)

    with flax.nn.stateful(state) as state:
        vector = pcr(jnp.ones((1,)))

    onp.testing.assert_array_almost_equal(scalar, vector)


def test_pcr_fit_value_error():
    """Test number of observations"""
    X = jax.random.uniform(random.generate_key(), shape=(1, 10))
    Y = jax.random.uniform(random.generate_key(), shape=(10, 1))

    with pytest.raises(ValueError):
        PCR.fit([(X, Y, None)], input_dim=10, history_len=1)
