from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
from scipy.stats import beta
OUT=ROOT/'results'
for file,keys in [('prediction_real',['dataset','method']),('cost_simulation',['case','method']),
                  ('close_pairs',['dataset','cohort','method']),('betting_simulation',['case','epsilon','alpha'])]:
 d=pd.read_json(OUT/(file+'.jsonl'),lines=True);d['fraction']=d.n/d.N
 s=d.groupby(keys).agg(runs=('n','size'),fraction=('fraction','mean'),errors=('error','sum'),error_rate=('error','mean')).reset_index()
 if file=='cost_simulation':s=s.merge(d.groupby(keys).cost_fraction.mean().reset_index(),on=keys)
 if file=='betting_simulation':
  s['error_cp_lower']=[0 if k==0 else beta.ppf(.025,k,n-k+1) for k,n in zip(s.errors,s.runs)]
  s['error_cp_upper']=[1 if k==n else beta.ppf(.975,k+1,n-k) for k,n in zip(s.errors,s.runs)]
 s.to_csv(OUT/(file+'_summary.csv'),index=False)
 print(file,len(d),'runs', 'max error',s.error_rate.max(),flush=True)
 if file!='betting_simulation':print(s.to_string(index=False))
