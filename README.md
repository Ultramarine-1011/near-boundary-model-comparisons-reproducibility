# Near-boundary model comparisons: reproducibility repository

This private repository contains the implementation, tests, analysis scripts, figures, lightweight audit summaries, and arXiv source associated with:

> The Cost of Certifying Near-Boundary Model Comparisons on Finite Benchmarks

Repository URL: https://github.com/Ultramarine-1011/near-boundary-model-comparisons-reproducibility

The repository is intentionally private. It is not a public archive and access is not implied by the manuscript. No model API keys, credentials, or secrets are required by the code.

## Contents

- `src/`: finite-population evaluation, prediction, low-rank, and joint-stratification implementations.
- `scripts/`: data preparation, experiment, summary, plotting, audit, and manuscript-rebuild scripts.
- `tests/`: unit and boundary-condition tests.
- `figures/`: regenerated figures and source graphics.
- `results/`: compact CSV/JSON/Markdown summaries and audit metadata. Large replay JSONL files are intentionally excluded.
- `data/`: provenance and fixed-source manifests. Raw archives and processed response matrices are intentionally excluded.
- `paper/`: the arXiv source package and release checks.
- `THEORY.md`, `CLAIMS.md`, `PROTOCOL.md`, `BASELINE_SCOPE.md`, and `REPRODUCE.md`: scientific scope, evidence mapping, and reproduction instructions.

## Reproduction

Use Python 3.12 and install the pinned dependencies:

```text
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/reproduce.py --full
```

The full pipeline downloads fixed-version upstream archives, checks their SHA-256 hashes, prepares derived matrices, runs the declared experiments, rebuilds summaries and figures, audits the results, and rebuilds the Markdown manuscript. Read `REPRODUCE.md` and `data/PROVENANCE.md` before downloading any upstream data.

The repository does not redistribute upstream archives or processed response matrices. Their source URLs, commit references, hashes, licensing notes, and reconstruction steps are recorded in `data/`.

## Scope and status

This is a reproducibility and audit repository for the submitted manuscript version. It does not claim a new generic three-way testing framework, universal cost superiority, population generalization, or monetary savings. The empirical records are finite-benchmark replay studies over fixed response matrices; replays are not new model evaluations.

The arXiv source package is included under `paper/arxiv-source/`. The final manuscript PDF and build intermediates are kept outside this code repository.
