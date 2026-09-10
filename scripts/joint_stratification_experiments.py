from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from stratified_joint import joint_replay
with (ROOT/'results'/'joint_stratification.jsonl').open('w',encoding='utf-8') as f:
 for p in sorted((ROOT/'data'/'processed').glob('*.npz')):
  z=np.load(p,allow_pickle=True);N=z['scores'].shape[1];definitions={}
  if len(np.unique(z['strata']))>1:definitions['task']=z['strata']
  order=np.argsort(z['difficulty'],kind='stable')
  for H in (2,4,8):
   s=np.empty(N,dtype=int)
   for k,idx in enumerate(np.array_split(order,H)):s[idx]=k
   definitions[f'difficulty{H}']=s
  definitions['random4']=np.random.default_rng(12345).permutation(N)%4
  for pair,(a,b) in enumerate(z['pairs'][:20]):
   d=z['scores'][a].astype(float)-z['scores'][b]
   for rep in range(5):
    seed=2026092900+pair*1000+rep
    for name,s in definitions.items():
     groups=[d[s==k] for k in np.unique(s)]
     for allocation in ('proportional','neyman'):
      f.write(json.dumps(dict(dataset=p.stem,pair=pair,rep=rep,seed=seed,strata=name,method='joint_'+allocation,epsilon=.02,alpha=.05,
                             **joint_replay(groups,.02,.05,seed,allocation)))+'\n')
  print('joint stratification',p.stem,flush=True)
