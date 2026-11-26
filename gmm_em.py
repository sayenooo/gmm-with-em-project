"""GMM with EM from scratch. NumPy is used only for numerical operations.
AI-assisted implementation and refactoring: see AI_DISCLOSURE.md.
"""
import argparse
import time
from pathlib import Path

import numpy as np


# 1. Initialize the Gaussian components (distance-weighted centers).
def initialize(X, k, rng, reg):
    n, d = X.shape
    means = [X[rng.integers(n)].copy()]
    for _ in range(1, k):
        distances = np.min(np.sum((X[:, None, :] - means) ** 2, axis=2), axis=1)
        means.append(X[rng.choice(n, p=distances / distances.sum())].copy())
    means = np.array(means)
    # Ten nearest-center updates improve the starting point for EM.
    for _ in range(10):
        labels = np.argmin(np.sum((X[:, None, :] - means) ** 2, axis=2), axis=1)
        for j in range(k):
            if np.any(labels == j):
                means[j] = X[labels == j].mean(axis=0)
    covariance = np.cov(X, rowvar=False) + reg * np.eye(d)
    return np.full(k, 1 / k), means, np.repeat(covariance[None, :, :], k, axis=0)


# 2. E-step: compute responsibilities and total log-likelihood.
def e_step(X, weights, means, covariances):
    n, d = X.shape
    log_joint = np.empty((n, len(weights)))
    for j, (weight, mean, cov) in enumerate(zip(weights, means, covariances)):
        sign, log_det = np.linalg.slogdet(cov)
        if sign <= 0:
            raise FloatingPointError('Invalid covariance')
        diff = X - mean
        mahalanobis = np.einsum('ni,ij,nj->n', diff, np.linalg.inv(cov), diff)
        log_joint[:, j] = np.log(weight) - 0.5 * (d * np.log(2 * np.pi) + log_det + mahalanobis)
    # Subtract the maximum before exponentiation to avoid underflow.
    maximum = log_joint.max(axis=1, keepdims=True)
    log_total = maximum + np.log(np.exp(log_joint - maximum).sum(axis=1, keepdims=True))
    responsibilities = np.exp(log_joint - log_total)
    return responsibilities, float(log_total.sum())


# 3. M-step: update mixture weights, means and full covariances.
def m_step(X, responsibilities, reg=1e-6):
    n, d = X.shape
    counts = responsibilities.sum(axis=0)
    if np.any(counts < 1e-10):
        raise FloatingPointError('Empty component')
    weights = counts / n
    means = responsibilities.T @ X / counts[:, None]
    covariances = []
    for j, mean in enumerate(means):
        diff = X - mean
        cov = (diff.T * responsibilities[:, j]) @ diff / counts[j]
        covariances.append((cov + cov.T) / 2 + reg * np.eye(d))
    return weights, means, np.array(covariances)


# 4. Alternate the two steps until relative likelihood change is small.
def fit_once(X, k, seed, tol=1e-7, max_iter=1000, reg=1e-6):
    weights, means, covs = initialize(X, k, np.random.default_rng(seed), reg)
    r, ll = e_step(X, weights, means, covs)
    history = [ll]
    converged = False
    for _ in range(max_iter):
        weights, means, covs = m_step(X, r, reg)
        r, ll = e_step(X, weights, means, covs)
        previous = history[-1]
        history.append(ll)
        if abs(ll - previous) <= tol * max(1., abs(previous)):
            converged = True
            break
    # Sort components by their first mean coordinate for consistent labels.
    order = np.argsort(means[:, 0])
    assert np.allclose(r.sum(axis=1), 1) and np.allclose(weights.sum(), 1)
    assert np.all(np.linalg.eigvalsh(covs) > 0)
    return dict(k=k, seed=seed, weights=weights[order], means=means[order],
                covs=covs[order], r=r[:, order], history=np.array(history),
                ll=ll, converged=converged, iterations=len(history) - 1)


# 5. Try several initializations; evaluate the best converged model.
def fit(X, k, restarts=12, seed=42, tol=1e-7, max_iter=1000):
    runs = []
    for j in range(restarts):
        try:
            runs.append(fit_once(X, k, seed + j, tol, max_iter))
        except FloatingPointError as error:
            print(f'K={k}, restart {j}: {error}')
    converged = [run for run in runs if run['converged']]
    if not converged:
        raise RuntimeError(f'No converged run for K={k}')
    best = max(converged, key=lambda run: run['ll'])
    n, d = X.shape
    p = (k - 1) + k * d + k * d * (d + 1) // 2
    best.update(p=p, aic=2 * p - 2 * best['ll'],
                bic=p * np.log(n) - 2 * best['ll'], runs=runs)
    return best


# 6. Run the assignment experiment. Reporting is kept separate from EM.
def main():
    from gmm_report import save_results

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=Path(__file__).with_name('FAA_AEDT_data.csv'))
    parser.add_argument('--out', type=Path, default=Path(__file__).with_name('results'))
    parser.add_argument('--restarts', type=int, default=12)
    args = parser.parse_args()
    start = time.perf_counter()
    X = np.loadtxt(args.data, delimiter=',', skiprows=1)
    assert X.shape == (1000, 2) and np.isfinite(X).all()
    models = [fit(X, k, args.restarts) for k in (2, 3, 4, 5)]
    best = min(models, key=lambda model: model['bic'])
    strict = fit_once(X, best['k'], best['seed'], tol=1e-10, max_iter=5000)
    save_results(X, models, best, strict, args.out)
    elapsed = time.perf_counter() - start
    print(f"BIC-optimal K={best['k']}; elapsed={elapsed:.3f}s")
    (args.out / 'runtime.txt').write_text(
        f'End-to-end runtime (including plots and stricter check): {elapsed:.3f} seconds\n')
    assert elapsed < 300, 'Runtime exceeds five-minute limit on this machine'


if __name__ == '__main__':
    main()
