# Claim-to-evidence map

Numbers refer to fixed released matrices or declared synthetic populations. Replays are sampling-design randomizations, not newly collected model responses. Theorems are proved separately and do not follow from observed low error rates.

| Manuscript claim | Primary records | Reporting / independent check |
|---|---|---|
| Main EB grid uses 41.6% macro-average, zero main-cohort errors | results/real.jsonl, epsilon=.02 and method=eb_grid | scripts/summarize.py; scripts/audit_results.py independently recomputes 0.41635001708545516 and 0/21000 |
| Direct betting reduces mean cost in each main matrix, 11 errors | results/betting_real.jsonl | scripts/summarize_additional.py; audit_results.py checks 11/21000 |
| Equivalent pairs can approach census | results/class_summary.csv and real.jsonl | scripts/summarize.py, grouped by true label, not failure to reject superiority |
| Naive normal intervals can have large decision error | results/simulation.jsonl | scripts/summarize.py; simulation_summary.csv gives per-cell error and binomial intervals |
| Direct betting simulation risk diagnostics | results/betting_simulation.jsonl | scripts/summarize_followups.py; betting_simulation_summary.csv |
| Simple stratification can help or hurt | results/heterogeneity_simulation.jsonl, stratification.jsonl | scripts/summarize_additional.py and summarize.py; cost ratios must not be confused with ratios of means |
| Joint inference removes much of separate-stratum overhead | results/joint_stratification.jsonl and joint_controls.jsonl | scripts/summarize_joint.py; same cohort, one-stratum matched batching control |
| Margin-nearest pairs remain expensive | results/close_pairs.jsonl and close_pair_selection.json | scripts/summarize_followups.py; retrospective selection disclosed |
| Predictor quality does not automatically reduce cost | results/prediction_real.jsonl and lowrank_real.jsonl | scripts/summarize_lowrank.py; paired cost differences and pair-cluster bootstrap intervals |
| Item cost and monetary cost differ | results/cost_simulation.jsonl | scripts/summarize_followups.py; artificial 1:10 cost units, no dollar inference |
| Closed-region three-way correctness | THEORY.md Sections 2, 3, 8 and 9 | Coverage implication and explicit directional-test union bounds; not an empirical claim |
| Boundary inclusion obstruction | THEORY.md Sections 5 and 6 | Coupled-history argument and combinatorial bound; no general optimality or priority claim |

`scripts/audit_targets.py` independently recomputes all recorded real-study means and labels from integer binary-score totals and rational margins, without importing the evaluator's label function. This checks the scientific target against the actual frozen matrices. `scripts/audit_results.py` checks record consistency, expected row counts, census labels and data digests. `scripts/compare_reproduction.py` compares independent executions after the full pipeline finishes. These checks have different scopes and are not interchangeable.

Figure sources: `scripts/summarize.py` produces the initial main-cost and boundary panels; `scripts/plot_followups.py` produces the three-panel follow-up comparison. Means in different panels may come from different cohorts; the manuscript captions specify those cohorts. Figures and all reported CSVs can be regenerated without model calls.

## Revised central claims

| Claim | Evidence and limits |
|---|---|
| Near-boundary costs are high but gap alone does not determine them | `boundary_revision_summary.csv`, 74 fixed populations, 300 permutations and three methods; `scripts/summarize_boundary_revision.py` produces Figure 1. Exploratory follow-up; no fitted universal phase transition. |
| Heterogeneous two-sided edit-capacity obstruction | THEORY.md Section 7, derived from Section 5 inclusion constraint; exhaustive small ternary-population alternatives in `tests/test_boundary_revision.py`. Elementary consequence, no priority or sharpness claim. |
| Explicit sufficient early-stopping regime | THEORY.md Section 7, all-look Serfling union bound; algebra tested. Does not match the lower bound or prove direct-betting optimality. |
| Planned Gaussian correction does not establish arbitrary-finite-vector validity | Rare-event cells in `boundary_revision_summary.csv`; exact small-population diagnostic test. Not an implementation or failure report of Arviv's engine. |
| New result reproducibility | `boundary_revision_audit.json`, exact repeated JSONL SHA-256. Historical clean rebuild covers only original results. |

## Current Figure 1 (10 September)

`scripts/summarize_boundary_revision.py` now combines controlled cost curves with public gap-versus-cost scatterplots. `results/boundary_figure_pairs.csv` contains 700 random pair means and 140 margin-nearest stress pair means. `scripts/check_boundary_figure.py` independently reconstructs all 840 means and gaps from the unchanged `betting_real.jsonl` and `close_pairs.jsonl` records; its output is `boundary_figure_audit.json`. Public points represent 30 and 100 permutations respectively. Identical axes make the cohort selection visible, without fitting a universal law. The Gaussian plot is now Figure D1 (`gaussian_diagnostic.png`), not main-claim evidence.
