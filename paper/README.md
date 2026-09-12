# arXiv v1 source snapshot

This directory contains the named arXiv v1 source snapshot. The supplied TMLR style is unmodified and used with `preprint`.

- `arxiv-source/`: complete source snapshot, with `main.tex` at its root and the generated `main.bbl` included.
- `METADATA.md`: proposed submission metadata.
- `OFFICIAL_REQUIREMENTS.md`: dated policy sources and bibliography completion notes.

## Compile

Extract the source ZIP into an empty directory. With TeX Live 2025 on PATH, run there:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex
```

The supplied `main.bbl` permits LaTeX-only processing. No Python, data downloads, model calls, project-level paths or shell-escape commands are needed. Four used figure assets are included. The style license is retained as a necessary redistribution notice; it does not license the paper. The source snapshot excludes the output paper PDF, logs, auxiliary files, unused graphics and experiment matrices.

The scientific sections and abstract are independent copies shared in structure, not filesystem links. The entry and preamble control presentation, `body.tex` selects main sections, and `appendices.tex` selects supplements. Future anonymous TMLR work should use another entry/copy with author fields and identifying references reviewed; do not simply upload this preprint.
