from run_experiments import simulation_cases,OUT,emit
from finite_eval import betting_decision
import numpy as np
with (OUT/'betting_simulation.jsonl').open('w',encoding='utf-8') as f:
 for c,(name,d,epsilon,alpha) in enumerate(simulation_cases()):
  for rep in range(1000):
   seed=2026090900+c*10000+rep
   stream=np.random.default_rng(seed).permutation(d)
   emit(f,dict(case=name,rep=rep,seed=seed,method='threshold_betting',epsilon=epsilon,alpha=alpha,**betting_decision(stream,epsilon,alpha)))
  print(name,flush=True)
