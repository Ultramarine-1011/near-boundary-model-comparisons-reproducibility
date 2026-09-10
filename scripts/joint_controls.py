from pathlib import Path
import json
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from finite_eval import betting_decision
from stratified_joint import joint_replay

with (ROOT/'results'/'joint_controls.jsonl').open('w',encoding='utf-8') as f:
    for p in sorted((ROOT/'data'/'processed').glob('*.npz')):
        z=np.load(p,allow_pickle=True)
        for pair,(a,b) in enumerate(z['pairs'][:20]):
            d=z['scores'][a].astype(float)-z['scores'][b]
            for rep in range(5):
                seed=2026092900+pair*1000+rep
                rows=[('joint_unstratified',joint_replay([d],seed=seed,batch=16)),
                      ('threshold_betting',betting_decision(np.random.default_rng(seed).permutation(d),.02,.05))]
                for method,result in rows:
                    f.write(json.dumps(dict(dataset=p.stem,pair=pair,rep=rep,seed=seed,method=method,**result))+'\n')
        print(p.stem,flush=True)
