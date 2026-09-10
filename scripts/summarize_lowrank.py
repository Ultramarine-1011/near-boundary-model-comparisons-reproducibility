from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'results'
d=pd.read_json(out/'lowrank_real.jsonl',lines=True)
assert len(d)==4200 and not d.duplicated(['dataset','pair','rep','method']).any()
assert (d.groupby(['dataset','method']).size()==300).all()
d['fraction']=d.n/d.N
s=d.groupby(['dataset','method']).agg(runs=('n','size'),fraction=('fraction','mean'),errors=('error','sum'),prediction_mse=('unseen_prediction_mse','mean')).reset_index()
s.to_csv(out/'lowrank_real_summary.csv',index=False)
print(s.to_string(index=False))
baseline=pd.read_json(out/'prediction_real.jsonl',lines=True)
baseline=baseline[baseline.method=='signal_uniform_constant'][['dataset','pair','rep','n','N']]
baseline['base_fraction']=baseline.n/baseline.N
matched=d.merge(baseline[['dataset','pair','rep','base_fraction']],on=['dataset','pair','rep'],validate='many_to_one')
matched['difference']=matched.fraction-matched.base_fraction
rows=[];rng=np.random.default_rng(20260909)
for (dataset,method),group in matched.groupby(['dataset','method']):
    pair_means=group.groupby('pair').difference.mean().to_numpy()
    assert len(pair_means)==30
    draws=pair_means[rng.integers(0,30,size=(5000,30))].mean(axis=1)
    rows.append(dict(dataset=dataset,method=method,pairs=30,difference=pair_means.mean(),
                     cluster_bootstrap_lower=np.quantile(draws,.025),cluster_bootstrap_upper=np.quantile(draws,.975)))
pd.DataFrame(rows).to_csv(out/'lowrank_paired_cost.csv',index=False)
