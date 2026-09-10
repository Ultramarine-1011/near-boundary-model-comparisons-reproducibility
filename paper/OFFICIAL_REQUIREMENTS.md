# Official requirements checked 2026-09-10

The official sources below were read during release preparation. This is local preparation, not confirmation of arXiv moderation or server compilation.

- [arXiv TeX submission](https://info.arxiv.org/help/submit_tex.html): submit the required TeX, bibliography and figure dependencies; omit unused files and the generated paper PDF. Use pdfLaTeX for PDF/PNG figures and inspect the server-generated result. This bundle has a root `main.tex`, `.bib` and matching `.bbl`, vendored styles, and no shell-escape requirement. The local engine is TeX Live 2025.
- [arXiv metadata](https://info.arxiv.org/help/prep.html): accurate named authors; ASCII metadata; abstract no longer than 1920 characters; comments may state page/figure counts. The draft abstract has 1431 characters. No journal reference or DOI is invented.
- [arXiv licenses](https://info.arxiv.org/help/license/index.html): the submitter must hold redistribution rights and choose the license. A version's license is irrevocable. CC BY 4.0 is proposed, not selected or granted on the author's behalf.
- [arXiv categories](https://arxiv.org/category_taxonomy): cs.LG with stat.ML cross-list is a proposed fit for statistically grounded ML evaluation, subject to author choice and moderation.
- [TMLR author guide](https://jmlr.org/tmlr/author-guide.html): public preprints are allowed; TMLR submissions themselves are double blind. TMLR requires its official style and CC BY 4.0 for submissions. This public preprint uses the supplied style's documented `preprint` option; it is not marked as under review or accepted.
- [TMLR editorial policies](https://jmlr.org/tmlr/editorial-policies.html): review publication and concurrent-submission restrictions before a future journal submission. Preserving an AISTATS draft does not itself imply an active submission. No submission status is asserted here.

## Bibliography completion

All 20 existing references were carried into a BibTeX database; no new research references were added. Six previously abbreviated author lists were completed from the corresponding primary arXiv records: [Arviv et al.](https://arxiv.org/abs/2607.08522), [Lyu et al.](https://arxiv.org/abs/2606.07726), [Zhou et al.](https://arxiv.org/abs/2606.20820), [Cordero Encinar et al.](https://arxiv.org/abs/2607.27023), [Li et al.](https://arxiv.org/abs/2511.04689), and [Balkir et al.](https://arxiv.org/abs/2601.13885). Remaining bibliographic details preserve the existing manuscript's source records. This round checked citation resolution and completed these metadata fields; it did not redo the prior full-text literature audit.

Public upstream data archive links and frozen commit identifiers were carried from the project's existing provenance ledger into Appendix B. No raw or derived response matrix is redistributed in the manuscript source bundle. The implementation and audit records are retained in the private GitHub repository at https://github.com/Ultramarine-1011/near-boundary-model-comparisons-reproducibility; the repository is not a public archive.
