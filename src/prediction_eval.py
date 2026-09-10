"""CELEUS Eq. (1) signal with finite-pool directional betting adaptation.

Not the authors' full experimental pipeline. Surrogates and weights are frozen
after a charged pilot; validity is independent of their predictive accuracy.
"""
import math
import numpy as np
from finite_eval import BET_GRID,label,validate

def signal_betting(d,prediction,weights,epsilon,alpha,seed,pilot_indices=()):
 d=validate(d,alpha);N=len(d);x=(d+1)/2
 p=np.asarray(prediction,float);w=np.asarray(weights,float)
 if p.shape!=x.shape or w.shape!=x.shape or not np.isfinite(p).all() or not np.isfinite(w).all():raise ValueError('invalid predictor/weights')
 if np.any((p<0)|(p>1)) or np.any(w<=0):raise ValueError('support violation')
 pilot=np.asarray(pilot_indices,dtype=int)
 if len(np.unique(pilot))!=len(pilot) or np.any((pilot<0)|(pilot>=N)):raise ValueError('invalid pilot')
 rem=np.setdiff1d(np.arange(N),pilot)
 if not len(rem):raise ValueError('pilot must leave an unobserved item')
 rng=np.random.default_rng(seed)
 # Exponential race is exactly successive sampling with probabilities w/sum(w).
 order=rem[np.argsort(-np.log(rng.uniform(size=len(rem)))/w[rem])]
 xs=x[order];ps=p[order];ws=w[order];n=len(order)
 remaining_w=np.cumsum(ws[::-1])[::-1]
 remaining_p=np.cumsum(ps[::-1])[::-1]
 old_sum=np.sum(x[pilot])+np.r_[0.,np.cumsum(xs)[:-1]]
 q=ws/remaining_w;base=(old_sum+remaining_p)/N
 signals=base+(xs-ps)/(N*q)
 maxlow=np.maximum.accumulate((ps/ws)[::-1])[::-1]
 maxhigh=np.maximum.accumulate(((1-ps)/ws)[::-1])[::-1]
 lower=base-remaining_w/N*maxlow
 upper=base+remaining_w/N*maxhigh
 span=upper-lower
 if np.any(span<=0):raise AssertionError('positive signal span required')
 y=(signals-lower)/span
 if np.any((y< -1e-10)|(y>1+1e-10)):raise AssertionError('invalid signal bounds')
 sums=old_sum+xs;remaining_count=N-len(pilot)-np.arange(1,n+1)
 rejects={}
 for bound in (-1,1):
  mu=(1+bound*epsilon)/2;m=(mu-lower)/span;feasible=(m>=0)&(m<=1)
  for sign in (-1,1):
   logs=np.cumsum(np.where(feasible,np.log1p(sign*BET_GRID[:,None]*(y-np.clip(m,0,1))),0.),axis=1)
   mx=logs.max(axis=0);logmean=mx+np.log(np.exp(logs-mx).mean(axis=0))
   impossible=(sums/N>mu+1e-12) if sign==1 else ((sums+remaining_count)/N<mu-1e-12)
   rejects[bound,sign]=np.maximum.accumulate((logmean>=math.log(2/alpha))|impossible)
 a=rejects[1,1];b=rejects[-1,-1];e=rejects[-1,1]&rejects[1,-1]
 verdict=np.full(n,'C',dtype='<U1');verdict[a&~b&~e]='A';verdict[b&~a&~e]='B';verdict[e&~a&~b]='E'
 mean=math.fsum(map(float,d))/N;truth=label(mean,epsilon);verdict[-1]=truth
 j=int(np.flatnonzero(verdict!='C')[0]);used=len(pilot)+j+1
 return dict(n=used,N=N,decision=str(verdict[j]),truth=truth,error=int(verdict[j]!=truth),cost=float(used),delta=mean,pilot=len(pilot))
