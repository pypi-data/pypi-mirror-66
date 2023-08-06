"""timecast.learners.pcr: testing"""
import numpy as onp
import pytest
from sklearn.decomposition import PCA

from timecast.learners._pcr import _compute_pca_projection


@pytest.mark.parametrize("shape", [(1, 1), (10, 1), (2, 10), (10, 2)])
def test_compute_pca_projection(shape):
    """Test PCA projection of X vs X.T @ X"""
    X = onp.random.rand(*shape)
    XTX = X.T @ X

    k = 1 if X.ndim == 1 else min(X.shape)
    p1 = _compute_pca_projection(X, k)
    p2 = _compute_pca_projection(XTX, k)

    onp.testing.assert_array_almost_equal(abs(p1), abs(p2), decimal=3)


@pytest.mark.parametrize("shape", [(1, 1), (10, 1), (1, 10), (10, 10)])
def test_compute_pca_projection_sklearn(shape):
    """Test PCA projection of X vs sklearn"""
    X = onp.random.rand(*shape)

    projection = _compute_pca_projection(X, 1, center=True)

    pca = PCA(n_components=1)
    pca.fit(X)

    onp.testing.assert_array_almost_equal(abs(projection), abs(pca.components_.T), decimal=3)
