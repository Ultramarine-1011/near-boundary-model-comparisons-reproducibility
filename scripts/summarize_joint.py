from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'results'
d=pd.read_json(out/'joint_stratification.jsonl',lines=True)
keys=['dataset','pair','rep','strata','method']
assert not d.duplicated(keys).any()
assert len(d)==5800, f'Incomplete run: {len(d)}'
assert set(d.dataset)=={'arc','composite','gsm8k','hellaswag','mmlu-pro','truthfulqa','winogrande'}
assert (d.groupby(['dataset','strata','method']).size()==100).all()
d['fraction']=d.n/d.N
s=d.groupby(['dataset','strata','method']).agg(runs=('n','size'),fraction=('fraction','mean'),errors=('error','sum')).reset_index()
s.to_csv(out/'joint_stratification_summary.csv',index=False)
print(s.to_string(index=False))
c=pd.read_json(out/'joint_controls.jsonl',lines=True)
assert len(c)==1400 and not c.duplicated(['dataset','pair','rep','method']).any()
assert (c.groupby(['dataset','method']).size()==100).all()
c['fraction']=c.n/c.N
controls=c.groupby(['dataset','method']).agg(runs=('n','size'),fraction=('fraction','mean'),errors=('error','sum')).reset_index()
controls.to_csv(out/'joint_controls_summary.csv',index=False)
print(controls.to_string(index=False))
