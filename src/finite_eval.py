"""Design-based finite-population confidence sequences, adapted from WS-R (2020).

All arrays returned are indexed after observations 1,...,N. No test-score data
outside the revealed prefix is used. Labels use practical superiority.
"""
from __future__ import annotations
import math
import numpy as np

BET_GRID = np.array([0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8])

def betting_decision(d, epsilon, alpha=.05):
    """Existing bounded betting factors, applied to four directional hypotheses.

    Each test is level alpha/2. At a given true label only two rejection events
    can produce a wrong label (see THEORY). This is a test, not a returned CS.
    """
    d=validate(d,alpha);label(0.,epsilon)
    x=(d+1)/2;N=len(x);t=np.arange(1,N+1)
    s=np.cumsum(x);prev=np.r_[0.,s[:-1]]
    rejects={}
    for bound in (-1,1):
        mu=(1+bound*epsilon)/2;m=(N*mu-prev)/(N-t+1)
        feasible=(m>=0)&(m<=1)
        for sign in (-1,1):
            increments=sign*BET_GRID[:,None]*(x-np.clip(m,0,1))
            logs=np.cumsum(np.where(feasible,np.log1p(increments),0.),axis=1)
            top=np.max(logs,axis=0)
            logmean=top+np.log(np.mean(np.exp(logs-top),axis=0))
            impossible=(s/N>mu+1e-12) if sign==1 else ((s+N-t)/N<mu-1e-12)
            rejects[bound,sign]=np.maximum.accumulate((logmean>=math.log(2/alpha))|impossible)
    a=rejects[1,1];b=rejects[-1,-1];e=rejects[-1,1]&rejects[1,-1]
    labels=np.full(N,'C',dtype='<U1')
    labels[a&~b&~e]='A';labels[b&~a&~e]='B';labels[e&~a&~b]='E'
    mean=math.fsum(map(float,d))/N;truth=label(mean,epsilon);labels[-1]=truth
    j=int(np.flatnonzero(labels!='C')[0])
    return dict(n=j+1,N=N,decision=str(labels[j]),truth=truth,error=int(labels[j]!=truth),cost=float(j+1),delta=mean)

def validate(x, alpha):
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or not len(x) or not np.isfinite(x).all():
        raise ValueError('finite nonempty one-dimensional observations required')
    if np.any((x < -1) | (x > 1)) or not 0 < alpha < 1:
        raise ValueError('bounds or alpha invalid')
    return x

def label(delta, epsilon):
    if not 0 <= epsilon < 1: raise ValueError('epsilon must be in [0,1)')
    return 'A' if delta > epsilon else 'B' if delta < -epsilon else 'E'

def decide(lo, hi, epsilon):
    if lo > hi: return 'C'  # empty CS: do not certify vacuous set inclusion
    if lo > epsilon: return 'A'
    if hi < -epsilon: return 'B'
    if lo >= -epsilon and hi <= epsilon: return 'E'
    return 'C'

def cs_path(d, alpha=0.05, method='eb_grid', completion=True, intersect=True):
    d = validate(d, alpha); n = len(d)
    x = (d + 1) / 2
    t = np.arange(1, n+1, dtype=float)
    s = np.cumsum(x); prev = np.r_[0., s[:-1]]
    rem = n-t+1
    a = np.cumsum(n/rem)
    z = np.cumsum(x + prev/rem)
    prediction = np.r_[0.5, np.clip(z[:-1]/a[:-1], 0, 1)]
    v = np.cumsum((x-prediction)**2)
    if method in ('eb_grid','hoeffding_grid'):
        lam = BET_GRID[:,None]
        penalty = np.log(2*len(BET_GRID)/alpha)
        cumulant = (-np.log1p(-lam)-lam)*v if method=='eb_grid' else lam**2*t/8
        width = np.min((penalty+cumulant)/(lam*a),axis=0)
        center = z/a
    elif method == 'eb_predictable':
        # Eq. 3.13 form; predictable variance proxy and pre-observation bets.
        variance = np.r_[0.25, (0.25+v[:-1])/t[:-1]]
        lam = np.minimum(0.5,np.sqrt(2*np.log(2/alpha)/(variance*t*np.log(t+1))))
        denom = np.cumsum(lam*n/rem)
        center = np.cumsum(lam*(x+prev/rem))/denom
        width = (np.log(2/alpha)+np.cumsum((-np.log1p(-lam)-lam)*(x-prediction)**2))/denom
    elif method == 'serfling_spending':
        looks=np.unique(np.r_[np.ceil(1.5**np.arange(0,math.ceil(math.log(n,1.5))+1)).astype(int),n])
        looks=looks[looks<=n]; L=len(looks)
        rho=1-(t-1)/n
        # Serfling's fixed-n bound, Bonferroni over prespecified looks.
        raw=np.sqrt(rho*np.log(2*L/alpha)/(2*t))
        center=s/t; width=np.full(n,np.inf);width[looks-1]=raw[looks-1]
    elif method == 'normal_peeking':
        center=s/t
        var=np.maximum(0,(np.cumsum(x*x)-s*s/t)/np.maximum(t-1,1))
        from statistics import NormalDist
        width=NormalDist().inv_cdf(1-alpha/2)*np.sqrt(var/t*(n-t)/max(n-1,1))
        width[:min(19,n)]=np.inf
    elif method == 'completion':
        center=np.full(n,0.5);width=np.full(n,np.inf)
    else: raise ValueError(method)
    lo=np.maximum(0,center-width);hi=np.minimum(1,center+width)
    if completion:
        lo=np.maximum(lo,s/n);hi=np.minimum(hi,(s+n-t)/n)
    if intersect:
        lo=np.maximum.accumulate(lo);hi=np.minimum.accumulate(hi)
    # On a past coverage failure the running intersection may be empty.
    # Census is exact and supersedes it, rather than asserting coverage anew.
    lo[-1]=hi[-1]=s[-1]/n
    # Conservative roundoff padding; final exact-score mean is handled separately.
    return 2*lo-1-1e-12, 2*hi-1+1e-12

