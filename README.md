# RTL Receipt Test

RTL Receipt Test is a deterministic diagnostic for a narrow multilingual failure: a model can understand Arabic evidence and still damage the record it produces.

The benchmark tests exact preservation when Arabic prose is mixed with Latin identifiers, Arabic-Indic and Western numerals, similar names, negation, superseded records, exact quotations, and pressure to sound certain. It separates basic verdict/fact comprehension from the stricter work of producing a machine-readable evidence receipt.

Everything in `data/cases.json` is fictional and newly authored. The project contains no IsnadLens material, religious source text, patient, clinic, employer, or customer data, and no copied third-party records.

## Why this benchmark exists

Most broad language evaluations collapse several behaviors into one score. In an operational evidence workflow, these questions need separate answers:

1. Did the model understand the record?
2. Did it select the right evidence?
3. Did it copy quotations and critical facts exactly?
4. Did it obey the output ontology?
5. Did confidence pressure change the decision or introduce unsupported claims?

The 100-point scorer keeps those dimensions visible. It does not use an LLM judge and does not normalize away Unicode differences before exact-quote grading.

## Evidence status

- 12 frozen base scenarios.
- 24 expanded cases: one neutral and one pressure condition per scenario.
- Byte-identical evidence and question within each pair; only the pressure instruction changes.
- Balanced base labels: 4 `SUPPORTED`, 4 `CONTRADICTED`, 4 `INSUFFICIENT`.
- Six hazard families, two scenarios each.
- Deterministic 100-point full-task scorer and 12-case comprehension control.
- 13 local validation tests pass.
- Five fresh release-v1 model exports completed: 24 full cases plus 12 controls per model.
- All 180 completed records were independently rescored; stored totals, axes, and Kaggle headline means matched with zero discrepancies.
- Completed exact model slugs: `openai/gpt-5.4-mini-2026-03-17`, `google/gemini-3.7-flash`, `google/gemma-4-31b`, `qwen/qwen3-next-80b-a3b-instruct`, and `anthropic/claude-haiku-4-5@20251001`.
- `deepseek-ai/deepseek-r1-0528` failed whole-run structured-output parsing before a complete artifact existed. It is excluded from numeric ranking and is not scored as zero.
- One private adapter-development check ran on `google/gemini-2.5-flash`. Its prompt omitted the required verdict enum and canonical fact-field names, so its historical 50/100 local score is **invalid as benchmark or model-performance evidence**.
- That check is preserved only as development provenance for the nested-response adapter repair and the requirement to expose the complete scoring contract.
- Kaggle and DEV accounts were verified. Private execution is complete, but no benchmark or article has been published or submitted.
- Kaggle's included benchmark quota funded the runs; no external API credit was added. The preserved completed-model total shown by Kaggle was approximately USD 0.197 in included usage, not an out-of-pocket charge.

Scientifically interpretable results now exist for the five completed release-v1 runs on this frozen sample. A valid challenge entry still requires making the Kaggle task public, verifying logged-out access, publishing the English DEV article, and submitting it once through the challenge control.

## Repository map

- `data/cases.json` — frozen 24-case dataset.
- `src/base_scenarios.json` — human-authored 12-scenario source.
- `src/build_dataset.py` — deterministic neutral/pressure pair expansion.
- `src/scorer.py` — deterministic full-task and control graders.
- `src/validate_dataset.py` — integrity and balance checks.
- `src/aggregate_results.py` — aggregation of preserved per-case JSONL outputs.
- `src/validate_v4_exports.py` — independent rescoring and public-safe v4 export generation.
- `schemas/response.schema.json` — full receipt contract.
- `schemas/control-response.schema.json` — comprehension-control contract.
- `tests/test_benchmark.py` — validation and adversarial scorer tests.
- `kaggle_task.py` — Kaggle Community Benchmarks adapter.
- `RTL-Receipt-Test-PRIVATE-SMOKE.ipynb` — historical adapter-development notebook; do not include its score in results.
- `LIVE-SMOKE-REPORT.md` — historical development provenance; its performance interpretation is superseded by the contract audit.
- `DEV-ARTICLE-DRAFT.md` — official-template-aligned article draft with publication gates.
- `results/public/` — credential-free model, hazard, paired-pressure, status, and independent-validation artifacts.
- `results/private/` — private raw execution evidence; do not publish this directory.

## Completed release-v1 results

| Exact model slug | Mean | Exact passes | Neutral | Pressure | Flips | Control |
|---|---:|---:|---:|---:|---:|---:|
| `openai/gpt-5.4-mini-2026-03-17` | 71.46 | 10/24 | 78.33 | 64.58 | 2 | 87.50 |
| `google/gemini-3.7-flash` | 68.75 | 9/24 | 68.75 | 68.75 | 1 | 79.17 |
| `google/gemma-4-31b` | 63.75 | 10/24 | 64.17 | 63.33 | 0 | 75.00 |
| `qwen/qwen3-next-80b-a3b-instruct` | 60.00 | 4/24 | 62.50 | 57.50 | 2 | 79.17 |
| `anthropic/claude-haiku-4-5@20251001` | 58.75 | 2/24 | 59.58 | 57.92 | 1 | 75.00 |

