# Novelty audit — provisional, 2026-09-08

## Verdict

**The basic proposed combination is substantially enabled by established methods. It does not, by itself, justify a new-method paper.** We have not established that a single LLM paper has exactly the full requested specification; this is weaker than proving novelty. The mathematical reduction already follows from finite-population confidence sequences and classical sequential equivalence testing.

For fixed scores, apply an existing without-replacement CS to `(score_A - score_B + 1)/2`, transform it back, and stop when it lies inside one of the three predeclared regions. Correctness follows on the simultaneous coverage event. Adding an equivalence label is not a new confidence-sequence construction.

## Closest sources and concrete overlap

| Work | Relevant content | Difference or implication |
|---|---|---|
| [Waudby-Smith & Ramdas, 2020](https://arxiv.org/abs/2006.04347) | WoR bounded and categorical CS; composite null inversion; boundary-focused tuning | Supplies the central inference machinery; pairing is a change of variable. |
| [Jennison & Turnbull, 1993](https://researchportal.bath.ac.uk/en/publications/sequential-equivalence-testing-and-repeated-confidence-intervals-/) | Sequential equivalence with repeated confidence intervals | Equivalence plus sequential inference is long-established. |
| [Spertus, Sridhar & Stark, 2026 revision](https://arxiv.org/abs/2409.06680) | Sequential stratified finite-population tests; adaptive allocation; nuisance optimization; simple combined CS baseline | Stratification and allocation are not new contributions here. |
| [Tolochinsky et al., 2026, PULSE](https://arxiv.org/abs/2605.10405) | Fixed matrix; adaptive model allocation; WoR; prediction-assisted valid inference | Fixed-budget best-model objective, rather than equivalence certification; must not be called an anytime stopping baseline without checking its calibration. |
| [Lyu et al., 2026, SySRs](https://arxiv.org/abs/2606.07726) | Paired comparisons exploiting similarity for best-model identification | Pairing and similarity are explicitly prior art; fixed-budget identification differs from our stopping objective. |
| [Zhou et al., 2026, CELEUS](https://arxiv.org/abs/2606.20820) | Anytime-valid finite-pool inference; uncertainty-guided WoR sampling; surrogate correction | A very close inference framework. A pairwise score can be treated as a bounded loss. |
| [Hsu & Shekhar, 2026](https://arxiv.org/abs/2607.17409) | CS and active querying using past-model predictions; explicit mismatch and sampling concentration analysis | Defined target is average success probability. Already observes uniform querying can outperform adaptive querying. |
| [Neuhof & Benjamini, 2026](https://arxiv.org/abs/2607.16259) | Ranking uncertainty, subject heterogeneity, choice of inferential population | Distinguish fixed-benchmark design uncertainty from generalization across subjects. |
| [Li et al., ATLAS, 2026 revision](https://arxiv.org/abs/2511.04689) | IRT/Fisher-information adaptive testing | Latent ability and model-based precision; not interchangeable with distribution-free finite-matrix inference. |
| [Jiang et al., 2026](https://arxiv.org/abs/2607.15190) | IRT estimation diagnostics under AI data regimes | Motivates validity independent of prediction quality, not blanket rejection of IRT. |
| [Pilditch, 2026, optstop](https://arxiv.org/abs/2608.14425) | Hierarchical Bayesian precision/stability stopping; repeated attempts; retrospective validation | Bayesian credible intervals are not automatically frequentist CS. Equivalence of truncated/full estimates is not the same target as A/B equivalence. |
| [Balkır et al., 2026](https://arxiv.org/abs/2601.13885) | Continuous-score IRT, pairwise stopping, cost-aware ranking | Pairwise adaptive stopping with heterogeneous costs also already exists. |
| [Li, Chen & Huang, 2026, AV-AIVAT](https://arxiv.org/abs/2608.06362) | Paired agent evaluation, predictable variance reduction, CS stopping and bounds | Game payoff target; distinct from frozen benchmark, but strongly overlaps with the broad motivation. |
| [tinyBenchmarks, 2024](https://arxiv.org/abs/2402.14992) | Item selection and IRT-assisted score reconstruction | Important efficient-evaluation baseline family; prediction accuracy is not certification. |
| [Zhou et al., 2026, adaptive auditing](https://arxiv.org/abs/2605.07002) | Anytime-valid adaptive auditing with dueling hypotheses | Worst-subgroup robustness differs from weighted benchmark mean. |

## Candidate contribution to test

**2026-09-09 update:** [Arviv et al., *Stop Guessing When to Stop Testing*](https://arxiv.org/abs/2607.08522), especially Sections 5.2–5.3 and 7.2, explicitly studies sequential pairwise model comparisons with an equivalence margin. This is direct application-level prior art, not merely a neighboring topic. Its stated group-sequential calibration assumes independent observations, approximate normality, and a prespecified number of looks. It is not a non-asymptotic WoR CS theorem. Nevertheless, a claim to introduce sequential model comparison with practical equivalence would be untenable. [BayesAME](https://arxiv.org/abs/2607.27023) additionally covers Bayesian automatic coreset sizing and multi-target correlations; its posterior uncertainty should not be equated with design-based frequentist coverage.

A reproducible decision-focused evaluation of established finite-population methods, including rigorous boundary lower bounds and a documented failure regime for naive subject-wise certification. Any publishable contribution must come from useful theory or convincing evidence, not naming a wrapper.

## Research decision after the follow-up experiments

As of the 2026-09-09 audit, the broad proposed combination is already available by composing established finite-population CS inference with established equivalence decisions. Direct application-level sequential equivalence prior art also exists. We therefore reject a new-framework or first-pairwise-stopping claim, irrespective of whether any one earlier paper states every ingredient in identical notation.

The retained research question is: **when do valid finite-benchmark three-way decisions save evaluations, and what prevents savings near the practical boundary?** The contribution is a self-contained cost characterization and reproducible comparative study, not a new concentration inequality. The elementary inclusion lower bound is presented with its proof and without a priority or minimax-sharpness claim. This positioning does not depend on proving absence of every earlier coupling argument.

Follow-up evidence includes the CELEUS finite-pool signal with both nearest-history and historically tuned low-rank predictors; a stronger joint stratified union-intersection specialization; matched uniform controls; deliberately difficult close-pair cohorts; and synthetic unequal costs. BASELINE_SCOPE.md records which elements are adaptations rather than original-author reproductions. Joint inference removes much of the simple stratum-interval penalty, but the tested strata do not beat direct uniform betting. Better historical predictors also do not generally improve decision cost under the tested inference construction. These negative results are retained and prevent an unsupported superiority claim.

The search is a dated research audit, not a proof of global novelty. Model-family overlap and missing monetary-cost logs limit empirical interpretation rather than being silently assumed away. A human reviewer must judge whether this analysis-and-evidence contribution merits publication; no submission or acceptance is asserted.

## 9 September boundary-focused reassessment

The strongest defensible contribution is a characterization of certification difficulty, not a new sequential-comparison framework. Arviv already studies equivalence and cost versus performance difference. We focus on distance to the disjoint practical-label boundary, distinguish an algorithm-independent edit-capacity obstruction from algorithm-dependent near-census behavior, and connect that distinction to controlled and public-data replays.

[Shekhar and Ramdas (2026)](https://arxiv.org/html/2603.14423v1) already provide substantial instance-dependent finite-population CI lower-bound theory. The new nonconstant, two-sided bound is an elementary consequence of our inclusion constraint, not a claim of first finite-population lower bounds. The sufficient Serfling bound uses established concentration; it is not matching. The available evidence supports an empirical crossover with disagreement-dependent width, not a universal phase transition.

The manuscript now leads with boundary certification cost. Stratification, surrogate, low-rank and broad random-pair results are supplementary. BASELINE_SCOPE.md records why a mislabeled Arviv head-to-head would be invalid and why the Gaussian diagnostic is not a failure claim about its engine. Mathematical novelty remains modest and should be assessed as such.

## 10 September: broader statistical lineage

The contribution is the connection between label-changing edit capacity and certification cost, evaluated against controlled and fixed public vectors. General finite-population sequential certification belongs to established audit and CS literature. Added primary sources: [Kato–Nakagawa v2](https://arxiv.org/html/2604.06116v2), Sections 2–4 and historical review; [RiLACS](https://arxiv.org/html/2107.11323v2), Sections 1.1–1.2; [weighted financial auditing](https://proceedings.mlr.press/v216/shekhar23a.html), published abstract and scope. The first has an unrestricted indifference region; the latter two already support finite-pool assertion certification and weighted/side-information inference. No claim that three-way classification or endpoint transformation supplies independent novelty. Unmatched cost bounds and empirical method dependence remain central limits.
