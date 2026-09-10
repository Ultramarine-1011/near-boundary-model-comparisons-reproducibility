"""Create a review archive without redistributing response matrices or caches."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
for required in ('integrity_audit.json','target_audit.json','clean_reproduction_comparison.json'):
    assert (ROOT/'results'/required).is_file(),f'Complete {required} before packaging'
selected=[]
for p in ROOT.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(ROOT)
    if any(part in ('.cache','__pycache__','.venv') for part in rel.parts):continue
    include=(len(rel.parts)==1 and p.suffix in ('.md','.txt'))
    include|=rel.parts[0] in ('src','tests','scripts') and p.suffix=='.py'
    include|=rel.parts[0]=='figures' and p.suffix in ('.png','.svg')
    include|=rel.parts[0]=='results' and p.suffix in ('.csv','.md','.json')
    include|=str(rel).replace('\\','/') in ('data/PROVENANCE.md','data/raw/manifest.json','data/processed/audit.json')
    if include:selected.append(p)
manifest={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(selected)}
target=ROOT.parent/'finite-benchmark-research.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(selected):z.write(p,'research/'+str(p.relative_to(ROOT)).replace('\\','/'))
    z.writestr('research/ARCHIVE_MANIFEST.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    assert not any(n.endswith(('.npz','.jsonl','.zip')) for n in z.namelist())
    for rel,digest in manifest.items():assert hashlib.sha256(z.read('research/'+rel)).hexdigest()==digest
print(target,len(selected),'files',target.stat().st_size,'bytes')
