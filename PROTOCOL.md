# Locked initial experimental protocol

Written before examining real-data stopping results. Changes will be logged.

## Target and outcomes

Fix scores in [0,1] and paired differences d_i in [-1,1]. The estimand is the item-weighted finite mean. With a predeclared margin epsilon, A means delta > epsilon, E means -epsilon <= delta <= epsilon, and B means delta < -epsilon. This is practical superiority; it is deliberately different from detecting any positive difference. Continue is an internal state, never evidence for E. Exhaustion returns the exact label.

## Comparators

Full census; deterministic bounded completions; Waudby-Smith–Ramdas Hoeffding and empirical-Bernstein WoR confidence sequences with a prespecified finite bet grid and Bonferroni allocation over bets; the original predictable empirical-Bernstein schedule; fixed-look Hoeffding–Serfling with error spending at geometric checkpoints; and a deliberately uncertified repeatedly inspected normal interval. Paired differences are used by all certification comparators. Separate-arm CS is an ablation. Fixed-budget plug-in decisions are reported separately, including their error rate; they are not treated as equivalent guarantees.

Stratification: fixed stratum weights, uniform draws within each selected stratum, Bonferroni simultaneous stratum CS, with proportional and predictable estimated-Neyman allocation. The latter is a heuristic. It has valid coverage through the component CS, but no optimal cost theorem is claimed. Include a bad/random stratification control and varying numbers of strata. No unobserved evaluation score enters allocation.

## Simulation

Fixed finite populations, random permutations only; paired disagreement rates and mean differences varied independently where feasible. Include zero variance, rare disagreement, high disagreement, exact positive/negative margin boundaries, one-item changes across boundaries, heterogeneous strata, and misleading strata. Compare alpha in {0.01,0.05,0.10}, margins in {0.01,0.02,0.05}, and benchmark sizes including 200, 1000, and 5000. Use a pilot for correctness/runtime; final seed bank independent of pilot. Report complete-path CS coverage, terminal decision error, mean and quantiles of cost, fraction reaching census, and class-conditioned results.

Binomial uncertainty for Monte Carlo errors must be reported. Zero observed errors is not a proof of zero risk. Include exact small-population enumeration and martingale conditional-factor checks independent of the Monte Carlo study.

## Public data

Prefer released complete response matrices, preserving published item IDs and source licenses. Candidate sources: ATLAS (five benchmarks) and efficiently-evaluating-llms (MMLU-Pro and a multi-task composite). Main model-pair selection uses a fixed random seed independent of observed performance. Any gap-selected or same-family subset is a separately labeled diagnostic. Remove incomplete model rows under a declared complete-case rule; never silently score missing as incorrect. Historical models used for predictors or difficulty strata must be disjoint from tested models. Record exclusions and exact hashes.

Report pair-item evaluations and model calls separately (normally two calls per new pair-item). Cached full matrices support offline counterfactual cost; they do not save the already-incurred collection cost. Without item-token logs, dollar savings are not identified. Synthetic heterogeneous costs are labeled as such.

## Claim restrictions

No distribution-free population generalization, stochastic-generation inference, family-wide model selection guarantee, or superior adaptive allocation claim without corresponding proof/evidence. No new-method novelty claim for the decision wrapper. Stronger prediction-assisted and union-intersection comparators remain required before a broad state-of-the-art cost claim.
