"""Full-covariance GMM with EM from scratch; NumPy for linear algebra only.
AI assistance: OpenAI ChatGPT (GPT-6.2), draft implementation and validation.
"""
from pathlib import Path
import argparse, csv, time
import numpy as np


def logsumexp(a, axis=1):
    m = np.max(a, axis=axis, keepdims=True)
    return np.squeeze(m + np.log(np.sum(np.exp(a-m), axis=axis, keepdims=True)), axis=axis)


def initialize(X, k, rng, reg):
    n, d = X.shape
    means = [X[rng.integers(n)].copy()]
    for _ in range(1, k):
        distances = np.min(np.sum((X[:,None,:]-np.array(means)[None,:,:])**2, axis=2), axis=1)
        means.append(X[rng.choice(n, p=distances/distances.sum())].copy())
    # A few Lloyd steps provide a better starting point; not a GMM library.
    means = np.array(means)
    for _ in range(10):
        labels = np.argmin(np.sum((X[:,None,:]-means[None,:,:])**2,axis=2),axis=1)
        for j in range(k):
            if np.any(labels==j): means[j] = X[labels==j].mean(axis=0)
    cov = np.cov(X,rowvar=False) + reg*np.eye(d)
    return np.full(k,1/k), means, np.repeat(cov[None,:,:],k,axis=0)


def e_step(X, weights, means, covariances):
    n,d=X.shape
    k=len(weights)
    log_joint=np.empty((n,k))
    for j in range(k):
        cov=covariances[j]
        sign, logdet=np.linalg.slogdet(cov)
        if sign<=0: raise FloatingPointError('Non-positive covariance determinant')
        diff=X-means[j]
        # solve via inverse of tiny (2x2) positive definite covariance
        mahal=np.einsum('ni,ij,nj->n',diff,np.linalg.inv(cov),diff)
        log_joint[:,j]=np.log(weights[j])-0.5*(d*np.log(2*np.pi)+logdet+mahal)
    log_norm=logsumexp(log_joint)
    return np.exp(log_joint-log_norm[:,None]), float(log_norm.sum())


def m_step(X, r, reg):
    n,d=X.shape
    nk=r.sum(axis=0)
    if np.any(nk<1e-10): raise FloatingPointError('Empty component')
    weights=nk/n
    means=r.T@X/nk[:,None]
    covs=[]
    for j in range(len(nk)):
        diff=X-means[j]
        cov=(diff.T*r[:,j])@diff/nk[j]
        covs.append((cov+cov.T)/2+reg*np.eye(d))
    return weights, means, np.array(covs)


def fit_once(X,k,seed,tol=1e-7,max_iter=1000,reg=1e-6):
    params=initialize(X,k,np.random.default_rng(seed),reg)
    r,ll=e_step(X,*params)
    history=[ll]
    converged=False
    for i in range(max_iter):
        params=m_step(X,r,reg)
        r,ll=e_step(X,*params)
        history.append(ll)
        improvement=ll-history[-2]
        if abs(improvement)<=tol*max(1.,abs(history[-2])):
            converged=True
            break
    # Reorder by first mean coordinate so labels are reproducible.
    order=np.argsort(params[1][:,0]); params=tuple(p[order] for p in params); r=r[:,order]
    assert np.allclose(r.sum(axis=1),1) and np.allclose(params[0].sum(),1)
    assert np.all(np.linalg.eigvalsh(params[2])>0)
    return dict(k=k,seed=seed,weights=params[0],means=params[1],covs=params[2],r=r,history=np.array(history),ll=ll,converged=converged,iterations=len(history)-1)


def fit(X,k,restarts=12,seed=42,tol=1e-7,max_iter=1000):
    runs=[]
    for j in range(restarts):
        try: runs.append(fit_once(X,k,seed+j,tol,max_iter))
        except FloatingPointError as exc: print(f'K={k}, restart {j}: {exc}')
    converged=[r for r in runs if r['converged']]
    if not converged: raise RuntimeError(f'No converged run for K={k}')
    best=max(converged,key=lambda r:r['ll'])
    n,d=X.shape
    p=(k-1)+k*d+k*d*(d+1)//2
    best.update(p=p,aic=2*p-2*best['ll'],bic=p*np.log(n)-2*best['ll'],runs=runs)
    return best


