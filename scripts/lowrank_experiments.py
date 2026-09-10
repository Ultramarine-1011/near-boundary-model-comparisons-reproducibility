from pathlib import Path
import sys,json,zipfile,time
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from lowrank_predictor import basis_from_history,predict,select_hyperparameters
from prediction_eval import signal_betting
start=time.time();provenance=[];out=ROOT/'results'
with (out/'lowrank_real.jsonl').open('w',encoding='utf-8') as f:
 for path in sorted((ROOT/'data'/'processed').glob('*.npz')):
  z=np.load(path,allow_pickle=True);name=path.stem;n=z['scores'].shape[1]
  if name in ('mmlu-pro','composite'):archive=name+'.zip';member='M1.csv'
  else:archive='atlas.zip';member=f'data/gaussian_sampled_{name}_response_matrix_train'+('' if name=='arc' else '_with_scores')+'.csv'
  with zipfile.ZipFile(ROOT/'data'/'raw'/archive) as raw:history=pd.read_csv(raw.open(member),index_col=0)
  history=history.loc[~history.index.isin(z['models']),z['items']]
  history=history.loc[np.isfinite(history.to_numpy(float)).all(axis=1)]
  indices=np.random.default_rng(91024).permutation(len(history))
  training=history.iloc[indices[:512]];validation=history.iloc[indices[512:576]]
  assert len(validation)==64 and not set(training.index)&set(validation.index)
  mean,features=basis_from_history(training.to_numpy(float))
  best,weights,candidates=select_hyperparameters(mean,features,validation.to_numpy(float))
  provenance.append(dict(dataset=name,training_ids=training.index.astype(str).tolist(),validation_ids=validation.index.astype(str).tolist(),best=best,candidates=candidates))
  for pair,(ia,ib) in enumerate(z['pairs'][:30]):
   a=z['scores'][ia].astype(float);b=z['scores'][ib].astype(float);d=a-b
   for rep in range(10):
    seed=2026094900+pair*1000+rep;pilot=np.random.default_rng(seed).permutation(n)[:64]
    pa=predict(mean,features,pilot,a[pilot],best['rank'],best['ridge'])
    pb=predict(mean,features,pilot,b[pilot],best['rank'],best['ridge'])
    prediction=(pa-pb+1)/2
    unseen=np.ones(n,bool);unseen[pilot]=False
    diagnostic_mse=float(np.mean((prediction[unseen]-(d[unseen]+1)/2)**2))
    for method,w in [('signal_uniform_lowrank',np.ones(n)),('signal_weighted_lowrank',weights)]:
     f.write(json.dumps(dict(dataset=name,pair=pair,rep=rep,seed=seed,method=method,epsilon=.02,alpha=.05,unseen_prediction_mse=diagnostic_mse,
                            **signal_betting(d,prediction,w,.02,.05,seed+1,pilot)))+'\n')
  (out/'lowrank_provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
  print(name,best,flush=True)
(out/'lowrank_run.json').write_text(json.dumps(dict(elapsed_seconds=time.time()-start,expected_rows=4200)),encoding='utf-8')
