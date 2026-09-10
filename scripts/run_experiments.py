"""Reproducible simulation and public-matrix replay. No external model calls."""
from pathlib import Path
import sys,json,argparse,time,csv,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from finite_eval import cs_path,stop_from_path,stratified_replay,label
METHODS=['eb_grid','eb_predictable','hoeffding_grid','serfling_spending','completion','normal_peeking']
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)

def emit(f,row):f.write(json.dumps(row,separators=(',',':'))+'\n')
def population(N,q,delta):
    # Counts fixed before random sampling: target is actual finite mean.
    pos=int(round(N*(q+delta)/2));neg=int(round(N*(q-delta)/2))
    if min(pos,neg)<0 or pos+neg>N:raise ValueError('infeasible population')
    return np.r_[np.ones(pos),-np.ones(neg),np.zeros(N-pos-neg)]

def simulation_cases():
    cases=[]
    for N in (200,1000,5000):
        for q in (.05,.3,.8):
            for delta in (0,.018,.02,.022,-.02,.04):
                cases.append((f'N{N}_q{q}_d{delta}',population(N,q,delta),.02,.05))
    for alpha in (.01,.10):
        for delta in (0,.02,.08):cases.append((f'alpha{alpha}_d{delta}',population(1000,.3,delta),.02,alpha))
    for eps in (.01,.05):
        for delta in (0,eps,2*eps):cases.append((f'eps{eps}_d{delta}',population(1000,.3,delta),eps,.05))
    cases.extend([('constant_equivalent',np.zeros(1000),.02,.05),('constant_boundary',np.full(1000,.02),.02,.05),('one_changed',np.r_[np.full(999,.02),1.],.02,.05)])
    return cases

def simulation(reps):
    cases=simulation_cases()
    with (OUT/'simulation.jsonl').open('w',encoding='utf-8') as f:
        for c,(name,d,eps,alpha) in enumerate(cases):
            for rep in range(reps):
                seed=2026090900+c*10000+rep;stream=np.random.default_rng(seed).permutation(d)
                for method in METHODS:
                    lo,hi=cs_path(stream,alpha,method)
                    emit(f,dict(study='simulation',case=name,rep=rep,seed=seed,method=method,epsilon=eps,alpha=alpha,
                                **stop_from_path(stream,lo,hi,eps)))
            print('simulation',c+1,len(cases),name,flush=True)

def real(reps,pairs):
    with (OUT/'real.jsonl').open('w',encoding='utf-8') as f:
        for p in sorted((ROOT/'data'/'processed').glob('*.npz')):
            data=np.load(p,allow_pickle=True);scores=data['scores']
            for pair,(ia,ib) in enumerate(data['pairs'][:pairs]):
                d=scores[ia].astype(float)-scores[ib]
                for rep in range(reps):
                    seed=2026091900+pair*1000+rep
                    order=np.random.default_rng(seed).permutation(len(d));stream=d[order]
                    for method in METHODS:
                        lo,hi=cs_path(stream,.05,method)
                        for eps in (.01,.02,.05):
                            emit(f,dict(study='real',dataset=p.stem,pair=pair,model_a=str(data['models'][ia]),model_b=str(data['models'][ib]),
                                        rep=rep,seed=seed,method=method,epsilon=eps,alpha=.05,disagreement=float(np.mean(d*d)),
                                        **stop_from_path(stream,lo,hi,eps)))
                    # Separate-arm intervals at alpha/2 each; same pair-item cost.
                    la,ua=cs_path(2*scores[ia][order]-1,.025,'eb_grid')
                    lb,ub=cs_path(2*scores[ib][order]-1,.025,'eb_grid')
                    emit(f,dict(study='real',dataset=p.stem,pair=pair,rep=rep,seed=seed,method='separate_arm',epsilon=.02,alpha=.05,
                                **stop_from_path(stream,(la-ub)/2,(ua-lb)/2,.02)))
                    # Fixed-budget plug-in classifiers: no certification claimed.
                    for frac in (.1,.25,.5):
                        n=math.ceil(len(d)*frac);truth=label(float(np.mean(d)),.02);verdict=label(float(np.mean(stream[:n])),.02)
                        emit(f,dict(study='real',dataset=p.stem,pair=pair,rep=rep,seed=seed,method=f'fixed_plugin_{frac}',epsilon=.02,alpha=.05,
                                    n=n,N=len(d),decision=verdict,truth=truth,error=int(verdict!=truth),cost=n,delta=float(np.mean(d))))
            print('real',p.stem,'pairs',min(pairs,len(data['pairs'])),'reps',reps,flush=True)

def stratification(reps,pairs):
    with (OUT/'stratification.jsonl').open('w',encoding='utf-8') as f:
        for p in sorted((ROOT/'data'/'processed').glob('*.npz')):
            data=np.load(p,allow_pickle=True);scores=data['scores'];N=scores.shape[1]
            definitions={}
            if len(np.unique(data['strata']))>1:definitions['task']=data['strata']
            if 'difficulty' in data:
                order=np.argsort(data['difficulty'],kind='stable')
                for h in (2,4,8):
                    groups=np.empty(N,dtype=int)
                    for k,ids in enumerate(np.array_split(order,h)):groups[ids]=k
                    definitions[f'difficulty{h}']=groups
            rand=np.random.default_rng(12345).permutation(N)%4;definitions['random4']=rand
            for pair,(ia,ib) in enumerate(data['pairs'][:pairs]):
                d=scores[ia].astype(float)-scores[ib]
                for rep in range(reps):
                    seed=2026092900+pair*1000+rep
                    stream=np.random.default_rng(seed).permutation(d)
                    emit(f,dict(dataset=p.stem,pair=pair,rep=rep,seed=seed,strata='none',method='unstratified',epsilon=.02,alpha=.05,
                                **stop_from_path(stream,*cs_path(stream),.02)))
                    for name,s in definitions.items():
                        groups=[d[s==k] for k in np.unique(s)]
                        for allocation in ('proportional','neyman'):
                            emit(f,dict(dataset=p.stem,pair=pair,rep=rep,seed=seed,strata=name,method=allocation,epsilon=.02,alpha=.05,
                                        **stratified_replay(groups,.02,.05,seed,allocation)))
            print('stratification',p.stem,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('study',choices=['simulation','real','stratification'])
    parser.add_argument('--reps',type=int,default=1000);parser.add_argument('--pairs',type=int,default=100)
    args=parser.parse_args();start=time.time()
    if args.study=='simulation':simulation(args.reps)
    elif args.study=='real':real(args.reps,args.pairs)
    else:stratification(args.reps,args.pairs)
    (OUT/(args.study+'_run.json')).write_text(json.dumps(dict(arguments=vars(args),elapsed_seconds=time.time()-start,numpy=np.__version__,python=sys.version),indent=2),encoding='utf-8')
