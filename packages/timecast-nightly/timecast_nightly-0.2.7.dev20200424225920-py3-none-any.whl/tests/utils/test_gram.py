"""timecast.utils.gram: testing"""
import jax
import jax.numpy as jnp
import numpy as onp
import pytest

from timecast.utils import random
from timecast.utils.gram import OnlineGram


dims = [1, 10, 20]


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [1, 10, 20])
def test_gram_update(X_dim, Y_dim, n):
    """Test update"""
    X = jax.random.uniform(random.generate_key(), shape=(n, X_dim))
    Y = jax.random.uniform(random.generate_key(), shape=(n, Y_dim))

    gram = OnlineGram(X_dim, Y_dim, fit_intercept=False, normalize=False)
    gram.update(X, Y)

    onp.testing.assert_array_almost_equal(gram.matrix, X.T @ Y)


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [1, 10, 20])
def test_gram_update_iterative(X_dim, Y_dim, n):
    """Test update iteratively"""
    X = jax.random.uniform(random.generate_key(), shape=(n, X_dim))
    Y = jax.random.uniform(random.generate_key(), shape=(n, Y_dim))

    gram = OnlineGram(X_dim, Y_dim, fit_intercept=False, normalize=False)

    for x, y in zip(X, Y):
        gram.update(x.reshape(1, -1), y.reshape(1, -1))

    onp.testing.assert_array_almost_equal(gram.matrix, X.T @ Y, decimal=3)


def test_gram_update_value_error():
    """Test update value error"""
    gram = OnlineGram(1, 1)
    with pytest.raises(ValueError):
        gram.update(
            jax.random.uniform(random.generate_key(), shape=(4, 1)),
            jax.random.uniform(random.generate_key(), shape=(1, 1)),
        )

    with pytest.raises(ValueError):
        gram.update(jax.random.uniform(random.generate_key(), shape=(4, 1)))

    gram = OnlineGram(1)
    with pytest.raises(ValueError):
        gram.update(onp.ones((1, 1)), onp.ones((1, 1)))


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [2, 10, 20])
def test_gram_normalize(X_dim, Y_dim, n):
    """Test normalize"""
    X = jax.random.uniform(random.generate_key(), shape=(n, X_dim))
    Y = jax.random.uniform(random.generate_key(), shape=(n, Y_dim))

    gram = OnlineGram(X_dim, Y_dim, fit_intercept=False, normalize=True)
    gram.update(X, Y)

    X_norm = (X - X.mean(axis=0)) / X.std(axis=0)
    Y_norm = (Y - Y.mean(axis=0)) / Y.std(axis=0)
    onp.testing.assert_array_almost_equal(gram.matrix, X_norm.T @ Y_norm, decimal=1)


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("n", [3, 10, 20])
@pytest.mark.parametrize("normalize", [True, False])
def test_gram_intercept_xtx(X_dim, n, normalize):
    """Test intercept on X.T @ X"""
    X = jax.random.uniform(random.generate_key(), shape=(n, X_dim))

    gram = OnlineGram(X_dim, fit_intercept=True, normalize=normalize)
    gram.update(X)

    if normalize:
        X = (X - X.mean(axis=0)) / X.std(axis=0)

    X = jnp.hstack((jnp.ones((n, 1)), X))

    onp.testing.assert_array_almost_equal(gram.matrix, X.T @ X, decimal=1)


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [2, 10, 20])
@pytest.mark.parametrize("normalize", [True, False])
def test_gram_intercept_xty(X_dim, Y_dim, n, normalize):
    """Test intercept on X.T @ Y"""
    X = jax.random.uniform(random.generate_key(), shape=(n, X_dim))
    Y = jax.random.uniform(random.generate_key(), shape=(n, Y_dim))

    gram = OnlineGram(X_dim, Y_dim, fit_intercept=True, normalize=normalize)

    gram.update(X, Y)

    onp.testing.assert_array_almost_equal(gram.mean.squeeze(), X.mean(axis=0))
    onp.testing.assert_array_almost_equal(gram.std.squeeze(), X.std(axis=0))
    assert gram.observations == X.shape[0]

    if normalize:
        X = (X - X.mean(axis=0)) / X.std(axis=0)
        Y = (Y - Y.mean(axis=0)) / Y.std(axis=0)

    X = jnp.hstack((jnp.ones((n, 1)), X))

    onp.testing.assert_array_almost_equal(gram.matrix, X.T @ Y, decimal=1)
