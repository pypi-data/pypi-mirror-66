"""timecast.utils.historify"""
import numpy as onp
import pytest

from timecast.utils import historify


@pytest.mark.parametrize("m", [1, 10])
@pytest.mark.parametrize("n", [1, 10])
@pytest.mark.parametrize("num_histories", [0, 1, 10])
@pytest.mark.parametrize("history_len", [-1, 0, 1, 10])
@pytest.mark.parametrize("offset", [0, 1, 10])
def test_historify(m, n, num_histories, history_len, offset):
    """Test history-making"""
    X = onp.random.rand(m, n)

    if (
        num_histories < 1
        or history_len < 1
        or X.shape[0] < offset + num_histories + history_len - 1
    ):
        with pytest.raises(ValueError):
            historify(X, num_histories, history_len, offset)

    else:
        batched = historify(X, num_histories, history_len, offset)

        for i, batch in enumerate(batched):
            onp.testing.assert_array_almost_equal(batch, X[i + offset : i + offset + history_len])
