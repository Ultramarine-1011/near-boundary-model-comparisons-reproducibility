import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from lowrank_predictor import basis_from_history,predict,select_hyperparameters

class LowRankTests(unittest.TestCase):
 def test_known_low_rank_signal_recovery(self):
  rng=np.random.default_rng(8)
  feature=np.linspace(-1,1,120)
  history=.5+rng.uniform(-.3,.3,64)[:,None]*feature
  mean,basis=basis_from_history(history,max_rank=1)
  target=.5+.22*feature;pilot=np.arange(0,120,4)
  forecast=predict(mean,basis,pilot,target[pilot],rank=1,ridge=1e-8)
  self.assertLess(float(np.max(np.abs(forecast-target))),1e-8)
 def test_historical_validation_selection(self):
  rng=np.random.default_rng(48)
  history=rng.binomial(1,.6,size=(40,100))
  mean,basis=basis_from_history(history,max_rank=4)
  validation=rng.binomial(1,.6,size=(20,100))
  best,weights,table=select_hyperparameters(mean,basis,validation,pilot_size=20)
  self.assertEqual(best['mse'],min(row['mse'] for row in table))
  self.assertTrue(np.isfinite(weights).all());self.assertTrue((weights>=.05).all())

if __name__=='__main__':unittest.main()
