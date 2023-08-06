import numpy as np
import numpy.testing as nt

from pyhrp.linalg import dist, correlation_from_covariance, sub, variance


def test_dist():
    cov = np.array([[1.0, 0.2], [0.2, 2.0]])
    a = correlation_from_covariance(cov)
    nt.assert_allclose(a, np.array([[1.0, 0.2 / np.sqrt(2.0)], [0.2 / np.sqrt(2.0), 1.0]]))
    nt.assert_allclose(dist(a), np.array([[0.000000e+00, 6.552017e-01], [6.552017e-01, 0.0]]), rtol=1e-6, atol=1e-6)


def test_sub():
    cov = np.array([[1, 0.5, 0], [0.5, 2, 0.0], [0, 0, 3]])
    a = sub(cov, idx=[0, 1])
    nt.assert_allclose(a, np.array([[1.0, 0.5], [0.5, 2.0]]))


def test_variance():
    cov = np.array([[1, 0.5, 0], [0.5, 2, 0.0], [0, 0, 3]])
    w = np.array([1.0, 0.5, 0.5])
    v = variance(cov=cov, w=w)
    nt.assert_approx_equal(v, 2.75)