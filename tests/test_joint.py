import itertools
import sys
import unittest
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT.parents[1] / 'work' / 'deps'))
from stratified_joint import extreme, joint_replay
from scipy.optimize import linprog


class JointTests(unittest.TestCase):
    def test_nuisance_optimization_against_independent_lp(self):
        rng = np.random.default_rng(304)
        for _ in range(150):
            h = int(rng.integers(2, 15))
            w = rng.dirichlet(np.ones(h))
            lo = rng.random(h)
            hi = lo + (1-lo)*rng.random(h)
            a = rng.random(h)*100
            bound = float(w@lo + rng.random()*(w@(hi-lo)))
            for maximize in (False, True):
                sign = -1 if maximize else 1
                reference = linprog(sign*a, A_eq=w[None, :], b_eq=[bound],
                                    bounds=list(zip(lo, hi)), method='highs')
                self.assertTrue(reference.success)
                self.assertAlmostEqual(extreme(a,w,lo,hi,bound,maximize),
                                       sign*reference.fun, places=7)

    def test_small_strata_all_populations(self):
        # Uniform random permutations are generated exactly by independent,
        # exhaustive stream orders. Permuting each input by seed zero is a
        # bijection, so grouping results by the two input histograms preserves
        # the correct conditional sampling law for every finite population.
        for allocation in ('proportional', 'neyman'):
            counts = {}; errors = {}
            for seq in itertools.product((-1.,0.,1.), repeat=6):
                key = tuple(tuple(seq[j:j+3].count(v) for v in (-1.,0.,1.))
                            for j in (0,3))
                result = joint_replay([seq[:3], seq[3:]], epsilon=.15,
                                      alpha=.2, seed=0, allocation=allocation, batch=1)
                counts[key] = counts.get(key,0)+1
                errors[key] = errors.get(key,0)+result['error']
                self.assertLessEqual(result['n'],6)
            self.assertLessEqual(max(errors[k]/counts[k] for k in counts),.2)


if __name__ == '__main__':
    unittest.main()
