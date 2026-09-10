"""Retrospectively selected hard cohorts, explicitly separate from random pairs."""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from finite_eval import cs_path,stop_from_path,betting_decision
selection=[]
with (ROOT/'results'/'close_pairs.jsonl').open('w',encoding='utf-8') as f:
 for p in sorted((ROOT/'data'/'processed').glob('*.npz')):
  z=np.load(p,allow_pickle=True);scores=z['scores'];means=scores.mean(axis=1);rank=np.argsort(-means,kind='stable')
  cohorts={'top_adjacent':list(zip(rank[:20],rank[1:21]))}
  i,j=np.triu_indices(len(means),1)
  distance=np.abs(np.abs(means[i]-means[j])-.02)
  inds=np.argsort(distance,kind='stable')[:20]
  cohorts['margin_nearest']=list(zip(i[inds],j[inds]))
  for cohort,pairs in cohorts.items():
   for pair,(a,b) in enumerate(pairs):
    d=scores[a].astype(float)-scores[b]
    selection.append(dict(dataset=p.stem,cohort=cohort,pair=pair,a=str(z['models'][a]),b=str(z['models'][b]),delta=float(d.mean())))
    for rep in range(100):
     seed=2026096900+pair*1000+rep;stream=np.random.default_rng(seed).permutation(d)
     for method,result in [('eb_grid',stop_from_path(stream,*cs_path(stream),.02)),('threshold_betting',betting_decision(stream,.02))]:
      f.write(json.dumps(dict(dataset=p.stem,cohort=cohort,pair=pair,rep=rep,seed=seed,method=method,epsilon=.02,alpha=.05,**result))+'\n')
  print('close pairs',p.stem,flush=True)
(ROOT/'results'/'close_pair_selection.json').write_text(json.dumps(selection,indent=2),encoding='utf-8')
