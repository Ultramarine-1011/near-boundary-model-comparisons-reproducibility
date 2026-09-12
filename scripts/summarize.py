from pathlib import Path
import json,os
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT / '.cache' / 'mplconfig')
from scipy.stats import beta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=ROOT/'results'; FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
def table(df):
 cols=list(df.columns)
 def fmt(x):return f'{x:.4f}' if isinstance(x,(float,np.floating)) else str(x)
 return '| '+' | '.join(cols)+' |\n|'+'|'.join(['---']*len(cols))+'|\n'+'\n'.join('| '+' | '.join(fmt(v) for v in row)+' |' for row in df.itertuples(index=False,name=None))+'\n'
def summarize(file,keys):
 df=pd.read_json(OUT/(file+'.jsonl'),lines=True)
 df['fraction']=df.n/df.N;df['census']=df.n==df.N
 g=df.groupby(keys,dropna=False)
 agg=g.agg(runs=('n','size'),cost_fraction=('fraction','mean'),median_fraction=('fraction','median'),
           errors=('error','sum'),error_rate=('error','mean'),census_fraction=('census','mean')).reset_index()
 if file=='simulation':
  coverage=g.coverage_failure.agg(['sum','mean']).reset_index().rename(columns={'sum':'coverage_failures','mean':'coverage_failure_rate'})
  agg=agg.merge(coverage,on=keys)
  # Per fixed population/method: independent random permutations, exact binomial CI.
  agg['error_cp_lower']=[0 if k==0 else beta.ppf(.025,k,n-k+1) for k,n in zip(agg.errors,agg.runs)]
  agg['error_cp_upper']=[1 if k==n else beta.ppf(.975,k+1,n-k) for k,n in zip(agg.errors,agg.runs)]
 agg.to_csv(OUT/(file+'_summary.csv'),index=False)
 return df,agg
sim,sa=summarize('simulation',['case','method','epsilon','alpha'])
real,ra=summarize('real',['dataset','method','epsilon'])
strat,sta=summarize('stratification',['dataset','strata','method'])
main=ra[(ra.epsilon==.02)&ra.method.isin(['eb_grid','eb_predictable','hoeffding_grid','serfling_spending','normal_peeking','separate_arm'])]
(OUT/'main_table.md').write_text(table(main[['dataset','method','runs','cost_fraction','error_rate','census_fraction']]),encoding='utf-8')
# Report conditional classes, rather than confusing aggregate ranking with equivalence.
real[real.epsilon==.02].groupby(['dataset','method','truth']).agg(runs=('n','size'),fraction=('fraction','mean'),error_rate=('error','mean')).reset_index().to_csv(OUT/'class_summary.csv',index=False)
# Cost uncertainty across model-pair cohort: pairs are clusters, permutations aren't models.
rows=[];rng=np.random.default_rng(78124)
for (dataset,method),g in real[real.epsilon==.02].groupby(['dataset','method']):
 vals=g.groupby('pair').fraction.mean().to_numpy()
 boots=rng.choice(vals,size=(5000,len(vals)),replace=True).mean(axis=1)
 rows.append(dict(dataset=dataset,method=method,pairs=len(vals),fraction=vals.mean(),bootstrap_lower=np.quantile(boots,.025),bootstrap_upper=np.quantile(boots,.975)))
pd.DataFrame(rows).to_csv(OUT/'pair_cluster_bootstrap.csv',index=False)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.bbox':'tight'})
fig,ax=plt.subplots(figsize=(9,4.4))
pivot=main[main.method.isin(['eb_grid','eb_predictable','hoeffding_grid','serfling_spending'])].pivot(index='dataset',columns='method',values='cost_fraction')
pivot.plot.bar(ax=ax);ax.set_ylabel('Mean fraction of pair-items evaluated');ax.set_xlabel('Released response matrix');ax.set_ylim(0,1.06);ax.legend(fontsize=8);plt.xticks(rotation=20)
fig.tight_layout();fig.savefig(FIG/'real_cost.png',dpi=180);fig.savefig(FIG/'real_cost.svg');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(10,4))
for method in ['eb_grid','eb_predictable','hoeffding_grid','serfling_spending','normal_peeking']:
 g=sim[(sim['case'].str.startswith('N5000_q0.3_'))&(sim.method==method)].groupby('delta').agg(cost=('fraction','mean'),err=('error','mean'))
 axes[0].plot(g.index,g.cost,'o-',label=method);axes[1].plot(g.index,g.err,'o-',label=method)
for ax in axes:
 ax.axvline(.02,color='gray',ls=':');ax.axvline(-.02,color='gray',ls=':');ax.set_xlabel('Actual finite-population difference')
axes[0].set_ylabel('Mean evaluated fraction');axes[1].set_ylabel('Decision error rate');axes[1].axhline(.05,color='black',ls='--');axes[0].legend(fontsize=7)
fig.tight_layout();fig.savefig(FIG/'boundary_cost_error.png',dpi=180);fig.savefig(FIG/'boundary_cost_error.svg');plt.close(fig)
baseline=strat[strat.method=='unstratified'][['dataset','pair','rep','fraction']].rename(columns={'fraction':'baseline_fraction'})
ratios=strat[strat.method!='unstratified'].merge(baseline,on=['dataset','pair','rep']);ratios['cost_ratio']=ratios.fraction/ratios.baseline_fraction
ratios.groupby(['dataset','strata','method']).agg(runs=('n','size'),cost_ratio=('cost_ratio','mean'),median_cost_ratio=('cost_ratio','median'),error_rate=('error','mean')).reset_index().to_csv(OUT/'stratification_ratios.csv',index=False)
stats={'simulation_runs':len(sim),'real_runs':len(real),'stratification_runs':len(strat),
 'max_certified_sim_error':float(sa[sa.method!='normal_peeking'].error_rate.max()),
 'max_normal_sim_error':float(sa[sa.method=='normal_peeking'].error_rate.max()),
 'eb_real_cost_fraction':float(real[(real.method=='eb_grid')&(real.epsilon==.02)].fraction.mean()),
 'eb_real_errors':int(real[(real.method=='eb_grid')&(real.epsilon==.02)].error.sum())}
(OUT/'headline.json').write_text(json.dumps(stats,indent=2),encoding='utf-8');print(json.dumps(stats,indent=2))
print(main[['dataset','method','cost_fraction','error_rate']].to_string(index=False))
