# Reproduction

Use Python 3.12. The algorithms require NumPy; data preparation uses pandas; reporting uses SciPy and Matplotlib. Install `requirements.txt` in an isolated environment. This project does not require model API keys, GPUs, or paid inference.

From the repository root:

The single entry point is `python scripts/reproduce.py --full` after installing the pinned requirements. It regenerates all studies and reports each subprocess outcome in `results/reproduction_run.json`. Without `--full`, it runs tests, rebuilds summaries and the standalone Markdown manuscript, and checks existing records. The expanded commands below document the individual steps.

```text
python -m pip install -r requirements.txt
python scripts/download_data.py
python scripts/prepare_data.py
python -m unittest discover -s tests -v
python scripts/run_experiments.py simulation --reps 1000
python scripts/run_experiments.py real --reps 30 --pairs 100
python scripts/run_experiments.py stratification --reps 5 --pairs 20
python scripts/additional_experiments.py
python scripts/betting_simulation.py
python scripts/prediction_experiments.py
python scripts/lowrank_experiments.py
python scripts/cost_experiments.py
python scripts/close_pair_experiments.py
python scripts/joint_stratification_experiments.py
python scripts/joint_controls.py
python scripts/boundary_revision.py
python scripts/summarize.py
python scripts/summarize_additional.py
python scripts/summarize_followups.py
python scripts/summarize_joint.py
python scripts/summarize_lowrank.py
python scripts/plot_followups.py
python scripts/summarize_boundary_revision.py
python scripts/audit_results.py
python scripts/audit_targets.py
python scripts/build_manuscript.py
```

All paths resolve relative to the scripts' repository, except the optional local reporting-library fallback used in this development workspace. Standard installed packages work when that fallback does not exist. A complete run overwrites corresponding generated outputs but never alters source archives.

`download_data.py` checks fixed SHA-256 hashes, including when using existing archives. All three archive URLs refer to fixed repository commits. ATLAS commit `a42e4d174de821f2f0ac2c1fee454afa4964d030` was resolved from its file history and its archive Git blob independently matched to the local input. A changed archive is rejected rather than silently changing the experiment. Downloading does not confer redistribution rights: preserve upstream licensing and keep original archives out of a public source-code release. See `data/PROVENANCE.md` for the licensing scope and source records.

Preparation retains the released item columns and records complete-case row exclusions. Historical model IDs used for prediction are recorded separately. Do not compare scores to an official leaderboard without checking its item set, prompts, normalization, and task weighting.

Initial measured runtimes on this workspace were about 137 seconds for simulation, 377 seconds for the main public replay, and 156 seconds for exploratory stratification. These are execution observations, not portable performance promises. Subsequent studies have their own runtime metadata where recorded. Raw result row counts count repeated algorithms and margins; they are not numbers of independently collected evaluations.

The scientific randomization seeds are fixed in the scripts. Figures and CSV formatting may differ across library versions. Numerical statements should be rechecked from per-run records; exact whole-file hashes of regenerated compressed containers are not used as a cross-platform equality criterion.

The initial 21-step entry-point snapshot completed an independent clean rebuild successfully. Two subsequently added reporting checks, `scripts/plot_followups.py` and `scripts/audit_targets.py`, were run on the rebuilt outputs and matched the original outputs. That entry point included both, for 23 full-run steps. The boundary revision adds an experiment and its summary, giving 25 current full-run steps. These reporting additions do not change experimental trajectories. The target audit recomputes real-data truth labels using integer score totals and rational margins. `CLAIMS.md` maps the main scientific claims to their records and reporting scripts.

For an independent rebuild in a second directory, run the full entry point there using the same source snapshot and pinned inputs. From the original directory, `python scripts/compare_reproduction.py /absolute/path/to/second/research` compares every named processed array and every per-run JSONL record. The current comparison accepts the documented pipeline snapshots but requires all currently named result files; a new independent rebuild must therefore include the boundary revision. The saved historical comparison passed for seven matrices and 1,051,600 original replay records, before the revision. It must not be cited as an independent rebuild of the added study. It establishes reproducibility in the recorded execution environment, not cross-platform bitwise identity or correctness of every scientific inference. `audit_results.py` independently streams records with the standard library and checks counts, label/error consistency, valid evaluation counts, exact census decisions, input digests and selected headline arithmetic. Its scope is explicitly recorded in the audit output.

## Boundary revision verification

The revised repository contains 1,118,200 replay records. `boundary_revision.py` produces 66,600 of them; `summarize_boundary_revision.py` validates unique case/replicate/method keys and 300 replicates per cell. A second execution of the study exactly reproduced its JSONL SHA-256 (`results/boundary_revision_audit.json`). This is a repeat-execution check in the same checkout, not an independent clean rebuild. All 18 unit tests pass. The updated standard-library integrity audit checks all 13 result files. The original separate-directory clean rebuild report remains unchanged as historical evidence for its original scope.

## Focused reporting revision (10 September)

The existing `summarize_boundary_revision.py` step now also reads `betting_real.jsonl` and `close_pairs.jsonl` to rebuild the four-panel main figure and `boundary_figure_pairs.csv`, and writes the separate supplementary Gaussian figure. No trajectories change. After that step, `python scripts/check_boundary_figure.py` independently checks all 840 public-pair means and gaps and writes `boundary_figure_audit.json`. This optional additional reporting audit does not change the 25-step full pipeline. Its successful execution is separate from the historical independent clean rebuild. This revision adds no evaluation runs.
