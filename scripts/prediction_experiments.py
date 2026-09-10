from pathlib import Path
import sys,json,zipfile,time
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from prediction_eval import signal_betting
OUT=ROOT/'results';start=time.time();provenance=[]
with (OUT/'prediction_real.jsonl').open('w',encoding='utf-8') as out:
 for path in sorted((ROOT/'data'/'processed').glob('*.npz')):
  data=np.load(path,allow_pickle=True);name=path.stem;N=data['scores'].shape[1]
  if name in ('mmlu-pro','composite'):archive=name+'.zip';member='M1.csv'
  else:
   archive='atlas.zip';member=f'data/gaussian_sampled_{name}_response_matrix_train'+('' if name=='arc' else '_with_scores')+'.csv'
  with zipfile.ZipFile(ROOT/'data'/'raw'/archive) as z:train=pd.read_csv(z.open(member),index_col=0)
  train=train.loc[~train.index.isin(data['models']),data['items']]
  train=train.loc[np.isfinite(train.to_numpy(float)).all(axis=1)]
  chosen=np.random.default_rng(91024).permutation(len(train))[:32]
  refs=train.iloc[chosen].to_numpy(float)
  provenance.append(dict(dataset=name,historical_model_ids=train.index[chosen].astype(str).tolist(),pilot=64,reference_count=len(refs)))
  uncertainty=np.sqrt(np.maximum(.01,refs.var(axis=0)))
  for pair,(ia,ib) in enumerate(data['pairs'][:30]):
   a=data['scores'][ia].astype(float);b=data['scores'][ib].astype(float);d=a-b
   for rep in range(10):
    seed=2026094900+pair*1000+rep;pilot=np.random.default_rng(seed).permutation(N)[:64]
    ra=np.argmin(np.mean((refs[:,pilot]-a[pilot])**2,axis=1))
    rb=np.argmin(np.mean((refs[:,pilot]-b[pilot])**2,axis=1))
    prediction=(refs[ra]-refs[rb]+1)/2
    for method,p,w in [('signal_uniform_constant',np.full(N,.5),np.ones(N)),
                       ('signal_uniform_surrogate',prediction,np.ones(N)),
                       ('signal_weighted_surrogate',prediction,uncertainty)]:
     out.write(json.dumps(dict(dataset=name,pair=pair,rep=rep,seed=seed,method=method,epsilon=.02,alpha=.05,
                               **signal_betting(d,p,w,.02,.05,seed+1,pilot)))+'\n')
  print('prediction',name,flush=True)
(OUT/'prediction_provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
(OUT/'prediction_run.json').write_text(json.dumps({'elapsed_seconds':time.time()-start,'pairs_per_dataset':30,'replays':10,'pilot':64}),encoding='utf-8')
