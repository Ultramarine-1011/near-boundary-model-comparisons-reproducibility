from pathlib import Path
import sys,os
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parents[1]/'work'/'deps'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache'/'matplotlib'))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out=ROOT/'results';figdir=ROOT/'figures';figdir.mkdir(exist_ok=True)
names=['arc','composite','gsm8k','hellaswag','mmlu-pro','truthfulqa','winogrande']
labels=['ARC','Composite','GSM8K','HellaSwag','MMLU-Pro','TruthfulQA','WinoGrande']
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,3,figsize=(13,4.8),sharey=True)
y=np.arange(7)
close=pd.read_csv(out/'close_pairs_summary.csv')
for cohort,label,color,offset in [('top_adjacent','Top-adjacent','#0072B2',-.10),('margin_nearest','Margin-nearest','#D55E00',.10)]:
    row=close[(close.method=='threshold_betting')&(close.cohort==cohort)].set_index('dataset').loc[names]
    axes[0].scatter(row.fraction,y+offset,label=label,color=color,s=32)
axes[0].set(title='A. Close-pair diagnostics',xlabel='Mean evaluated fraction',xlim=(0,1.05))
joint=pd.read_csv(out/'joint_stratification_summary.csv')
controls=pd.read_csv(out/'joint_controls_summary.csv')
for method,label,color,offset in [('joint_unstratified','Joint: no strata','#0072B2',-.13),('threshold_betting','Direct betting','#009E73',0)]:
    row=controls[controls.method==method].set_index('dataset').loc[names]
    axes[1].scatter(row.fraction,y+offset,label=label,color=color,s=32)
row=joint[(joint.method=='joint_proportional')&(joint.strata=='difficulty4')].set_index('dataset').loc[names]
axes[1].scatter(row.fraction,y+.13,label='Joint: 4 difficulty strata',color='#D55E00',s=32)
axes[1].set(title='B. Matched inference controls',xlabel='Mean evaluated fraction',xlim=(0,1.05))
diff=pd.read_csv(out/'lowrank_paired_cost.csv')
for method,label,color,offset in [('signal_uniform_lowrank','Uniform low-rank','#0072B2',-.12),('signal_weighted_lowrank','Weighted low-rank','#D55E00',.12)]:
    row=diff[diff.method==method].set_index('dataset').loc[names]
    axes[2].errorbar(row.difference,y+offset,xerr=np.vstack([row.difference-row.cluster_bootstrap_lower,row.cluster_bootstrap_upper-row.difference]),fmt='o',label=label,color=color,markersize=4,capsize=2)
axes[2].axvline(0,color='.5',linestyle='--',linewidth=1)
axes[2].set(title='C. Predictor cost differences',xlabel='Fraction minus constant-predictor control')
axes[0].set_yticks(y,labels);axes[0].invert_yaxis()
for ax in axes:
    ax.grid(axis='x',alpha=.2);ax.legend(loc='upper center',bbox_to_anchor=(.5,-.16),frameon=False,fontsize=8)
fig.suptitle('Supplementary comparisons use distinct, explicitly matched cohorts',fontsize=11)
fig.tight_layout(rect=(0,.05,1,.95))
for extension in ('png','svg'):fig.savefig(figdir/f'followup_costs.{extension}',dpi=180,bbox_inches='tight')
plt.close(fig)
print('followup_costs.png and .svg written')
