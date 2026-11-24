"""Run with python -m unittest -v test_gmm."""
import unittest
import numpy as np
from gmm_em import e_step, m_step, fit_once

class TestGMM(unittest.TestCase):
    def test_standard_normal(self):
        r,ll=e_step(np.array([[0.,0.]]),np.array([1.]),np.array([[0.,0.]]),np.array([np.eye(2)]))
        np.testing.assert_allclose(r,[[1.]])
        self.assertAlmostEqual(ll,-np.log(2*np.pi))
    def test_weighted_update(self):
        X=np.array([[0.,0.],[2.,2.],[4.,4.]])
        r=np.array([[1.,0.],[.5,.5],[0.,1.]])
        w,mu,cov=m_step(X,r,1e-6)
        np.testing.assert_allclose(w,[.5,.5]); np.testing.assert_allclose(mu,[[2/3,2/3],[10/3,10/3]])
        self.assertTrue(np.all(np.linalg.eigvalsh(cov)>0))
    def test_synthetic_recovery(self):
        rng=np.random.default_rng(19)
        X=np.vstack([rng.normal(-5,.5,(150,2)),rng.normal(5,.5,(150,2))])
        fit=fit_once(X,2,42)
        self.assertTrue(fit['converged']); self.assertTrue(np.all(np.diff(fit['history'])>=-1e-6))
        np.testing.assert_allclose(fit['r'].sum(1),1.)
        self.assertGreater(np.mean(fit['r'].argmax(1)==np.repeat([0,1],150)),.99)
    def test_faa_reproducibility(self):
        from pathlib import Path
        X=np.loadtxt(Path(__file__).with_name('FAA_AEDT_data.csv'),delimiter=',',skiprows=1)
        m=fit_once(X,3,42); s=fit_once(X,3,42,tol=1e-10,max_iter=5000)
        self.assertTrue(m['converged'] and s['converged']); self.assertTrue(np.all(np.diff(m['history'])>=-1e-6))
        np.testing.assert_array_equal(m['r'].argmax(1),s['r'].argmax(1))
        self.assertAlmostEqual(m['ll'],-4955.676997,places=3)
if __name__=='__main__': unittest.main()
