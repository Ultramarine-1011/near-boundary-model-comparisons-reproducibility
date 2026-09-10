from pathlib import Path
import sys,os,json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parents[1]/'work/deps'))
from scipy.stats import beta
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=ROOT/'results';d=pd.read_json(out/'boundary_revision.jsonl',lines=True)
assert len(d)==66600 and not d.duplicated(['case','rep','method']).any()
assert (d.groupby(['case','method']).size()==300).all()
d['fraction']=d.n/d.N
s=d.groupby(['case','N','q','gap','delta','epsilon','variance','method']).agg(runs=('n','size'),fraction=('fraction','mean'),errors=('error','sum')).reset_index()
s['error_upper']=[beta.ppf(.975,k+1,n-k) if k<n else 1 for k,n in zip(s.errors,s.runs)]
s.to_csv(out/'boundary_revision_summary.csv',index=False)
print(s[s.case.str.startswith('rare')][['case','method','fraction','errors','error_upper']].to_string(index=False))
print(s[(s.N==5000)&(s.method=='direct_betting')][['case','gap','fraction']].to_string(index=False))
fig,axes=plt.subplots(2,2,figsize=(11,7.6))
ax=axes.ravel()
for N,axis in zip((1000,5000),ax[:2]):
 for q in (.05,.3,.8):
  z=s[(s.N==N)&np.isclose(s.q,q)&(s.method=='direct_betting')&s.case.str.startswith('N')].sort_values('delta')
  assert len(z)>=9
  axis.plot(z.delta-.02,z.fraction,'o-',label=f'q={q}',markersize=3)
 z=s[(s.N==N)&s.case.str.startswith('constant')&(s.method=='direct_betting')].sort_values('delta')
 axis.plot(z.delta-.02,z.fraction,'s--',color='black',label='Constant scores',markersize=3)
 axis.axvline(0,color='.5',linestyle=':');axis.set(title=f'Controlled populations: N={N}',xlabel='Signed distance to +epsilon (delta - epsilon)',ylim=(0,1.04));axis.legend(fontsize=8)
 axis.text(.02,.04,'Equivalent side | boundary at 0 | A side',transform=axis.transAxes,fontsize=8)
pair_tables=[]
for axis,filename,cohort,reps,pairs in ((ax[2],'betting_real','random',30,700),(ax[3],'close_pairs','margin_nearest',100,140)):
 r=pd.read_json(out/f'{filename}.jsonl',lines=True)
 if cohort!='random':r=r[r.cohort==cohort]
 r=r[r.method=='threshold_betting'].copy()
 assert np.allclose(r.epsilon,.02) and np.allclose(r.alpha,.05)
 assert not r.duplicated(['dataset','pair','rep']).any()
 assert (r.groupby(['dataset','pair']).size()==reps).all()
 r['fraction']=r.n/r.N
 p=r.groupby(['dataset','pair']).agg(delta=('delta','first'),epsilon=('epsilon','first'),fraction=('fraction','mean'),N=('N','first'),runs=('n','size')).reset_index()
 assert len(p)==pairs and p.dataset.nunique()==7
 p['gap']=abs(abs(p.delta)-p.epsilon);p['cohort']=cohort;pair_tables.append(p)
 for j,name in enumerate(sorted(p.dataset.unique())):
  z=p[p.dataset==name]
  axis.scatter(z.gap,z.fraction,s=13,alpha=.65,color=plt.get_cmap('tab10')(j),label=name)
 axis.set_xscale('symlog',linthresh=1e-5)
 axis.set(xlim=(0,1),ylim=(0,1.04),xlabel='Decision gap g = ||delta| - epsilon|',title=f'{"Random pairs" if cohort=="random" else "Margin-nearest stress test"}: {pairs} pairs')
 axis.set_xticks([0,.0001,.001,.01,.1,1],['0','0.0001','0.001','0.01','0.1','1'])
 if cohort=='random':axis.legend(fontsize=7,ncol=2,loc='lower left')
for axis in (ax[0],ax[2]):axis.set_ylabel('Mean fraction evaluated, direct betting')
pd.concat(pair_tables,ignore_index=True).to_csv(out/'boundary_figure_pairs.csv',index=False)
fig.tight_layout()
for ext in ('png','pdf'):fig.savefig(ROOT/'figures'/f'boundary_revision.{ext}',dpi=180)
plt.close(fig)
fig,axis=plt.subplots(figsize=(5,3.8))
colors={'eb_grid':'#0072B2','direct_betting':'#009E73','planned_gaussian':'#D55E00'}
display_names={'eb_grid':'EB grid','direct_betting':'Direct betting','planned_gaussian':'Gaussian diagnostic'}
rare=s[s.case.str.startswith('rare')]
for method,color in colors.items():
 z=rare[rare.method==method]
 axis.scatter(z.fraction,z.errors/z.runs,color=color,label=display_names[method])
axis.axhline(.05,color='.5',linestyle=':');axis.set(xlabel='Mean evaluated fraction',ylabel='Decision error frequency',title='Rare-event calibration diagnostic',ylim=(-.02,1.02));axis.legend(fontsize=7)
fig.tight_layout()
for ext in ('png','pdf'):fig.savefig(ROOT/'figures'/f'gaussian_diagnostic.{ext}',dpi=180)
plt.close(fig)
