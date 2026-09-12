"""Focused, prespecified boundary sweep and planned-look calibration diagnostic."""
from pathlib import Path
import sys,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'src')]
from scipy.stats import norm
from finite_eval import cs_path,stop_from_path,betting_decision,decide,label
from run_experiments import population

def planned_gaussian(d,eps,alpha=.05):
    n=len(d);looks=np.unique(np.r_[np.ceil(20*1.5**np.arange(30)).astype(int),n]);looks=looks[looks<=n]
    critical=norm.ppf(1-alpha/(2*len(looks)))
    mean=math.fsum(map(float,d))/n;truth=label(mean,eps)
    for t in looks:
        m=float(np.mean(d[:t]));se=float(np.std(d[:t],ddof=1))*math.sqrt((1-t/n)/t)
        decision=truth if t==n else decide(m-critical*se,m+critical*se,eps)
        if decision!='C':return dict(n=int(t),N=n,decision=decision,truth=truth,error=int(decision!=truth),delta=mean)

if __name__=='__main__':
 cases=[]
 for N in (1000,5000):
  for q in (.05,.3,.8):
   for offset in (-.02,-.01,-.004,-.002,0,.002,.004,.01,.02,.04):
    delta=.02+offset
    if delta<=q:cases.append((f'N{N}_q{q}_o{offset}',population(N,q,delta),.02,q))
  for b in (0.,.016,.018,.02,.022,.024,.04):cases.append((f'constant_N{N}_b{b}',np.full(N,b),.02,0.))
  cases.append((f'rare_N{N}',np.r_[np.zeros(N-1),1.],.5/N,1/N))
 with (ROOT/'results/boundary_revision.jsonl').open('w',encoding='utf-8') as out:
  for k,(name,d,eps,q) in enumerate(cases):
   delta=math.fsum(map(float,d))/len(d);g=abs(abs(delta)-eps);v=float(np.var(d))
   for rep in range(300):
    seed=202609091000+k*1000+rep;s=np.random.default_rng(seed).permutation(d)
    for method,r in [('direct_betting',betting_decision(s,eps)),('eb_grid',stop_from_path(s,*cs_path(s),eps)),('planned_gaussian',planned_gaussian(s,eps))]:
     out.write(json.dumps(dict(case=name,rep=rep,seed=seed,epsilon=eps,alpha=.05,q=q,gap=g,variance=v,method=method,**r))+'\n')
   print(name,flush=True)
