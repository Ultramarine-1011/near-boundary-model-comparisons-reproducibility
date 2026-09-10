import unittest,itertools,math,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from finite_eval import cs_path,stop_from_path,label,decide,stratified_replay,betting_decision
from prediction_eval import signal_betting

class CoreTests(unittest.TestCase):
 def test_prediction_signal_conditional_mean(self):
  rng=np.random.default_rng(4201)
  for _ in range(1000):
   x=rng.random(9);p=rng.random(9);q=rng.dirichlet(np.ones(6))
   base=(x[:3].sum()+p[3:].sum())/9
   y=base+(x[3:]-p[3:])/(9*q)
   self.assertAlmostEqual(float(q@y),float(x.mean()),places=12)
   low=base-np.max(p[3:]/(9*q));high=base+np.max((1-p[3:])/(9*q))
   self.assertTrue(np.all(y>=low-1e-12));self.assertTrue(np.all(y<=high+1e-12))
 def test_prediction_replay_deterministic(self):
  d=np.r_[np.ones(60),-np.ones(30),np.zeros(10)]
  kwargs=dict(d=d,prediction=np.linspace(.1,.9,100),weights=np.linspace(.01,2,100),epsilon=.02,alpha=.05,seed=42,pilot_indices=[0,1,99])
  self.assertEqual(signal_betting(**kwargs),signal_betting(**kwargs))
  self.assertLessEqual(signal_betting(**kwargs)['n'],100)
 def test_betting_decision_exact_enumeration(self):
  total={};errors={}
  for seq in itertools.product([-1,0,1],repeat=8):
   key=(seq.count(-1),seq.count(0),seq.count(1))
   total[key]=total.get(key,0)+1
   r=betting_decision(seq,.125,.2)
   errors[key]=errors.get(key,0)+r['error']
  self.assertLessEqual(max(errors[k]/total[k] for k in total),.2)
 def test_hypergeometric_lower_bound_algebra(self):
  for N in range(2,21):
   for k in range(1,N+1):
    for t in range(N+1):
     exact=math.comb(N-t,k)/math.comb(N,k) if N-t>=k else 0.
     bound=max(1-t/(N-k+1),0.)**k
     self.assertGreaterEqual(exact+1e-14,bound)
 def test_input_and_labels(self):
  for x in ([],[np.nan],[2],[[0]]):
   with self.assertRaises(ValueError):cs_path(x)
  self.assertEqual(label(.02,.02),'E');self.assertEqual(label(-.02,.02),'E')
  self.assertEqual(decide(.1,-.1,.02),'C')
 def test_prefix_measurability(self):
  for method in ('eb_grid','hoeffding_grid','eb_predictable','serfling_spending'):
   a=cs_path([0,1,-1,0,1,0],method=method)
   b=cs_path([0,1,-1,-1,-1,1],method=method)
   np.testing.assert_array_equal(a[0][:3],b[0][:3]);np.testing.assert_array_equal(a[1][:3],b[1][:3])
 def test_completion_contains_exact(self):
  for seq in itertools.product([-1,0,1],repeat=6):
   lo,hi=cs_path(seq,method='completion')
   self.assertTrue(np.all(lo<=np.mean(seq)+1e-12));self.assertTrue(np.all(hi>=np.mean(seq)-1e-12))
 def test_exact_small_population_coverage(self):
  # Enumerate every ternary length-7 ordering; conditional on counts all unique
  # orderings are equiprobable. This checks every ternary population of size 7.
  for method in ('eb_grid','hoeffding_grid','eb_predictable','serfling_spending'):
   totals={};fails={}
   for seq in itertools.product([-1,0,1],repeat=7):
    key=(seq.count(-1),seq.count(0),seq.count(1))
    totals[key]=totals.get(key,0)+1
    lo,hi=cs_path(seq,alpha=.1,method=method)
    failure=np.any(lo>np.mean(seq)+1e-12) or np.any(hi<np.mean(seq)-1e-12)
    fails[key]=fails.get(key,0)+int(failure)
   self.assertLessEqual(max(fails[k]/totals[k] for k in totals),.1)
 def test_empirical_bernstein_conditional_factor(self):
  # Independent conditional-MGF check; does not call the implementation.
  rng=np.random.default_rng(123)
  for _ in range(2000):
   values=rng.random(8);p=rng.dirichlet(np.ones(8));m=p@values
   prediction=rng.random();lam=rng.uniform(.001,.95)
   for sign in (-1,1):
    factor=np.exp(sign*lam*(values-m)-(-np.log1p(-lam)-lam)*(values-prediction)**2)
    self.assertLessEqual(float(p@factor),1+1e-12)
 def test_census_boundary_and_symmetry(self):
  for d in (np.zeros(100),np.full(100,.02),np.r_[np.ones(51),-np.ones(49)]):
   lo,hi=cs_path(d,method='completion')
   r=stop_from_path(d,lo,hi,.02)
   self.assertLessEqual(r['n'],len(d));self.assertEqual(r['error'],0)
   l2,h2=cs_path(-d,method='completion')
   np.testing.assert_allclose(lo,-h2,atol=1e-11)
   np.testing.assert_allclose(hi,-l2,atol=1e-11)
 def test_stratified_exhaustion(self):
  r=stratified_replay([np.ones(10),-np.ones(10)],0,.05,123,'neyman')
  self.assertEqual(r['n'],20);self.assertEqual(r['decision'],'E');self.assertEqual(r['error'],0)

if __name__=='__main__':unittest.main(verbosity=2)
