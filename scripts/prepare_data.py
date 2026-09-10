"""Build immutable-score study inputs from published response matrices.

Only remove incomplete model rows. Do not fill missing responses with zero.
Save the complete original item grid and 100 randomly selected disjoint pairs.
"""
from pathlib import Path
import json,zipfile,hashlib,sys
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'processed';OUT.mkdir(parents=True,exist_ok=True)
audits=[]
def prepare(name,archive,test_member,train_member=None):
 with zipfile.ZipFile(ROOT/'data'/'raw'/archive) as z:
  df=pd.read_csv(z.open(test_member),index_col=0)
  meta=[c for c in ('created_date','sha') if c in df]
  df=df.drop(columns=meta)
  original_shape=df.shape
  a=df.apply(pd.to_numeric,errors='raise').to_numpy(float)
  finite=np.isfinite(a).all(axis=1)
  if np.any(np.isfinite(a)&((a!=0)&(a!=1))):
   raise ValueError(f'{name}: nonbinary observed scores; inspect rather than coerce')
  df=df.loc[finite];a=a[finite].astype(np.int8)
  if df.index.has_duplicates:raise ValueError('duplicate model IDs')
  if df.columns.has_duplicates:raise ValueError('duplicate item IDs')
  rng=np.random.default_rng(20260909)
  # Unique, disjoint model pairs prevents a model dominating the random cohort.
  indices=rng.permutation(len(a))[:min(200,len(a)//2*2)].reshape(-1,2)
  strata=np.zeros(a.shape[1],dtype=int);strata_names=['all']
  if name=='composite':
   names=[str(c).rsplit('_',1)[0] for c in df.columns]
   strata_names=sorted(set(names));strata=np.array([strata_names.index(s) for s in names])
  difficulty=None;train_info=None
  if train_member:
   train=pd.read_csv(z.open(train_member),index_col=0).drop(columns=['created_date','sha','model_score','score','actual_accuracy'],errors='ignore')
   train=train.loc[~train.index.isin(df.index)]
   common=[c for c in df.columns if c in train.columns]
   if len(common)==len(df.columns):
    ta=train[df.columns].apply(pd.to_numeric,errors='raise').to_numpy(float)
    ta=ta[np.isfinite(ta).all(axis=1)]
    if len(ta):difficulty=ta.mean(axis=0)
    train_info={'complete_disjoint_rows':len(ta),'common_items':len(common)}
   else:train_info={'complete_disjoint_rows':None,'common_items':len(common)}
  save=dict(scores=a,models=df.index.astype(str).to_numpy(),items=df.columns.astype(str).to_numpy(),pairs=indices,strata=strata,strata_names=np.array(strata_names))
  if difficulty is not None:save['difficulty']=difficulty
  np.savez_compressed(OUT/(name+'.npz'),**save)
  audit=dict(dataset=name,archive=archive,member=test_member,original_shape=original_shape,
             retained_shape=a.shape,incomplete_rows_removed=int((~finite).sum()),pairs=len(indices),
             strata=len(strata_names),train=train_info,
             source_archive_sha256=hashlib.sha256((ROOT/'data'/'raw'/archive).read_bytes()).hexdigest(),
             processed_sha256=hashlib.sha256((OUT/(name+'.npz')).read_bytes()).hexdigest())
  audits.append(audit);print(json.dumps(audit),flush=True)
for name in ['arc','gsm8k','hellaswag','truthfulqa','winogrande']:
 train='data/gaussian_sampled_'+name+'_response_matrix_train'+('' if name=='arc' else '_with_scores')+'.csv'
 prepare(name,'atlas.zip',f'data/gaussian_sampled_{name}_response_matrix_test.csv',train)
for name in ['mmlu-pro','composite']:prepare(name,name+'.zip','M2.csv','M1.csv')
(OUT/'audit.json').write_text(json.dumps(audits,indent=2),encoding='utf-8')
