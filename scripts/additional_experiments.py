from pathlib import Path
import sys,json,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from finite_eval import betting_decision,cs_path,stop_from_path,stratified_replay
OUT=ROOT/'results'
start=time.time()
with (OUT/'betting_real.jsonl').open('w',encoding='utf-8') as f:
 for p in sorted((ROOT/'data'/'processed').glob('*.npz')):
  a=np.load(p,allow_pickle=True)
  for pair,(i,j) in enumerate(a['pairs']):
   d=a['scores'][i].astype(float)-a['scores'][j]
   for rep in range(30):
    seed=2026091900+pair*1000+rep;stream=np.random.default_rng(seed).permutation(d)
    f.write(json.dumps(dict(dataset=p.stem,pair=pair,rep=rep,seed=seed,method='threshold_betting',epsilon=.02,alpha=.05,**betting_decision(stream,.02)))+'\n')
  print('betting',p.stem,flush=True)
cases={'opposite_constants':[np.ones(1000),-np.ones(1000)],
       'opposite_mixed':[np.r_[np.ones(900),np.zeros(100)],np.r_[-np.ones(900),np.zeros(100)]],
       'homogeneous_mixed':[np.r_[np.ones(100),-np.ones(100),np.zeros(800)]]*2,
       'rare_noisy_stratum':[np.zeros(1800),np.r_[np.ones(100),-np.ones(100)]]}
with (OUT/'heterogeneity_simulation.jsonl').open('w',encoding='utf-8') as f:
 for name,groups in cases.items():
  for rep in range(300):
   seed=2026093900+rep;stream=np.random.default_rng(seed).permutation(np.concatenate(groups))
   records=[dict(method='unstratified',**stop_from_path(stream,*cs_path(stream),.02))]
   records.extend(dict(method=m,**stratified_replay(groups,.02,.05,seed,m)) for m in ['proportional','neyman'])
   for row in records:f.write(json.dumps(dict(case=name,rep=rep,seed=seed,epsilon=.02,alpha=.05,**row))+'\n')
  print('heterogeneity',name,flush=True)
(OUT/'additional_run.json').write_text(json.dumps({'elapsed_seconds':time.time()-start}),encoding='utf-8')
