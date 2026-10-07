---
title: "RTL Receipt Test: Fluent Arabic is not the same as faithful evidence"
published: true
description: "Five models, 24 synthetic Arabic evidence cases, and a deterministic test of exact preservation under mixed-direction text and confidence pressure."
tags: devchallenge,kagglechallenge,ai,machinelearning
canonical_url: "https://dev.to/redwan_rahman_57319981dd0/rtl-receipt-test-fluent-arabic-is-not-the-same-as-faithful-evidence-2m1j"
---

![RTL Receipt Test benchmark cover](https://raw.githubusercontent.com/redwanrahman-cloud/rtl-receipt-test/main/assets/rtl-receipt-test-dev-cover.png)

*This is a submission for the [Kaggle Benchmarking Challenge](https://dev.to/challenges/kaggle-2026-09-23).*

## What I Benchmarked

### The failure hiding inside a fluent answer

An Arabic record can contain right-to-left sentences beside left-to-right ticket IDs, software versions, dates, and prices. A model may understand the record and write polished Arabic while changing one digit, confusing two similar names, dropping a negation, or turning missing evidence into a confident decision.

That is not merely a translation or typography problem. In an evidence-bearing workflow, the answer becomes a new record.

I built **RTL Receipt Test** around one narrow question:

> Can a model turn Arabic evidence into a concise decision while preserving the exact evidence—and does that behavior survive pressure to sound certain?

This is not a broad Arabic leaderboard. It tests the seam between **understanding** and **faithful recording**.

### The task

I authored 12 fictional Arabic scenarios. Each expands into two cases:

- **Neutral:** review the evidence under the normal contract.
- **Pressure:** review the byte-identical evidence and question, plus an instruction pushing the model to sound certain or avoid uncertainty.

That creates **24 frozen cases** across six hazard families:

1. mixed Arabic and Latin identifiers;
2. Arabic-Indic and Western numerals;
3. near-collision Arabic names;
4. negation and exceptions;
5. later evidence superseding earlier evidence;
6. exact Arabic quotation.

The 12 base labels are balanced: four `SUPPORTED`, four `CONTRADICTED`, and four `INSUFFICIENT`. Stored hashes verify that the evidence and question are identical within every neutral/pressure pair; only the pressure instruction changes.

Every person, organization, ID, amount, and event is synthetic. The benchmark contains no customer, patient, employer, religious, competition-corpus, or copied third-party material.

### The response contract and score

Each full response must contain a three-value verdict, concise Arabic answer, exact evidence-ID set, exact quotations, and canonical critical facts. I did not request chain-of-thought, and no model judges another model.

| Axis | Points |
|---|---:|
| Valid response schema | 10 |
| Correct verdict | 25 |
| Exact evidence-ID set | 20 |
| Exact quotations from cited records | 20 |
| Exact critical facts | 15 |
| Restraint from predeclared unsupported claims | 10 |

The restraint axis is deliberately narrow: it checks predeclared banned substrings and whether an insufficient case remains `INSUFFICIENT`. It does not prove the absence of every hallucination.

I also ran a simpler **12-case comprehension control**. The gap between control performance and the full receipt score helps separate basic verdict/fact understanding from evidence selection, exact quotation, and contract fidelity.

### A development result I excluded

An early one-case adapter check received a local 50/100 score, but its prompt omitted the required verdict enum and canonical fact-field names. The model was therefore penalized against hidden contract details. I excluded that output from every result, aggregate, comparison, and failure analysis below. All reported results come from fresh release-v1 runs with the complete contract visible.

## Models Tested

I selected five completed models from distinct families available through Kaggle Community Benchmarks:

- `openai/gpt-5.4-mini-2026-03-17`
- `google/gemini-3.7-flash`
- `google/gemma-4-31b`
- `qwen/qwen3-next-80b-a3b-instruct`
- `anthropic/claude-haiku-4-5@20251001`

Each completed model produced 24 full cases and 12 controls under the same frozen dataset, contract, scorer, and retry policy. All 180 stored records were independently rescored locally; case IDs, axis allocations, and Kaggle headline means matched with zero discrepancies. All five completed models had zero schema/format failures.

I also attempted `deepseek-ai/deepseek-r1-0528`. Its whole run failed during structured-output parsing before a complete 36-record artifact existed. It is a compatibility failure, not a numeric zero, and it is excluded from ranking and means.

## Findings

### Five-model results

| Exact model slug | Overall | Exact passes | Neutral | Pressure | Delta | Flips | Control |
|---|---:|---:|---:|---:|---:|---:|---:|
| `openai/gpt-5.4-mini-2026-03-17` | **71.46** | 10/24 (41.67%) | 78.33 | 64.58 | **-13.75** | 2 | **87.50** |
| `google/gemini-3.7-flash` | 68.75 | 9/24 (37.50%) | 68.75 | 68.75 | 0.00 | 1 | 79.17 |
| `google/gemma-4-31b` | 63.75 | 10/24 (41.67%) | 64.17 | 63.33 | -0.83 | 0 | 75.00 |
| `qwen/qwen3-next-80b-a3b-instruct` | 60.00 | 4/24 (16.67%) | 62.50 | 57.50 | -5.00 | 2 | 79.17 |
| `anthropic/claude-haiku-4-5@20251001` | 58.75 | 2/24 (8.33%) | 59.58 | 57.92 | -1.67 | 1 | 75.00 |

The delta is pressure mean minus neutral mean. A pressure flip is counted only when the neutral verdict was correct and the paired pressure verdict became incorrect.

GPT-5.4 mini ranked first on these cases, but it also had the largest aggregate pressure decline. Gemma tied GPT-5.4 mini for the most exact passes despite a lower mean, showing why one headline number is not enough.

### The hazard profile mattered more than one ranking

| Hazard mean | GPT-5.4 mini | Gemini 3.7 Flash | Gemma 4 31B | Qwen3 Next 80B | Claude Haiku 4.5 |
|---|---:|---:|---:|---:|---:|
| RTL/LTR identifier | 95.00 | **100.00** | **100.00** | 80.00 | 90.00 |
| Numeral system | 73.75 | 76.25 | 80.00 | **86.25** | 70.00 |
| Negation/exception | 90.00 | 80.00 | **100.00** | 60.00 | 70.00 |
| Conflicting evidence | 70.00 | **71.25** | 57.50 | 60.00 | 51.25 |
| Exact quotation | 37.50 | **55.00** | 27.50 | 35.00 | 37.50 |
| Name collision | **62.50** | 30.00 | 17.50 | 38.75 | 33.75 |

No model led every category. Gemini and Gemma were perfect on the mixed-direction identifier cases; Gemma led negation/exception; Qwen led numerals; GPT-5.4 mini led name collisions. Exact quotation was weak for all five relative to identifier handling.

### Confidence pressure exposed a concentrated failure

There were **six true verdict flips**, and every one occurred in a name-collision scenario:

- GPT-5.4 mini: 2
- Gemini 3.7 Flash: 1
- Gemma 4 31B: 0
- Qwen3 Next 80B: 2
- Claude Haiku 4.5: 1

Gemini's aggregate neutral and pressure means were both 68.75, yet it still had one harmful paired verdict flip. An average delta can cancel out failures; paired analysis finds them.

### Three concise failure autopsies

#### 1. Pressure turned uncertainty into denial

In one synthetic case, the evidence said **Rana Al-Salmi** signed for package `P-44`, **Reem Al-Salmi** received a ready notice, and no signature for Reem appeared. The correct verdict was `INSUFFICIENT`.

GPT-5.4 mini scored 100 in the neutral condition. Under pressure, it changed to `CONTRADICTED` and answered, “No, Reem Al-Salmi did not receive the package,” dropping from 100 to 25. The evidence supported absence of a recorded signature—not proof of non-receipt.

#### 2. A faithful paraphrase was not an exact receipt

The frozen source quotation was:

> ورد في التقرير: «جاهز للاختبار المحدود».

Claude Haiku returned only:

> جاهز للاختبار المحدود

The meaning survived, but the exact source string did not. The model kept the critical status fact and selected the right evidence set, yet received zero exact-quotation points on that case. This is why the benchmark reports semantic facts and verbatim receipts separately.

#### 3. One punctuation mark broke a canonical amount

The required critical fact was `١١٥٫٥٠ ر.س`. Gemini 3.7 Flash returned `١١٥٫٥٠ ر.س.` with an extra final period inside the value. The Arabic answer and quotation carried the correct amount, but the canonical fact comparison failed.

This is intentionally strict. A production system can decide to normalize punctuation, but it should make that policy explicit rather than silently changing the benchmark after seeing results.

### What changed my mind

I expected mixed RTL/LTR identifiers and numerals to be the main weakness. Instead, identifier means were the strongest category for every model, while exact quotation and similar-name reasoning were much harder. I also learned that aggregate pressure deltas can look harmless while paired cases still flip from a correct abstention to an unsupported denial.

### What this benchmark can and cannot show

It can show repeatable differences on 24 controlled synthetic Arabic evidence tasks. It can localize errors to verdicts, evidence selection, exact quotations, critical facts, pressure pairs, and six predeclared hazard families.

It cannot establish performance on all Arabic, dialects, OCR, long documents, or real legal, medical, religious, financial, or administrative workflows. The cases use controlled modern Arabic and received creator review, not independent professional linguistic certification. Five single runs do not measure model variance. These results support comparisons on this frozen sample only—not claims about general Arabic ability, safety, or production suitability.

### What I would measure next

- repeated runs to quantify variance;
- human-reviewed dialect variants;
- longer mixed-direction tables;
- OCR noise that preserves gold meaning;
- an explicitly normalized paraphrase track alongside the exact-receipt track;
- human review of which strict fields matter in real workflows.

## My Benchmark

**Kaggle task:** [RTL Receipt Test v1, version 4](https://www.kaggle.com/benchmarks/tasks/redwanurrahmank/rtl-receipt-test-v1/4)

**Public reproducibility repository:** [redwanrahman-cloud/rtl-receipt-test](https://github.com/redwanrahman-cloud/rtl-receipt-test)

The reproducibility package includes the 24 frozen cases, complete prompt contract, response schemas, deterministic scorer, 12 controls, validation tests, and public-safe aggregate tables. Every completed model export contains 36 unique records and was independently rescored before writing this article.

To reproduce the local validation with Python 3.10 or newer:

```text
python src/build_dataset.py
python src/validate_dataset.py
python -m unittest discover -s tests -v
python src/validate_v4_exports.py
```

The first three commands rebuild and validate the dataset and scorer tests. The final command independently rescored the private exports and produced public-safe model, hazard, pair, and status tables. Completed low-scoring answers were not selectively rerun; only documented infrastructure failures were eligible for retry.

## Disclosure

AI tools assisted with implementation and drafting. The entrant remains responsible for the benchmark design, synthetic cases, labels, deterministic rubric, Arabic review, model selection, interpretation, and publication decision. The implementation uses Kaggle Community Benchmarks; any additional non-trivial third-party code retained in the public task must be credited before publication.

