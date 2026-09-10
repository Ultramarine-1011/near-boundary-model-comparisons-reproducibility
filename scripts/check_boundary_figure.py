"""Independently check the public pair means plotted in the main figure."""
from pathlib import Path
import csv, json, math, hashlib
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'results'
raw=defaultdict(list)
for filename,cohort in [('betting_real','random'),('close_pairs','margin_nearest')]:
    with (out/f'{filename}.jsonl').open(encoding='utf-8') as f:
        for line in f:
            r=json.loads(line)
            if r['method']!='threshold_betting':continue
            if cohort!='random' and r['cohort']!=cohort:continue
            assert r['epsilon']==.02 and r['alpha']==.05
            raw[(cohort,r['dataset'],r['pair'])].append(r)
table=list(csv.DictReader((out/'boundary_figure_pairs.csv').open(encoding='utf-8')))
assert len(table)==len(raw)==840
seen=set()
for p in table:
    key=(p['cohort'],p['dataset'],int(p['pair']))
    assert key not in seen;seen.add(key)
    rows=raw[key];n=len(rows)
    assert n==int(p['runs'])==(30 if key[0]=='random' else 100)
    assert len({r['rep'] for r in rows})==n
    assert math.isclose(float(p['fraction']),math.fsum(r['n']/r['N'] for r in rows)/n,abs_tol=1e-12)
    assert math.isclose(float(p['gap']),abs(abs(rows[0]['delta'])-.02),abs_tol=1e-12)
assert sum(k[0]=='random' for k in seen)==700
assert sum(k[0]=='margin_nearest' for k in seen)==140
report={'checked_pair_means':840,'random_pairs':700,'stress_pairs':140,
        'new_evaluation_runs':0,'scope':'Standard-library reconstruction of plotted pair means and gaps from existing JSONL records.',
        'files':{name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in ['betting_real.jsonl','close_pairs.jsonl','boundary_figure_pairs.csv']}}
(out/'boundary_figure_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
