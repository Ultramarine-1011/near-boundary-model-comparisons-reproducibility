from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from finite_eval import cs_path,stop_from_path,stratified_replay
profiles={'cheap_constant':[np.zeros(1800),np.r_[np.ones(100),-np.ones(100)]],
          'expensive_constant':[np.r_[np.ones(100),-np.ones(100)],np.zeros(1800)]}
with (ROOT/'results'/'cost_simulation.jsonl').open('w',encoding='utf-8') as f:
 for name,groups in profiles.items():
  d=np.concatenate(groups);cost=np.repeat([1.,10.],[len(g) for g in groups]);full=cost.sum()
  for rep in range(300):
   seed=2026095900+rep;order=np.random.default_rng(seed).permutation(len(d));stream=d[order]
   rows=[dict(method='unstratified',**stop_from_path(stream,*cs_path(stream),.02,cost[order]))]
   rows.extend(dict(method=m,**stratified_replay(groups,.02,.05,seed,m,[1.,10.])) for m in ['proportional','neyman'])
   for r in rows:f.write(json.dumps(dict(case=name,rep=rep,seed=seed,full_cost=full,cost_fraction=r['cost']/full,**r))+'\n')
  print('cost',name,flush=True)
