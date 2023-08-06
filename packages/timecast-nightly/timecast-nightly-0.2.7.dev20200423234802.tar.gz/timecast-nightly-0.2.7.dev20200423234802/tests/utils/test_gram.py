"""timecast.utils.gram: testing"""
import jax.numpy as jnp
import numpy as onp
import pytest

from timecast.utils.gram import OnlineGram


dims = [1, 10, 20]


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [1, 10, 20])
def test_gram_update(X_dim, Y_dim, n):
    """Test update"""
    X = onp.random.rand(n, X_dim)
    Y = onp.random.rand(n, Y_dim)

    gram = OnlineGram(X_dim, Y_dim, fit_intercept=False, normalize=False)
    gram.update(X, Y)

    onp.testing.assert_array_almost_equal(gram.matrix, X.T @ Y)


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [1, 10, 20])
def test_gram_update_iterative(X_dim, Y_dim, n):
    """Test update iteratively"""
    X = onp.random.rand(n, X_dim)
    Y = onp.random.rand(n, Y_dim)

    gram = OnlineGram(X_dim, Y_dim, fit_intercept=False, normalize=False)

    for x, y in zip(X, Y):
        gram.update(x.reshape(1, -1), y.reshape(1, -1))

    onp.testing.assert_array_almost_equal(gram.matrix, X.T @ Y, decimal=3)


def test_gram_update_value_error():
    """Test update value error"""
    gram = OnlineGram(1, 1)
    with pytest.raises(ValueError):
        gram.update(onp.random.rand(4, 1), onp.random.rand(1, 1))

    with pytest.raises(ValueError):
        gram.update(onp.random.rand(4, 1))

    gram = OnlineGram(1)
    with pytest.raises(ValueError):
        gram.update(onp.ones((1, 1)), onp.ones((1, 1)))


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [2, 10, 20])
def test_gram_normalize(X_dim, Y_dim, n):
    """Test normalize"""
    X = onp.random.rand(n, X_dim)
    Y = onp.random.rand(n, Y_dim)

    gram = OnlineGram(X_dim, Y_dim, fit_intercept=False, normalize=True)
    gram.update(X, Y)

    X_norm = (X - X.mean(axis=0)) / X.std(axis=0)
    Y_norm = (Y - Y.mean(axis=0)) / Y.std(axis=0)
    onp.testing.assert_array_almost_equal(gram.matrix, X_norm.T @ Y_norm, decimal=1)


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("n", [2, 10, 20])
@pytest.mark.parametrize("normalize", [True, False])
def test_gram_intercept_xtx(X_dim, n, normalize):
    """Test intercept on X.T @ X"""
    X = onp.random.rand(n, X_dim)

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
    X = onp.random.rand(n, X_dim)
    Y = onp.random.rand(n, Y_dim)

    gram = OnlineGram(X_dim, Y_dim, fit_intercept=True, normalize=normalize)

    gram.update(X, Y)

    if normalize:
        X = (X - X.mean(axis=0)) / X.std(axis=0)
        Y = (Y - Y.mean(axis=0)) / Y.std(axis=0)

    X = jnp.hstack((jnp.ones((n, 1)), X))

    onp.testing.assert_array_almost_equal(gram.matrix, X.T @ Y, decimal=1)