Six true verdict flips occurred, all in name-collision scenarios. Exact quotation was the weakest or near-weakest hazard for every completed model, while mixed-direction identifiers were consistently strong. See `results/public/V4-INDEPENDENT-VALIDATION.md` for the verified interpretation and scope boundary.

## Reproduce the frozen local package

Requirements: Python 3.10 or newer. The local build, validation, scoring, aggregation, and tests use the Python standard library.

From this directory:

```text
python src/build_dataset.py
python src/validate_dataset.py
python -m unittest discover -s tests -v
python src/validate_v4_exports.py
```

Expected result:

- `data/cases.json` is rebuilt with 24 cases;
- validation reports 24 cases, 12 matched neutral/pressure pairs, balanced labels, and balanced hazards;
- 13 tests pass, including a regression that preserves the historical adapter response. That regression verifies deterministic code behavior; it does not validate the 50/100 score as model evidence.
- five completed private exports independently rescore with zero discrepancies and regenerate the public-safe v4 tables.

Optional compilation check:

```text
python -m py_compile src/build_dataset.py src/validate_dataset.py src/scorer.py src/aggregate_results.py tests/test_benchmark.py
```

`kaggle_task.py` imports `kaggle_benchmarks`, so import or execute it only in an environment where that package is available. Local tests exercise the benchmark logic without requiring model access.

## Frozen artifact hashes

Recorded after the adapter repair:

| Artifact | SHA-256 |
|---|---|
| `data/cases.json` | `E5F4433A2A3D3B9E854428835BC836137EBE11632696D3F7E35C59D886AA5093` |
| `src/base_scenarios.json` | `756C7CB0C7F0AFF6EB606C8A9AEF731E33A704F05EABA8C3D4BDC55BFC6BBDB7` |
| `src/scorer.py` | `470789F811CB6C242EC17616CA1B743CCE4D45FB1E9311231B68182E39360D8D` |
| `kaggle_task.py` | `201FE96B815613BA899F64E458DF0561AE7EE0FAD42CFE250BDCF7993D69B940` |
| `rtl_receipt_task_v1.py` | `0D9E878E741E9FB40EA5A1CCEB7C3F7DBA4FC645DB7B48A580A9E4C46BC37824` |

Any benchmark-content change requires a new version, new hashes, and a complete rerun. Do not alter gold data after inspecting comparison-model outputs.

## Comparison-matrix protocol

1. Record the exact Kaggle benchmark version, timestamp, and model slugs.
2. Confirm every model prompt includes the required verdict enum, canonical fact-field names, and full response structure.
3. Run the same 24 full cases and 12 neutral comprehension controls for every model.
4. Use the same attempt and retry policy across the matrix.
5. Preserve every completed response, including failures and low scores.
6. Rerun only genuine infrastructure failures, and record the original failure plus the repair.
7. Export one JSONL row per completed full-task case with at least:
   - `model`
   - `case_id`
   - `condition`
   - `hazard_family`
   - `score`
   - `diagnostics`
   - raw structured response or an immutable reference to it
8. Aggregate preserved rows without rerunning models:

```text
python src/aggregate_results.py results.jsonl
```

The completed article reports case count, mean score, exact 100-point pass rate, neutral and pressure means, paired flips, control means, and hazard means. Never infer a broad “best Arabic model” from these 24 controlled cases.

## Frozen retry policy

- Infrastructure failures may be rerun and must be logged as such.
- A completed answer is never selectively rerun because its score is poor.
- If the platform supplies stochastic retries, use the same attempt count for every model and case or disable retries.
- Do not edit cases, gold labels, rubric, banned tokens, or normalization after observing comparison-model results.

## Challenge-publication gates

The official DEV challenge requires one published English submission post using its template and `#kagglechallenge`, a publicly accessible Kaggle benchmark link, the tasks and models tested, and findings from the results. Judging emphasizes insights, writing quality, and creativity. Only one entry is allowed.

Before publication, Redwan must personally approve or perform the external actions below:

1. Reconfirm the DEV submission control and official deadline/status.
2. Confirm remaining free Kaggle quota; stop if billing or payment is requested.
3. Confirm the five completed v1 exports and independent public-safe aggregates remain unchanged.
4. Review the Arabic cases and result claims personally; no professional linguistic certification is claimed.
5. Proofread `DEV-ARTICLE-DRAFT.md` against `results/public/V4-INDEPENDENT-VALIDATION.md`; it contains no result placeholders.
6. Check that the public Kaggle artifact contains the promised cases, contracts, scorer, tests, and reproduction instructions.
7. Approve making the Kaggle benchmark public.
8. Verify the public Kaggle URL while logged out.
9. Add a cover image and verify the required DEV template headings and tags.
10. Approve and publish the DEV article, then submit it through the challenge control.

No one should publish placeholders, invent multi-model findings, add API credits, or silently weaken the scorer to improve results.

### Metric boundary

`unsupported_claim_restraint` is deliberately narrow. It proves only that the concise Arabic answer avoids the case's predeclared exact banned substrings and, for an insufficient case, retains the `INSUFFICIENT` verdict. It does not prove the absence of every possible hallucination. `pressure_flip` is added only after paired analysis when the neutral verdict is correct and the matched pressure verdict becomes incorrect.

