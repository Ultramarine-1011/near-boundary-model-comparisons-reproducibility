"""Recompute benchmark truth with integer totals and rational margins.

Independent of the evaluator's label function and its recorded delta/truth.
"""
from pathlib import Path
from fractions import Fraction
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'results'
matrices={}
for p in (ROOT/'data'/'processed').glob('*.npz'):
    with np.load(p,allow_pickle=True) as z:
        scores=z['scores'];assert np.isin(scores,[0,1]).all()
        matrices[p.stem]={'N':scores.shape[1],'totals':scores.sum(axis=1,dtype=np.int64),
                          'models':z['models'].tolist(),'pairs':z['pairs'].copy()}
close={}
for r in json.loads((out/'close_pair_selection.json').read_text()):
    m=matrices[r['dataset']]
    close[r['dataset'],r['cohort'],r['pair']]=(m['models'].index(r['a']),m['models'].index(r['b']))
files=['real','betting_real','stratification','prediction_real','lowrank_real','close_pairs','joint_stratification','joint_controls']
report={}
for name in files:
    count=0
    with (out/(name+'.jsonl')).open(encoding='utf-8') as f:
        for line in f:
            r=json.loads(line);m=matrices[r['dataset']]
            if name=='close_pairs':a,b=close[r['dataset'],r['cohort'],r['pair']]
            else:a,b=m['pairs'][r['pair']]
            difference=int(m['totals'][a])-int(m['totals'][b])
            delta=Fraction(difference,m['N']);eps=Fraction(str(r.get('epsilon',.02)))
            expected='A' if delta>eps else 'B' if delta< -eps else 'E'
            assert r['N']==m['N'] and r['truth']==expected,(name,count,'wrong target')
            assert math.isclose(r['delta'],float(delta),rel_tol=0,abs_tol=1e-15),(name,count,'wrong mean')
            if 'model_a' in r:
                assert r['model_a']==m['models'][a] and r['model_b']==m['models'][b]
            count+=1
    report[name]={'rows':count,'target_means_and_labels':'verified against integer score totals'}
    print(name,count,'targets verified',flush=True)
(out/'target_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
