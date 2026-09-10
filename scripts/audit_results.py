"""Independent streaming consistency audit, using only the standard library.

Checks completeness and recorded outcomes, not the validity proof or whether
the experimental design supports extrapolation beyond the released matrices.
"""
from pathlib import Path
from collections import defaultdict
import csv,hashlib,json,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
EXPECTED={'simulation':414000,'real':462000,'stratification':6500,
          'betting_real':21000,'heterogeneity_simulation':3600,
          'betting_simulation':69000,'prediction_real':6300,
          'cost_simulation':1800,'close_pairs':56000,
          'joint_stratification':5800,'joint_controls':1400,'lowrank_real':4200,'boundary_revision':66600}
report={'scope':'record integrity and selected headline arithmetic, not a proof of inference validity','files':{},'claims':{}}
main=defaultdict(lambda:[0,0.,0]);bet=defaultdict(lambda:[0,0.,0])
for name,expected in EXPECTED.items():
    path=OUT/(name+'.jsonl');count=0;errors=0
    with path.open(encoding='utf-8') as f:
        for line in f:
            row=json.loads(line);count+=1
            assert isinstance(row['n'],int) and 1<=row['n']<=row['N'],(name,count,'sample count')
            assert row['decision'] in ('A','B','E') and row['truth'] in ('A','B','E'),(name,count,'label')
            assert row['error']==int(row['decision']!=row['truth']),(name,count,'error flag')
            assert math.isfinite(row.get('cost',row['n'])) and row.get('cost',row['n'])>0,(name,count,'cost')
            assert -1-1e-12<=row['delta']<=1+1e-12,(name,count,'mean')
            assert row['n']!=row['N'] or row['error']==0,(name,count,'census error')
            errors+=row['error']
            if name=='real' and row['epsilon']==.02 and row['method']=='eb_grid':
                a=main[row['dataset']];a[0]+=1;a[1]+=row['n']/row['N'];a[2]+=row['error']
            if name=='betting_real':
                a=bet[row['dataset']];a[0]+=1;a[1]+=row['n']/row['N'];a[2]+=row['error']
    assert count==expected,(name,count,expected)
    report['files'][name]={'rows':count,'errors':errors,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    print(name,count,'rows checked',flush=True)
assert len(main)==7 and all(x[0]==3000 for x in main.values())
assert len(bet)==7 and all(x[0]==3000 for x in bet.values())
assert sum(x[2] for x in main.values())==0
assert sum(x[2] for x in bet.values())==11
macro=sum(x[1]/x[0] for x in main.values())/7
assert round(100*macro,1)==41.6
with (OUT/'real_summary.csv').open(newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['method']=='eb_grid' and float(row['epsilon'])==.02:
            count,total,errors=main[row['dataset']]
            assert math.isclose(total/count,float(row['cost_fraction']),abs_tol=1e-12)
            assert errors==int(row['errors']) and count==int(row['runs'])
report['claims']={'main_eb_grid_macro_fraction':macro,'main_eb_grid_errors':0,'direct_betting_errors':11,
                  'main_runs_per_method':21000,'total_replay_records':sum(EXPECTED.values())}
for entry in json.loads((ROOT/'data'/'raw'/'manifest.json').read_text()):
    raw=ROOT/'data'/'raw'/entry['file']
    assert hashlib.sha256(raw.read_bytes()).hexdigest()==entry['sha256']
for entry in json.loads((ROOT/'data'/'processed'/'audit.json').read_text()):
    derived=ROOT/'data'/'processed'/(entry['dataset']+'.npz')
    assert hashlib.sha256(derived.read_bytes()).hexdigest()==entry['processed_sha256']
report['input_archive_hashes']='verified';report['processed_snapshot_hashes']='verified'
(OUT/'integrity_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report['claims'],indent=2))
