# arXiv v1 release

This is the named preprint, not an anonymous TMLR submission. The supplied TMLR style is unmodified and used with `preprint`. The AISTATS tree is independent and untouched.

- `arxiv-v1.pdf`: final locally verified PDF, 20 pages.
- `arxiv-v1-source.zip`: upload this archive; main entry is `main.tex` at archive root.
- `source/`: editable release source, including BibTeX database and generated `main.bbl`.
- `METADATA.md` / `metadata.json`: proposed submission fields.
- `FINAL_CHECK.md`: remaining author decisions.
- `validation.json`: checks, file hashes, and scope.
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

The supplied `main.bbl` also permits LaTeX-only processing. No Python, data downloads, model calls, project-level paths or shell-escape commands are needed. Four used figure assets are included. The style license is retained as a necessary redistribution notice; it does not license the paper. The source ZIP excludes the output paper PDF, logs, auxiliary files, unused graphics and experiment matrices.

## Separation and recovery

The original anonymous source remains at `../latex/`. The complete frozen copy is `../backups/aistats2027-2026-template-20260910/`; the independent archive is `../aistats2027-anonymous-backup.zip`. Restore the ZIP into an empty directory and run `python compile.py aistats2027` within its `aistats2027` directory. That backup includes a legacy `arxiv.tex` scaffold from the preceding conversion, which is not this release. Do not upload the backup as arXiv source.

The scientific sections and abstract are independent copies shared in structure, not filesystem links. In this release, the entry and preamble control presentation, `body.tex` selects main sections, and `appendices.tex` selects supplements. Future anonymous TMLR work should use another entry/copy with author fields and identifying references reviewed; do not simply upload this preprint.
