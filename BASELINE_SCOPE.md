# Closest-method audit and comparison scope

Checked 2026-09-09. This record separates reproduction of an inference construction from reproduction of an entire published evaluation pipeline. None of the results establish state-of-the-art performance.

## CELEUS

[The paper](https://arxiv.org/html/2606.20820v1), Appendix D.4, uses predictable betting fractions, global signal scaling, a sampling-probability floor, and a precision stopping target. Our implementation uses its finite-pool residual-correction identity, but fixed-grid directional betting, per-round predictable scaling, and a ternary decision target. The existing nearest-history predictor is a local choice, not the paper's small-language-model surrogate. Searching the paper links and a targeted author/title/GitHub query did not locate an author implementation; that search result does not prove none exists.

The initial prediction comparison changes only predictor and weights while holding our signal-based inference implementation fixed. A follow-up adds a historical-only low-rank predictor, with 512 fitting rows and 64 validation rows, all disjoint from test-model IDs. A 64-item target pilot is charged. Ranks 0/4/8/16/32 and ridge penalties .1/1/10/100 are selected by held-out historical prediction MSE, never target stopping cost. Rank zero retains an intercept and historical item means. Predictions and residual-based sampling weights are then frozen. Uniform and weighted variants are reported together, without choosing a winner using test responses. This squared-loss predictor is not PULSE's logistic factorization.

## PULSE

[Author repository](https://github.com/elad-tolo/pulse-llm-eval), inspected at commit `d9a01db4a53de2068c7bd9fc2fee7c087f923cee`. Read `bandit.py`, `bandit_si.py`, the selected configuration files and README; source checksums are retained in the local research cache. The implementation uses logistic matrix factorization with historical question factors and online test-model fitting. It evaluates fixed-budget best-arm identification, with 1,000 candidate models. The paper's Theorem 1 is a fixed-step bound and Theorem 2 addresses budget-T identification. Reading those statements does not justify treating their displayed intervals as our alpha-correct equivalence stopping rule. Their published best-arm accuracy/cost figures therefore cannot be compared directly to our three-label stopping fractions. The low-rank follow-up tests the relevant predictor mechanism under a common valid inference layer, and is explicitly an adaptation.

## Stratified inference

The separate-CS and joint union-intersection methods are established constructions specialized to paired scores. Joint inference is compared with a one-stratum control using the same 16-item inspection schedule, plus direct uniform betting. This prevents attributing the separate-CS alpha-splitting overhead to all stratified methods. Estimated-Neyman allocation is a heuristic for this sequential objective, not an oracle or optimal policy.

## Other stopping targets

Group-sequential equivalence is directly relevant prior art (Arviv et al.; Jennison–Turnbull). Approximate Gaussian calibration is not relabeled as finite-sample anytime validity. SySRs targets fixed-budget identification; ATLAS targets latent-ability precision; Bayesian methods quantify posterior uncertainty. They belong in the scientific comparison, but their error metrics and budgets are not interchangeable with conditional finite-vector decision risk.

An additional search found [Kato, Sequential Audit Sampling with Statistical Guarantees](https://arxiv.org/html/2604.06116v1). Its abstract and setup describe binary finite-population testing with an indifference region and exact hypergeometric calibration. This reinforces the need to distinguish our closed equivalence region from an indifference region. A full lower-bound priority audit remains separate from the methodological overlap check; no priority claim is made for the elementary coupling argument.

## Boundary revision: closest application and target audit

Read [Arviv et al. v1](https://arxiv.org/html/2607.08522v1) and author source at commit `2c44ed23d2a8df2b42a036c9dc639bb71c0c07d5`: `sequential_rules.py`, `sequential_engines.py`, and `case_studies_pairwise_separability.py`. Their cost-versus-difference analysis already addresses difficulty-dependent cost. Efficacy excludes zero; equivalence contains the CI within the margin; the case study orders efficacy before equivalence. These overlapping claims differ from our disjoint practical-superiority regions. Their engine also rejects nonpositive aggregate variance.

Decision: do not report an original-author head-to-head by relabeling these stop reasons. Compare direct betting and EB-grid on identical populations and permutations; add a clearly named planned Gaussian–Bonferroni diagnostic under our target. The diagnostic allows zero-width intervals and is not the authors' engine. Its rare-event failure cannot be attributed to their implementation. A target-harmonized original-pipeline study remains an explicit limitation; no cost dominance over Arviv is claimed.

The new [Shekhar–Ramdas rate-function paper](https://arxiv.org/html/2603.14423v1), especially Theorem 3.4, is relevant prior for instance-dependent fixed-sample WoR interval lower bounds. Our adaptive label-query coupling is narrower and elementary; it does not subsume that theory.

## 10 September: auditing comparators and evidence placement

Added Kato–Nakagawa v2, RiLACS and weighted financial auditing to main related work. Binary indifference-region audit decisions, assertion-oriented risk control, and three mutually exclusive labels are related but have distinct loss definitions. Generic constructions can be adapted; the manuscript does not treat these differences as proof of superior efficiency. No new author-pipeline comparison was run. The Gaussian diagnostic is now entirely supplementary (Appendix D); the main figure uses direct betting on existing controlled populations and separately identified random/stress public cohorts.
