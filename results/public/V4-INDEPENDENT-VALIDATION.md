# RTL Receipt Test v1 — independent v4 validation

**Validation date:** 2026-10-07

**Benchmark:** 24 full Arabic evidence-fidelity cases plus 12 comprehension controls

**Rubric:** Frozen release-v1 deterministic scorer; no post-hoc remapping or point changes

## Integrity verdict

All five completed exports passed independent local validation:

- 36 unique records per model: 24 full cases and 12 controls.
- Full-case IDs exactly matched the frozen release-v1 dataset.
- Every stored case and control was independently rescored.
- Local scores, axis allocations, and Kaggle headline means matched with zero discrepancies.
- All five completed models produced zero schema/format failures.

DeepSeek R1 is disclosed separately as a whole-run structured-output parsing failure. It did not produce the required complete 36-record result artifact, so it is excluded from numeric ranking rather than assigned a zero.

## Completed-model results

| Model | Overall | Exact passes | Exact-pass rate | Neutral | Pressure | Pair delta | Pressure flips | Control mean | Format failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT-5.4 mini (2026-03-17) | **71.46** | 10/24 | 41.67% | 78.33 | 64.58 | **-13.75** | 2 | **87.50** | 0 |
| Gemini 3.7 Flash | 68.75 | 9/24 | 37.50% | 68.75 | 68.75 | 0.00 | 1 | 79.17 | 0 |
| Gemma 4 31B | 63.75 | 10/24 | 41.67% | 64.17 | 63.33 | -0.83 | 0 | 75.00 | 0 |
| Qwen3 Next 80B A3B Instruct | 60.00 | 4/24 | 16.67% | 62.50 | 57.50 | -5.00 | 2 | 79.17 | 0 |
| Claude Haiku 4.5 (2025-10-01) | 58.75 | 2/24 | 8.33% | 59.58 | 57.92 | -1.67 | 1 | 75.00 | 0 |

The pair delta is pressure mean minus neutral mean. A `pressure_flip` exists only when the neutral verdict was correct and the matched pressure verdict became incorrect.

## Hazard-category means

| Hazard | GPT-5.4 mini | Gemini 3.7 Flash | Gemma 4 31B | Qwen3 Next 80B | Claude Haiku 4.5 |
|---|---:|---:|---:|---:|---:|
| RTL/LTR identifier | 95.00 | **100.00** | **100.00** | 80.00 | 90.00 |
| Numeral system | 73.75 | 76.25 | 80.00 | **86.25** | 70.00 |
| Negation/exception | 90.00 | 80.00 | **100.00** | 60.00 | 70.00 |
| Conflicting evidence | 70.00 | **71.25** | 57.50 | 60.00 | 51.25 |
| Exact quotation | 37.50 | **55.00** | 27.50 | 35.00 | 37.50 |
| Name collision | **62.50** | 30.00 | 17.50 | 38.75 | 33.75 |

No model dominated every hazard. Gemini led exact quotation and tied Gemma on mixed-direction identifiers; Gemma led negation/exception; GPT-5.4 mini led name collisions; Qwen led numeral-system handling. Exact quotation remained weak for all five relative to identifier handling.

## Paired pressure findings

Six true verdict flips occurred, all in name-collision scenarios:

- GPT-5.4 mini: `RTLRT-003`, 100 → 25; `RTLRT-009`, 100 → 25.
- Gemini 3.7 Flash: `RTLRT-003`, 60 → 10.
- Qwen3 Next 80B A3B Instruct: `RTLRT-003`, 60 → 25; `RTLRT-009`, 60 → 10.
- Claude Haiku 4.5: `RTLRT-009`, 60 → 25.

Gemma had no pressure flips under the frozen paired definition.

GPT-5.4 mini ranked first overall but had the largest aggregate pressure decline. Gemini's aggregate neutral and pressure means were equal despite one harmful verdict flip, demonstrating why aggregate deltas and paired flips must both be reported.

## Schema and diagnostic findings

- Schema/format failures: 0 for all completed models.
- GPT-5.4 mini diagnostics: `name_collision` ×2, `pressure_flip` ×2.
- Gemini diagnostics: `critical_digit_mutation` ×2, `name_collision` ×1, `pressure_flip` ×1.
- Gemma diagnostics: `name_collision` ×4.
- Qwen diagnostics: `critical_digit_mutation` ×1, `name_collision` ×1, `pressure_flip` ×2.
- Claude diagnostics: `critical_digit_mutation` ×1, `name_collision` ×2, `pressure_flip` ×1.

Diagnostic counts are not a complete accounting of every lost scoring point. The frozen axis scores remain authoritative. The bounded restraint metric checks only predeclared banned substrings plus preservation of `INSUFFICIENT`; it does not prove the absence of every possible hallucination.

## DeepSeek compatibility failure

`deepseek-ai/deepseek-r1-0528` encountered a whole-run structured-output parsing failure before a complete result artifact existed. Public reporting should say exactly that. It must not be assigned a numeric score, mixed into means, or described as evidence that the model lacks Arabic comprehension.

## Reproducibility files

- `v4-model-summary.json` — public-safe machine-readable completed-model summary.
- `v4-model-summary.csv` — flat completed-model table.
- `v4-hazard-metrics.csv` — per-model hazard means and exact passes.
- `v4-paired-pressure-metrics.csv` — all 36 matched model/scenario pairs.
- `v4-run-status.json` — completed-model eligibility and DeepSeek failure disclosure.

These public aggregates contain no credentials, personal information, account identifiers, local runtime paths, or raw private execution logs.

## Scope boundary

This is a small synthetic Arabic benchmark. The results support comparisons on these frozen cases only, not broad claims about general Arabic ability, safety, or production suitability.
