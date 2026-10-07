# Gate 1 acceptance report

**Date:** 2026-10-07, Asia/Riyadh  
**Scope:** Local, zero-cost Arabic Evidence Fidelity Benchmark package  
**Decision:** LOCAL GATE 1 PASS; SIGNED-IN KAGGLE GATE REMAINS

## Delivered

- 12 newly authored synthetic Arabic base scenarios.
- 24 frozen neutral/pressure cases.
- Six hazard families with two scenarios each.
- Balanced base verdicts: 4 supported, 4 contradicted, 4 insufficient.
- Byte-identical evidence/query packets within each neutral/pressure pair, proven by stored SHA-256 packet hashes.
- Deterministic 100-point full-task scorer with diagnostics.
- Deterministic 12-scenario verdict/fact comprehension control.
- Response schemas, dataset validator, aggregation helper, Kaggle adapter, runbook, and draft DEV article.
- Article result sections remain explicit placeholders; no result or model claim was invented.

## Local verification

Executed with the Codex bundled Python runtime:

1. Dataset build: wrote 24 cases.
2. Dataset validation: PASS — 24 cases, 12 matched pairs, balanced labels and hazards.
3. Unit tests: PASS — 12/12 after adding the live smoke regression.
4. Python compilation: PASS for builder, scorer, validator, aggregator, Kaggle adapter, and tests.
5. JSON parsing: PASS for dataset and both response schemas.

The tests cover:

- all perfect fixtures scoring 100;
- malformed JSON without a crash;
- fabricated evidence IDs;
- extra real but unsupported evidence;
- changed Arabic-Indic digits;
- visually similar quotation code-point changes;
- evidence-ID order invariance;
- insufficient-evidence overclaim under pressure;
- repeated-score determinism;
- comprehension-control scoring;
- exact reproduction of the live 50/100 invalid-enum/canonical-field failure;
- complete dataset invariants.

## Frozen artifact hashes

- `data/cases.json` release v1: `E5F4433A2A3D3B9E854428835BC836137EBE11632696D3F7E35C59D886AA5093`
- `src/base_scenarios.json`: `756C7CB0C7F0AFF6EB606C8A9AEF731E33A704F05EABA8C3D4BDC55BFC6BBDB7`
- `src/scorer.py`: `534144329FA373B07B6ADF2D294E0E36C8CDC21CB93D403D7F245B1B384B9323`
- `kaggle_task.py`: `201FE96B815613BA899F64E458DF0561AE7EE0FAD42CFE250BDCF7993D69B940`

Any content change requires new hashes and a new benchmark version. Do not edit gold data after observing comparison-model outputs.

## Provenance boundary

The cases are fictional and newly authored. No IsnadLens corpus, prompt, evaluation case, submission artifact, religious text, patient/clinic/employer/customer data, or copied third-party document was used. This is a technical provenance statement, not independent copyright or legal certification.

## Honest remaining limitations

- No signed-in Kaggle task has run, so the adapter is compiled but not platform-validated.
- No model list or free quota has been observed from Redwan's account.
- No Arabic human clarity/label review has been completed.
- No benchmark has been created, saved, made public, or linked.
- No DEV account/submission control has been tested.
- The public challenge page's contradictory `Live Ended` label remains unresolved.
- No model results exist; the draft article must not be published in its current placeholder state.

## Next gate

Redwan must perform the exact signed-in sequence in `README.md`, beginning with DEV submission-path confirmation and Kaggle phone/identity/quota checks. Stop if payment is requested. The first external technical action is a one-case, one-free-model private smoke run. Only after that succeeds should the frozen matrix run.
