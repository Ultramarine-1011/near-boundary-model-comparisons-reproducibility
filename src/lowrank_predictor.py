"""Historical-only squared-loss low-rank surrogate; not PULSE's logistic MF.

No target responses enter basis estimation or hyperparameter selection.
Target predictions use only a charged pilot and remain frozen thereafter.
"""
import numpy as np


def basis_from_history(scores, max_rank=32, seed=183):
    x=np.asarray(scores,float)
    if x.ndim!=2 or not np.isfinite(x).all():raise ValueError('history')
    mean=x.mean(axis=0);centered=x-mean
    rank=min(max_rank+8,min(x.shape))
    rng=np.random.default_rng(seed)
    q,_=np.linalg.qr(centered@rng.normal(size=(x.shape[1],rank)))
    for _ in range(2):
        right,_=np.linalg.qr(centered.T@q)
        q,_=np.linalg.qr(centered@right)
    _,_,vt=np.linalg.svd(q.T@centered,full_matrices=False)
    # Unit average squared feature scale, including the intercept.
    features=np.column_stack([np.ones(x.shape[1]),vt[:max_rank].T*np.sqrt(x.shape[1])])
    return mean,features


def predict(mean,features,pilot,observed,rank,ridge):
    pilot=np.asarray(pilot,int);observed=np.asarray(observed,float)
    if len(pilot)!=len(observed) or len(np.unique(pilot))!=len(pilot):raise ValueError('pilot')
    f=features[:,:rank+1];a=f[pilot]
    coef=np.linalg.solve(a.T@a+ridge*np.eye(rank+1),a.T@(observed-mean[pilot]))
    return np.clip(mean+f@coef,0,1)


def select_hyperparameters(mean,features,validation,pilot_size=64,seed=194):
    rng=np.random.default_rng(seed);n=len(mean)
    pilots=[rng.permutation(n)[:pilot_size] for _ in validation]
    candidates=[]
    for rank in (0,4,8,16,32):
        if rank+1>features.shape[1]:continue
        for ridge in (.1,1.,10.,100.):
            losses=[]
            for y,pilot in zip(validation,pilots):
                p=predict(mean,features,pilot,y[pilot],rank,ridge)
                held=np.ones(n,bool);held[pilot]=False
                losses.append(float(np.mean((p[held]-y[held])**2)))
            candidates.append(dict(rank=rank,ridge=ridge,mse=float(np.mean(losses))))
    best=min(candidates,key=lambda c:c['mse'])
    # Residual weights use historical validation responses only.
    errors=[]
    for y,pilot in zip(validation,pilots):
        p=predict(mean,features,pilot,y[pilot],best['rank'],best['ridge'])
        residual=(p-y)**2;residual[pilot]=np.nan;errors.append(residual)
    weights=np.sqrt(np.maximum(.0025,np.nanmean(errors,axis=0)))
    return best,weights,candidates
