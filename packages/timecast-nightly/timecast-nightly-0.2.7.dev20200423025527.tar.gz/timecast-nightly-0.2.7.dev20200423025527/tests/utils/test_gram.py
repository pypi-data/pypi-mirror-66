"""timecast.utils.gram: testing"""
import jax.numpy as jnp
import numpy as onp
import pytest

from timecast.utils.gram import OnlineGram
from timecast.utils.statistics import OnlineStatistics


dims = [1, 10, 20]


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [1, 10, 20])
def test_gram_update(X_dim, Y_dim, n):
    """Test update"""
    X = onp.random.rand(n, X_dim)
    Y = onp.random.rand(n, Y_dim)

    gram = OnlineGram(X_dim, Y_dim)
    gram.update(X, Y)

    onp.testing.assert_array_almost_equal(gram.matrix, X.T @ Y)


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [1, 10, 20])
def test_gram_update_iterative(X_dim, Y_dim, n):
    """Test update iteratively"""
    X = onp.random.rand(n, X_dim)
    Y = onp.random.rand(n, Y_dim)

    gram = OnlineGram(X_dim, Y_dim)

    for x, y in zip(X, Y):
        gram.update(x, y)

    onp.testing.assert_array_almost_equal(gram.matrix, X.T @ Y)


def test_gram_update_value_error():
    """Test update value error"""
    gram = OnlineGram(1, 1)
    with pytest.raises(ValueError):
        gram.update(onp.random.rand(4, 1), onp.random.rand(1, 1))


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [2, 10, 20])
def test_gram_normalize(X_dim, Y_dim, n):
    """Test normalize"""
    X = onp.random.rand(n, X_dim)
    Y = onp.random.rand(n, Y_dim)

    gram = OnlineGram(X_dim, Y_dim)
    X_stats = OnlineStatistics(X_dim)
    Y_stats = OnlineStatistics(Y_dim)
    X_stats.update(X)
    Y_stats.update(Y)

    for x, y in zip(X, Y):
        gram.update(x, y)

    gram.normalize(X_stats, Y_stats)

    X_norm = (X - X.mean(axis=0)) / X.std(axis=0)
    Y_norm = (Y - Y.mean(axis=0)) / Y.std(axis=0)
    onp.testing.assert_array_almost_equal(gram.matrix, X_norm.T @ Y_norm, decimal=2)


def test_gram_normalize_value_error():
    """Test normalize value_error"""
    gram = OnlineGram(1, 1)
    stat1 = OnlineStatistics(1)
    stat2 = OnlineStatistics(1)
    stat2.update(3)

    with pytest.raises(ValueError):
        gram.normalize(stat1, stat2)


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("n", [2, 10, 20])
@pytest.mark.parametrize("normalize", [True, False])
def test_gram_intercept_xtx(X_dim, n, normalize):
    """Test intercept on X.T @ X"""
    X = onp.random.rand(n, X_dim)

    gram = OnlineGram(X_dim)
    gram.update(X)

    X_stats = OnlineStatistics(X_dim)
    X_stats.update(X)

    if normalize:
        gram.normalize(X_stats)
        X = (X - X.mean(axis=0)) / X.std(axis=0)

    result = gram.intercept(X_stats, normalize=normalize)
    X = jnp.hstack((jnp.ones((n, 1)), X))

    onp.testing.assert_array_almost_equal(result, X.T @ X, decimal=2)


@pytest.mark.parametrize("X_dim", dims)
@pytest.mark.parametrize("Y_dim", dims)
@pytest.mark.parametrize("n", [2, 10, 20])
@pytest.mark.parametrize("normalize", [True, False])
def test_gram_intercept_xty(X_dim, Y_dim, n, normalize):
    """Test intercept on X.T @ Y"""
    X = onp.random.rand(n, X_dim)
    Y = onp.random.rand(n, Y_dim)

    gram = OnlineGram(X_dim, Y_dim)
    X_stats = OnlineStatistics(X_dim)
    Y_stats = OnlineStatistics(Y_dim)
    X_stats.update(X)
    Y_stats.update(Y)

    gram.update(X, Y)

    if normalize:
        gram.normalize(X_stats, Y_stats)
        X = (X - X.mean(axis=0)) / X.std(axis=0)
        Y = (Y - Y.mean(axis=0)) / Y.std(axis=0)

    result = gram.intercept(X_stats, Y_stats, normalize=normalize)
    X = jnp.hstack((jnp.ones((n, 1)), X))

    onp.testing.assert_array_almost_equal(result, X.T @ Y, decimal=2)
