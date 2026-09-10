# Input provenance and redistribution scope

Checked 2026-09-09. The scripts download public research response matrices; experiments use local immutable copies. This repository does not assert ownership of those matrices or redistribute them as original research code.

## ATLAS

Source: [Peiyu-Georgia-Li/ATLAS](https://github.com/Peiyu-Georgia-Li/ATLAS). The file-history API identifies commit `a42e4d174de821f2f0ac2c1fee454afa4964d030` for `data/data.zip`. Its [fixed contents API record](https://api.github.com/repos/Peiyu-Georgia-Li/ATLAS/contents/data/data.zip?ref=a42e4d174de821f2f0ac2c1fee454afa4964d030) gives Git blob SHA-1 `5c26eeea58ec6d55f7e0e5b0403d4adbf81a1cdb`. Computing the Git blob digest from the downloaded bytes independently matches that value. The SHA-256 used to accept downloads is `4c58404271957478b5c64b1b734e7c0825b1303ddbe5ce2c29c8629798f79e64`.

The current README describes response matrices as not committed, despite the accessible historical archive. We therefore identify the actual historical file and verify its bytes rather than treating current README counts as data facts. The GitHub repository-license endpoint returned HTTP 404 at inspection. This does not prove that no terms apply elsewhere. No explicit redistribution permission was established; the public code release should contain the download script, not these raw or derived response matrices.

## Efficiently evaluating LLMs

Source: [skbwu/efficiently-evaluating-llms](https://github.com/skbwu/efficiently-evaluating-llms). Both archives are pinned to commit `857ee18607bd9c84e90431ce0b8f36fc3f72ae68` and checked against SHA-256 values in `scripts/download_data.py` and `raw/manifest.json`. The current repository license endpoint identifies Apache-2.0. That repository-level metadata alone is not treated as a license grant for every underlying benchmark or model-response matrix. Raw archives and processed response matrices remain excluded from the public code manifest; users retrieve the fixed upstream files through the documented script.

## Analytical boundary

Counts, missingness, model identifiers and item columns are audited from the actual archive members in `processed/audit.json`. The transformed arrays preserve the released item set, including upstream filtering. Historical-reference model IDs are excluded from test IDs; this is not a guarantee of family independence. Evaluation records are frozen responses, not fresh model generations. Results concern these finite, item-weighted matrices and must not be labeled official leaderboard scores or dollar savings.
