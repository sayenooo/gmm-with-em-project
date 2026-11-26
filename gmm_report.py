"""Output utilities: CSV evidence and figures. No GMM fitting is done here."""
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save_results(X, models, best, strict, out):
    out.mkdir(parents=True, exist_ok=True)
    metrics, restarts = [], []
    for m in models:
        changes = np.diff(m['history'])
        row = dict(K=m['k'], log_likelihood=m['ll'], parameters=m['p'],
                   AIC=m['aic'], BIC=m['bic'], iterations=m['iterations'],
                   converged=m['converged'], seed=m['seed'],
                   final_abs_change=abs(changes[-1]), min_increment=changes.min(),
                   converged_restarts=sum(r['converged'] for r in m['runs']),
                   total_restarts=len(m['runs']), mean_max_posterior=m['r'].max(axis=1).mean())
        metrics.append(row)
        print(f"K={m['k']}: LL={m['ll']:.4f}, AIC={m['aic']:.2f}, BIC={m['bic']:.2f}, iterations={m['iterations']}")
        restarts.extend(dict(K=m['k'], seed=r['seed'], log_likelihood=r['ll'],
                             iterations=r['iterations'], converged=r['converged']) for r in m['runs'])
        write_csv(out / f"convergence_k{m['k']}.csv", [dict(iteration=i, log_likelihood=v)
                                                       for i, v in enumerate(m['history'])])
    write_csv(out / 'model_selection.csv', metrics)
    write_csv(out / 'restarts.csv', restarts)
    k = best['k']
    labels = best['r'].argmax(axis=1)
    write_csv(out / 'cluster_parameters.csv', [dict(cluster=j+1, weight=best['weights'][j],
        mean_x1=best['means'][j, 0], mean_x2=best['means'][j, 1],
        cov_x1_x1=best['covs'][j, 0, 0], cov_x1_x2=best['covs'][j, 0, 1],
        cov_x2_x2=best['covs'][j, 1, 1], hard_count=int((labels == j).sum())) for j in range(k)])
    np.savetxt(out / 'cluster_assignments.csv', np.column_stack([X, labels+1, best['r']]),
               delimiter=',', header='x1,x2,cluster,' + ','.join(f'p_cluster_{j+1}' for j in range(k)), comments='')
    write_csv(out / 'convergence_validation.csv', [dict(K=k, standard_iterations=best['iterations'],
        strict_iterations=strict['iterations'], standard_LL=best['ll'], strict_LL=strict['ll'],
        LL_difference=strict['ll']-best['ll'], label_agreement=np.mean(labels == strict['r'].argmax(axis=1)),
        strict_converged=strict['converged'])])
    make_plots(X, models, out)


def make_plots(X, models, out):
    colors = ['#007F86', '#E28C28', '#5456B4', '#C14F70', '#62964A']
    plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.grid': True, 'grid.alpha': .18, 'savefig.bbox': 'tight'})

    def save(fig, filename):
        fig.savefig(out / filename, dpi=180)
        plt.close(fig)

    def scatter(ax, model):
        labels = model['r'].argmax(axis=1)
        for j in range(model['k']):
            ax.scatter(*X[labels == j].T, s=11, alpha=.65, color=colors[j], label=f'C{j+1}', linewidths=0)
            values, vectors = np.linalg.eigh(model['covs'][j])
            angle = np.degrees(np.arctan2(vectors[1, 1], vectors[0, 1]))
            # 95% probability contour for a two-dimensional Gaussian.
            width, height = 2 * np.sqrt(5.991 * values[::-1])
            ax.add_patch(Ellipse(model['means'][j], width, height, angle=angle, fill=False, color=colors[j], lw=2))
            ax.scatter(*model['means'][j], marker='X', s=85, color=colors[j], edgecolors='white', zorder=5)
        ax.set(xlabel='x1', ylabel='x2', title=f"K = {model['k']}", xlim=(-10, 10), ylim=(-12, 9))
        ax.set_aspect('equal')
        ax.legend(loc='upper right', fontsize=8, frameon=False, ncol=2)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(*X.T, s=12, color='#24465E', alpha=.65, linewidths=0)
    ax.set(xlabel='x1', ylabel='x2', title='FAA AEDT dataset | 1,000 observations')
    ax.set_aspect('equal')
    save(fig, 'raw_data.png')
    fig, axes = plt.subplots(2, 2, figsize=(10, 9), constrained_layout=True)
    for ax, model in zip(axes.flat, models):
        scatter(ax, model)
    save(fig, 'clusters_all.png')
    for model in models:
        fig, ax = plt.subplots(figsize=(5.4, 5))
        scatter(ax, model)
        save(fig, f"clusters_k{model['k']}.png")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    for ax, key in zip(axes, ['aic', 'bic']):
        ks = [m['k'] for m in models]
        values = [m[key] for m in models]
        ax.plot(ks, values, 'o-', color=colors[0])
        i = int(np.argmin(values))
        ax.scatter(ks[i], values[i], color=colors[1], s=100, zorder=5)
        ax.set(xlabel='Number of components K', ylabel=key.upper(), xticks=ks, title=f'{key.upper()} (lower is better)')
        for k, value in zip(ks, values):
            ax.annotate(f'{value:.1f}', (k, value), xytext=(0, 8), textcoords='offset points', ha='center', fontsize=9)
        ax.margins(y=.2)
    save(fig, 'model_selection.png')
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    for model, color in zip(models, colors):
        h = model['history']
        axes[0].plot(h, label=f"K={model['k']}", color=color)
        axes[1].semilogy(np.arange(1, len(h)), np.maximum(abs(np.diff(h)), 1e-14), color=color, label=f"K={model['k']}")
    axes[0].set(xlabel='EM iteration', ylabel='Total log-likelihood', title='Likelihood convergence')
    axes[1].set(xlabel='EM iteration', ylabel='Absolute likelihood change', title='Update size approaches zero')
    for ax in axes:
        ax.legend(frameon=False)
    save(fig, 'convergence.png')
