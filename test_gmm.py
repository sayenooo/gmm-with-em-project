"""Four small checks of the EM implementation."""
import unittest
from pathlib import Path

import numpy as np
from gmm_em import e_step, m_step, fit_once


class TestGMM(unittest.TestCase):
    def test_standard_normal(self):
        X = np.array([[0., 0.]])
        weights = np.array([1.])
        means = np.array([[0., 0.]])
        covariances = np.array([np.eye(2)])
        r, ll = e_step(X, weights, means, covariances)
        np.testing.assert_allclose(r, [[1.]])
        self.assertAlmostEqual(ll, -np.log(2 * np.pi))

    def test_weighted_update(self):
        X = np.array([[0., 0.], [2., 2.], [4., 4.]])
        r = np.array([[1., 0.], [.5, .5], [0., 1.]])
        weights, means, covs = m_step(X, r, 1e-6)
        np.testing.assert_allclose(weights, [.5, .5])
        np.testing.assert_allclose(means, [[2/3, 2/3], [10/3, 10/3]])
        self.assertTrue(np.all(np.linalg.eigvalsh(covs) > 0))

    def test_synthetic_recovery(self):
        rng = np.random.default_rng(19)
        left = rng.normal(-5, .5, (150, 2))
        right = rng.normal(5, .5, (150, 2))
        model = fit_once(np.vstack([left, right]), 2, 42)
        self.assertTrue(model['converged'])
        self.assertTrue(np.all(np.diff(model['history']) >= -1e-6))
        np.testing.assert_allclose(model['r'].sum(axis=1), 1.)
        expected = np.repeat([0, 1], 150)
        self.assertGreater(np.mean(model['r'].argmax(axis=1) == expected), .99)

    def test_faa_reproducibility(self):
        X = np.loadtxt(Path(__file__).with_name('FAA_AEDT_data.csv'), delimiter=',', skiprows=1)
        normal = fit_once(X, 3, 42)
        strict = fit_once(X, 3, 42, tol=1e-10, max_iter=5000)
        self.assertTrue(normal['converged'] and strict['converged'])
        self.assertTrue(np.all(np.diff(normal['history']) >= -1e-6))
        np.testing.assert_array_equal(normal['r'].argmax(1), strict['r'].argmax(1))
        self.assertAlmostEqual(normal['ll'], -4955.676997, places=3)


if __name__ == '__main__':
    unittest.main()
