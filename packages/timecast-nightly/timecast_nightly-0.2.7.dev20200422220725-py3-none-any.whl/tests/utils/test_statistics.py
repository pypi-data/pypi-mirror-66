"""timecast.utils.statistics: testing"""
import numpy as onp
import pytest

from timecast.utils.statistics import OnlineStatistics


@pytest.mark.parametrize("n", [2, 10, 50, 100])
@pytest.mark.parametrize("j", [1, 10, 100])
@pytest.mark.parametrize("k", [1, 10, 100])
@pytest.mark.parametrize("func", ["sum", "mean", "std", "var", "observations", "zscore"])
def test_online_sum(n, j, k, func):
    """Test online statistics"""
    stats = OnlineStatistics(input_dim=k)
    X = onp.random.rand(n, j * k)

    for i in X:
        stats.update(i.reshape(j, k))

    if func == "zscore":
        onp.testing.assert_array_almost_equal(
            stats.zscore(X[0, :].reshape(j, k)),
            (X[0, :].reshape(j, k) - stats.mean()) / stats.std(),
        )
    elif func != "observations":
        result = getattr(stats, func)()
        onp.testing.assert_array_almost_equal(
            result, getattr(X.reshape(n * j, k), func)(axis=0).reshape(1, -1), decimal=2
        )
    else:
        assert n * j == stats.observations()
