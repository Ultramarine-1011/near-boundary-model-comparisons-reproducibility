"""Union-intersection exponential tests for a weighted finite mean.

Specialization of established stratified testing: solve nuisance optimization
exactly by fractional knapsack. This avoids separate alpha/H intervals.
"""
import math
import numpy as np
from finite_eval import BET_GRID,validate,label

def extreme(a,w,lo,hi,bound,maximize):
    """Optimize a @ mu over a box and the boundary w @ mu = bound.

    Caller handles a globally infeasible null and clamps to feasible boundary.
    """
    mu=lo.copy();left=max(0.,float(bound-w@lo))
    order=np.argsort(a/w)
    if maximize:order=order[::-1]
    for k in order:
        increment=min(float(hi[k]-lo[k]),left/w[k])
        mu[k]+=increment;left=max(0.,left-increment*w[k])
    return float(a@mu)

def joint_replay(groups,epsilon=.02,alpha=.05,seed=0,allocation='proportional',batch=16):
    groups=[validate(g,alpha) for g in groups];rng=np.random.default_rng(seed)
    Nhs=np.array([len(g) for g in groups]);N=int(Nhs.sum());w=Nhs/N;H=len(groups)
    streams=[(rng.permutation(g)+1)/2 for g in groups]
    local=[]
    for x in streams:
        n=len(x);t=np.arange(1,n+1);s=np.cumsum(x);prev=np.r_[0.,s[:-1]]
        A=np.cumsum(n/(n-t+1));Z=np.cumsum(x+prev/(n-t+1));p=np.r_[.5,Z[:-1]/A[:-1]]
        V=np.cumsum((x-p)**2)
        local.append((s,A,Z,V,np.cumsum(x*x)))
    counts=np.zeros(H,dtype=int);s=np.zeros(H);A=np.zeros(H);Z=np.zeros(H);V=np.zeros(H);ss=np.zeros(H)
    truthmean=math.fsum(float(x) for g in groups for x in g)/N;truth=label(truthmean,epsilon)
    rejected={(b,sg):False for b in (-1,1) for sg in (-1,1)}
    for t in range(1,N+1):
        if allocation=='proportional':priority=w/(counts+1)
        elif allocation=='neyman':
            variance=np.maximum(0,(ss-s*s/np.maximum(counts,1))/np.maximum(counts-1,1))
            sd=np.sqrt((counts*variance+.25)/(counts+1));priority=w*sd/(counts+1)
        else:raise ValueError('allocation')
        k=int(np.argmax(np.where(counts<Nhs,priority,-np.inf)));j=counts[k];counts[k]+=1
        s[k],A[k],Z[k],V[k],ss[k]=[arr[j] for arr in local[k]]
        if t%batch and t<N:continue
        lo=s/Nhs;hi=(s+Nhs-counts)/Nhs
        globlo=float(w@lo);globhi=float(w@hi);zsum=Z.sum();vsum=V.sum()
        for b in (-1,1):
            mu=(1+b*epsilon)/2
            for sg in (-1,1):
                impossible=globlo>mu+1e-12 if sg==1 else globhi<mu-1e-12
                if impossible:rejected[b,sg]=True;continue
                if sg==1:
                    worst=extreme(A,w,lo,hi,min(mu,globhi),True);signal=zsum-worst
                else:
                    worst=extreme(A,w,lo,hi,max(mu,globlo),False);signal=worst-zsum
                logs=BET_GRID*signal-(-np.log1p(-BET_GRID)-BET_GRID)*vsum
                mx=logs.max();logmean=mx+np.log(np.exp(logs-mx).mean())
                rejected[b,sg]=rejected[b,sg] or logmean>=math.log(2/alpha)
        a=rejected[1,1];b=rejected[-1,-1];e=rejected[-1,1] and rejected[1,-1]
        decision='A' if a and not b and not e else 'B' if b and not a and not e else 'E' if e and not a and not b else 'C'
        if t==N:decision=truth
        if decision!='C':return dict(n=t,N=N,decision=decision,truth=truth,error=int(decision!=truth),cost=float(t),delta=truthmean,batch=batch)
    raise AssertionError('census')
