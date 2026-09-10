# Repository scope

## Included

- Source modules, experiment and reporting scripts, and tests.
- Pinned Python requirements.
- Scientific protocol, theory, evidence mapping, novelty scope, and reproduction instructions.
- Figures and compact audit/summary outputs needed to inspect the reported results.
- Data provenance/manifests and the arXiv source package.

## Excluded

- Raw upstream archives and processed response matrices. The provenance files record how to reconstruct them and the hashes used for integrity checks; redistribution rights are not assumed.
- Large replay JSONL files, caches, Python bytecode, LaTeX build intermediates, and rendered PDFs.
- Credentials, API keys, private browser data, and local machine metadata.

The exclusion of large or upstream-controlled files is deliberate. It keeps the repository reviewable and preserves the source-data licensing boundary while retaining the code path needed for an authorized reproduction.
