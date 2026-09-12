import unittest,itertools,math,sys
from pathlib import Path
from fractions import Fraction
root=Path(__file__).resolve().parents[1];sys.path[:0]=[str(root/'scripts'),str(root/'src')]
from boundary_revision import planned_gaussian

class BoundaryRevisionTests(unittest.TestCase):
 def test_capacity_subsets_change_label(self):
  eps=Fraction(1,5)
  label=lambda d:'A' if d>eps else 'B' if d< -eps else 'E'
  for d in itertools.product((-1,0,1),repeat=5):
   delta=Fraction(sum(d),5);gap=abs(abs(delta)-eps)
   sign=1 if delta< -eps or 0<=delta<=eps else -1
   for h in (1,2):
    eligible=[i for i,x in enumerate(d) if 1-sign*x>=h]
    k=math.floor(5*gap/h)+1
    if k>len(eligible):continue
    for ids in itertools.combinations(eligible,k):
     alt=list(d)
     for i in ids:alt[i]=sign
     self.assertNotEqual(label(delta),label(Fraction(sum(alt),5)))
 def test_sufficient_upper_bound_radius(self):
  for n in (10,100,1000,10000):
   L=math.log(2*n/.05)
   for gap in (.001,.01,.1,.5,1):
    t=min(n,math.floor(8*L*(n+1)/(n*gap**2+8*L))+1)
    if t<n:self.assertLess(2*math.sqrt(2*(1-(t-1)/n)*L/t),gap)
 def test_planned_gaussian_rare_event_enumeration(self):
  errors=0
  for i in range(100):
   d=[0.]*100;d[i]=1.
   errors+=planned_gaussian(d,.005)['error']
  self.assertEqual(errors,80)