def stop_from_path(d, lo, hi, epsilon, cost=None):
    d=np.asarray(d);n=len(d)
    valid=lo<=hi
    codes=np.full(n,'C',dtype='<U1')
    codes[valid & (lo>epsilon)]='A'
    codes[valid & (hi<-epsilon)]='B'
    codes[valid & (lo>=-epsilon) & (hi<=epsilon)]='E'
    # Use direct original-scale mean at census, avoiding affine cancellation.
    mean=math.fsum(map(float,d))/n
    codes[-1]=label(mean,epsilon)
    idx=int(np.flatnonzero(codes!='C')[0])
    truth=label(mean,epsilon)
    return dict(n=idx+1,N=n,decision=str(codes[idx]),truth=truth,error=int(codes[idx]!=truth),
                coverage_failure=int(np.any((lo>np.mean(d)+1e-12)|(hi<np.mean(d)-1e-12))),
                cost=float(idx+1 if cost is None else np.sum(cost[:idx+1])),
                empty_path=int(np.any(lo>hi)),delta=float(np.mean(d)))

def stratified_replay(groups, epsilon, alpha, seed, allocation='proportional', costs=None):
    """Adaptive interleaving of independent uniform within-stratum permutations.

    Paths are precomputed solely as an optimization; allocation reads only each
    stratum's current revealed prefix. Total lengths and costs are known metadata.
    """
    rng=np.random.default_rng(seed);h=len(groups)
    groups=[validate(g,alpha) for g in groups]
    sizes=np.array([len(g) for g in groups]);N=int(sizes.sum());weights=sizes/N
    streams=[rng.permutation(g) for g in groups]
    paths=[cs_path(g,alpha/h) for g in streams]
    counts=np.zeros(h,dtype=int);sums=np.zeros(h);sumsq=np.zeros(h)
    lows=np.full(h,-1.);highs=np.full(h,1.)
    costs=np.ones(h) if costs is None else np.asarray(costs,float)
    if np.any(costs<=0):raise ValueError('costs must be positive')
    true=float(sum(np.sum(g) for g in groups)/N);spent=0.;fail=False
    for t in range(1,N+1):
        available=counts<sizes
        if allocation=='proportional': priority=weights/(counts+1)
        elif allocation=='neyman':
            variance=np.maximum(0,(sumsq-sums*sums/np.maximum(counts,1))/np.maximum(counts-1,1))
            sd=np.sqrt((counts*variance+1)/(counts+1))
            priority=weights*sd/(np.sqrt(costs)*(counts+1))
        else:raise ValueError(allocation)
        k=int(np.argmax(np.where(available,priority,-np.inf)))
        j=counts[k];obs=streams[k][j];counts[k]+=1
        sums[k]+=obs;sumsq[k]+=obs*obs;spent+=costs[k]
        lows[k]=paths[k][0][j];highs[k]=paths[k][1][j]
        lower=float(weights@lows);upper=float(weights@highs)
        fail=fail or lower>true+1e-12 or upper<true-1e-12
        verdict=decide(lower,upper,epsilon)
        if np.any(lows>highs):verdict='C'
        if t==N:verdict=label(true,epsilon)
        if verdict!='C':
            return dict(n=t,N=N,decision=verdict,truth=label(true,epsilon),error=int(verdict!=label(true,epsilon)),
                        coverage_failure=int(fail),cost=spent,delta=true,counts=counts.tolist())
    raise AssertionError('must stop by census')
