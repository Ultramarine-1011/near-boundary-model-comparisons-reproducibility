"""Single sequential reproduction entry point. Requires installed dependencies."""
from pathlib import Path
import argparse,json,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--full',action='store_true',help='rebuild matrices and every experiment before checking');args=p.parse_args()
steps=[['-m','unittest','discover','-s','tests','-v']]
if args.full:
 steps += [['scripts/download_data.py'],['scripts/prepare_data.py'],
           ['scripts/run_experiments.py','simulation','--reps','1000'],
           ['scripts/run_experiments.py','real','--reps','30','--pairs','100'],
           ['scripts/run_experiments.py','stratification','--reps','5','--pairs','20']]
 steps += [[f'scripts/{s}.py'] for s in ('additional_experiments','betting_simulation','prediction_experiments','lowrank_experiments','cost_experiments','close_pair_experiments','joint_stratification_experiments','joint_controls','boundary_revision')]
steps += [[f'scripts/{s}.py'] for s in ('summarize','summarize_additional','summarize_followups','summarize_joint','summarize_lowrank','plot_followups','summarize_boundary_revision','audit_results','audit_targets','build_manuscript')]
report=[];out=ROOT/'results';out.mkdir(exist_ok=True)
for step in steps:
 print('Running:', ' '.join(step),flush=True);start=time.time()
 result=subprocess.run([sys.executable,*step],cwd=ROOT,check=False)
 report.append(dict(arguments=step,returncode=result.returncode,elapsed_seconds=time.time()-start))
 (out/'reproduction_run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 if result.returncode:raise SystemExit(result.returncode)
print('All documented reproduction steps passed.',flush=True)
