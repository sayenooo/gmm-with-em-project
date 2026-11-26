from pathlib import Path
from time import perf_counter
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent


def e_step(X, weights, means, covs):
    log_prob = np.zeros((len(X), len(weights)))
    for j in range(len(weights)):
        diff = X - means[j]
        log_det = np.linalg.slogdet(covs[j])[1]
        distance = np.sum((diff @ np.linalg.inv(covs[j])) * diff, axis=1)
        log_prob[:, j] = np.log(weights[j]) - 0.5 * (
            X.shape[1] * np.log(2 * np.pi) + log_det + distance)
    # Stable normalization of posterior probabilities.
    largest = log_prob.max(axis=1, keepdims=True)
    prob = np.exp(log_prob - largest)
    total = prob.sum(axis=1, keepdims=True)
    return prob / total, float(np.sum(largest + np.log(total)))


def m_step(X, r):
    counts = r.sum(axis=0)
    if np.any(counts < 1e-10):
        raise FloatingPointError('Empty component')
    weights = counts / len(X)
    means = (r.T @ X) / counts[:, None]
    covs = []
    for j in range(len(weights)):
        diff = X - means[j]
        cov = (diff.T * r[:, j]) @ diff / counts[j]
        covs.append(cov + 1e-6 * np.eye(X.shape[1]))
    return weights, means, np.array(covs)


def gmm(X, k, seed, tol=1e-7, max_iter=2000):
    rng = np.random.default_rng(seed)
    weights = np.ones(k) / k
    means = X[rng.choice(len(X), k, replace=False)].copy()
    covs = np.array([np.cov(X.T) + 1e-6 * np.eye(X.shape[1])] * k)
    r, ll = e_step(X, weights, means, covs)
    history = [ll]
    converged = False
    for _ in range(max_iter):
        weights, means, covs = m_step(X, r)
        r, ll = e_step(X, weights, means, covs)
        history.append(ll)
        if abs(history[-1] - history[-2]) <= tol * max(1, abs(history[-2])):
            converged = True
            break
    assert np.allclose(r.sum(axis=1), 1)
    assert np.isclose(weights.sum(), 1)
    assert np.all(np.linalg.eigvalsh(covs) > 0)
    return r, history, converged


def main():
    start = perf_counter()
    X = np.loadtxt(ROOT / 'FAA_AEDT_data.csv', delimiter=',', skiprows=1)
    assert X.shape == (1000, 2) and np.isfinite(X).all()
    out = ROOT / 'results'
    out.mkdir(exist_ok=True)
    rows = []
    models = {}
    for k in (2, 3, 4, 5):
        # EM can reach local optima: keep the best converged start.
        runs = []
        for seed in range(42, 54):
            try:
                r, history, converged = gmm(X, k, seed)
            except FloatingPointError:
                continue
            if converged:
                runs.append((history[-1], seed, r, history))
        if not runs:
            raise RuntimeError(f'No converged run for K={k}')
        ll, seed, r, history = max(runs, key=lambda run: run[0])
        d = X.shape[1]
        p = k - 1 + k * d + k * d * (d + 1) // 2
        aic = 2 * p - 2 * ll
        bic = p * np.log(len(X)) - 2 * ll
        rows.append([k, ll, aic, bic, len(history)-1, seed, len(runs),
                     abs(history[-1]-history[-2]), np.min(np.diff(history))])
        models[k] = (seed, r, history)
        print(f'K={k}: LL={ll:.4f}, AIC={aic:.2f}, BIC={bic:.2f}, '
              f'iterations={len(history)-1}, converged starts={len(runs)}/12')
        plt.figure()
        plt.scatter(X[:, 0], X[:, 1], c=r.argmax(axis=1), s=12, cmap='tab10')
        plt.xlabel('x1')
        plt.ylabel('x2')
        plt.title(f'GMM clustering: K={k}')
        plt.savefig(out / f'clusters_k{k}.png', dpi=160, bbox_inches='tight')
        plt.close()
        np.savetxt(out / f'likelihood_k{k}.csv', history, delimiter=',',
                   header='log_likelihood', comments='')
    np.savetxt(out / 'model_selection.csv', rows, delimiter=',',
               header='K,log_likelihood,AIC,BIC,iterations,seed,converged_starts,final_change,min_increment', comments='')
    plt.figure()
    for k, (_, _, history) in models.items():
        plt.plot(history, label=f'K={k}')
    plt.xlabel('EM iteration')
    plt.ylabel('Log-likelihood')
    plt.legend()
    plt.savefig(out / 'convergence.png', dpi=160, bbox_inches='tight')
    plt.close()
    table = np.array(rows)
    plt.figure()
    plt.plot(table[:, 0], table[:, 2], 'o-', label='AIC')
    plt.plot(table[:, 0], table[:, 3], 'o-', label='BIC')
    plt.xticks([2, 3, 4, 5])
    plt.xlabel('K')
    plt.ylabel('Criterion (lower is better)')
    plt.legend()
    plt.savefig(out / 'model_selection.png', dpi=160, bbox_inches='tight')
    plt.close()
    best_k = int(min(rows, key=lambda row: row[3])[0])
    seed, r, history = models[best_k]
    strict_r, strict_history, strict_ok = gmm(X, best_k, seed, tol=1e-10, max_iter=5000)
    summary = (f'Best K by BIC: {best_k}\n'
               f'Strict convergence: {strict_ok}\n'
               f'Iterations: {len(history)-1} -> {len(strict_history)-1}\n'
               f'LL improvement: {strict_history[-1]-history[-1]:.8f}\n'
               f'Unchanged labels: {np.sum(r.argmax(axis=1)==strict_r.argmax(axis=1))}/{len(X)}\n'
               f'Runtime: {perf_counter()-start:.3f} seconds\n')
    print(summary)
    (out / 'summary.txt').write_text(summary)


if __name__ == '__main__':
    main()
