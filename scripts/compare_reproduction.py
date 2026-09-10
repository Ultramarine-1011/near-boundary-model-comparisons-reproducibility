"""Compare independent outputs; container timestamps are not semantic data."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('other',type=Path);args=p.parse_args();other=args.other.resolve()
audit=json.loads((ROOT/'results'/'integrity_audit.json').read_text())
report={'other':str(other),'score_arrays':{},'replay_files':{}}
for source in sorted((ROOT/'data'/'processed').glob('*.npz')):
    with np.load(source,allow_pickle=True) as a,np.load(other/'data'/'processed'/source.name,allow_pickle=True) as b:
        assert set(a.files)==set(b.files)
        for key in a.files:assert np.array_equal(a[key],b[key]),(source.name,key)
        report['score_arrays'][source.name]='all named arrays exactly equal'
for name,entry in audit['files'].items():
    target=other/'results'/(name+'.jsonl')
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    assert digest==entry['sha256'],name+' replay records differ'
    report['replay_files'][name]={'sha256':digest,'rows':entry['rows'],'exact_match':True}
steps=json.loads((other/'results'/'reproduction_run.json').read_text())
assert len(steps) in (21,23,25) and all(s['returncode']==0 for s in steps), 'incomplete or failed reproduction pipeline'
if len(steps)==21:
    supplements=json.loads((other/'results'/'supplemental_reproduction_run.json').read_text())
    assert {s['script'] for s in supplements}=={'plot_followups.py','audit_targets.py'}
    assert all(s['returncode']==0 for s in supplements)
    report['supplemental_steps']=2
report['pipeline_steps']=len(steps)
code_files=list((ROOT/'src').glob('*.py'))
code_files += [ROOT/s['arguments'][0] for s in steps if s['arguments'][0].startswith('scripts/')]
report['matched_source_files']={}
for source in code_files:
    rel=source.relative_to(ROOT)
    original=hashlib.sha256(source.read_bytes()).hexdigest()
    rebuilt=hashlib.sha256((other/rel).read_bytes()).hexdigest()
    assert original==rebuilt, str(rel)+' changed since the clean run'
    report['matched_source_files'][str(rel).replace('\\','/')]=original
(ROOT/'results'/'clean_reproduction_comparison.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Seven matrices and all replay records match the independent rebuild exactly.')
