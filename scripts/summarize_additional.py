from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
for file,keys in [('betting_real',['dataset','method']),('heterogeneity_simulation',['case','method'])]:
 d=pd.read_json(OUT/(file+'.jsonl'),lines=True);d['fraction']=d.n/d.N
 s=d.groupby(keys).agg(runs=('n','size'),fraction=('fraction','mean'),errors=('error','sum'),error_rate=('error','mean')).reset_index()
 s.to_csv(OUT/(file+'_summary.csv'),index=False);print(s.to_string(index=False))