def write_csv(path, rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--data',type=Path,default=Path(__file__).with_name('FAA_AEDT_data.csv')); parser.add_argument('--out',type=Path,default=Path(__file__).with_name('results')); parser.add_argument('--restarts',type=int,default=12); args=parser.parse_args()
    start=time.perf_counter(); X=np.loadtxt(args.data,delimiter=',',skiprows=1); out=args.out; out.mkdir(parents=True,exist_ok=True)
    assert X.shape==(1000,2) and np.isfinite(X).all(), 'Expected 1000 finite two-dimensional records'
    models=[]; metrics=[]; restart_rows=[]
    for k in (2,3,4,5):
        m=fit(X,k,args.restarts); models.append(m)
        changes=np.diff(m['history']); confident=m['r'].max(axis=1)
        row=dict(K=k,log_likelihood=m['ll'],parameters=m['p'],AIC=m['aic'],BIC=m['bic'],iterations=m['iterations'],converged=m['converged'],seed=m['seed'],final_abs_change=abs(changes[-1]),min_increment=changes.min(),converged_restarts=sum(r['converged'] for r in m['runs']),total_restarts=len(m['runs']),mean_max_posterior=confident.mean())
        metrics.append(row); print(row)
        for run in m['runs']: restart_rows.append(dict(K=k,seed=run['seed'],log_likelihood=run['ll'],iterations=run['iterations'],converged=run['converged']))
        write_csv(out/f'convergence_k{k}.csv',[dict(iteration=i,log_likelihood=v) for i,v in enumerate(m['history'])])
    write_csv(out/'model_selection.csv',metrics); write_csv(out/'restarts.csv',restart_rows)
    best=min(models,key=lambda m:m['bic']); k=best['k']; labels=best['r'].argmax(axis=1)
    write_csv(out/'cluster_parameters.csv',[dict(cluster=j+1,weight=best['weights'][j],mean_x1=best['means'][j,0],mean_x2=best['means'][j,1],cov_x1_x1=best['covs'][j,0,0],cov_x1_x2=best['covs'][j,0,1],cov_x2_x2=best['covs'][j,1,1],hard_count=int((labels==j).sum())) for j in range(k)])
    np.savetxt(out/'cluster_assignments.csv',np.column_stack([X,labels+1,best['r']]),delimiter=',',header='x1,x2,cluster,'+','.join(f'p_cluster_{i+1}' for i in range(k)),comments='')
    # Extended run checks whether a stricter tolerance materially changes the solution.
    extended=fit_once(X,k,best['seed'],tol=1e-10,max_iter=5000)
    write_csv(out/'convergence_validation.csv',[dict(K=k,standard_iterations=best['iterations'],strict_iterations=extended['iterations'],standard_LL=best['ll'],strict_LL=extended['ll'],LL_difference=extended['ll']-best['ll'],label_agreement=np.mean(labels==extended['r'].argmax(axis=1)),strict_converged=extended['converged'])])
    make_plots(X,models,best,out)
    elapsed=time.perf_counter()-start
    print(f'BIC-optimal K={k}; elapsed={elapsed:.3f}s'); (out/'runtime.txt').write_text(f'End-to-end runtime (including plots and stricter check): {elapsed:.3f} seconds\n')
    assert elapsed<300, 'Runtime exceeds five-minute limit on this machine'


def make_plots(X,models,best,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse
    colors=['#007F86','#E28C28','#5456B4','#C14F70','#62964A']
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','axes.grid':True,'grid.alpha':.18,'axes.labelcolor':'#26354A','axes.titlecolor':'#142C44','savefig.bbox':'tight'})
    def scatter(ax,m):
        y=m['r'].argmax(axis=1)
        for j in range(m['k']):
            ax.scatter(*X[y==j].T,s=11,alpha=.65,color=colors[j],label=f'C{j+1}',linewidths=0)
            vals,vecs=np.linalg.eigh(m['covs'][j]); angle=np.degrees(np.arctan2(vecs[1,1],vecs[0,1]))
            # 95% probability contour for a bivariate Gaussian (chi-square 2 df).
            ax.add_patch(Ellipse(m['means'][j],2*np.sqrt(5.991*vals[1]),2*np.sqrt(5.991*vals[0]),angle=angle,fill=False,color=colors[j],lw=2))
            ax.scatter(*m['means'][j],marker='X',s=85,color=colors[j],edgecolors='white',linewidths=1.2,zorder=5)
        ax.set(xlabel='x1',ylabel='x2',title=f"K = {m['k']}",xlim=(-10,10),ylim=(-12,9)); ax.set_aspect('equal'); ax.legend(loc='upper right',fontsize=8,frameon=False,ncol=2)
    fig,ax=plt.subplots(figsize=(6,5)); ax.scatter(*X.T,s=12,color='#24465E',alpha=.65,linewidths=0); ax.set(xlabel='x1',ylabel='x2',title='FAA AEDT dataset | 1,000 observations'); ax.set_aspect('equal'); fig.savefig(out/'raw_data.png',dpi=180); plt.close(fig)
    fig,axs=plt.subplots(2,2,figsize=(10,9),constrained_layout=True)
    for ax,m in zip(axs.flat,models): scatter(ax,m)
    fig.savefig(out/'clusters_all.png',dpi=180); plt.close(fig)
    for m in models:
        fig,ax=plt.subplots(figsize=(5.4,5)); scatter(ax,m); fig.savefig(out/f"clusters_k{m['k']}.png",dpi=180); plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
    for ax,key in zip(axs,['aic','bic']):
        ks=[m['k'] for m in models]; vals=[m[key] for m in models]; ax.plot(ks,vals,'o-',color='#007F86',lw=2); i=int(np.argmin(vals)); ax.scatter(ks[i],vals[i],s=100,color='#E28C28',zorder=5); ax.set(xlabel='Number of components K',ylabel=key.upper(),xticks=ks,title=f'{key.upper()} (lower is better)')
        for xx,yy in zip(ks,vals): ax.annotate(f'{yy:.1f}',(xx,yy),xytext=(0,8),textcoords='offset points',ha='center',fontsize=9)
        ax.margins(y=.2)
    fig.savefig(out/'model_selection.png',dpi=180); plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
    for m,c in zip(models,colors):
        h=m['history']; axs[0].plot(h,label=f"K={m['k']}",color=c,lw=2); axs[1].semilogy(np.arange(1,len(h)),np.maximum(abs(np.diff(h)),1e-14),label=f"K={m['k']}",color=c,lw=1.7)
    axs[0].set(xlabel='EM iteration',ylabel='Total log-likelihood',title='Likelihood improves and plateaus'); axs[1].set(xlabel='EM iteration',ylabel='Absolute change in likelihood',title='Update size approaches zero');
    for ax in axs: ax.legend(frameon=False)
    fig.savefig(out/'convergence.png',dpi=180); plt.close(fig)

if __name__=='__main__': main()
