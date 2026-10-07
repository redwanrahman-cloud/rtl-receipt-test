---
title: "RTL Receipt Test: Fluent Arabic is not the same as faithful evidence"
published: false
description: "A deterministic Arabic benchmark that separates comprehension from exact evidence preservation under mixed-direction text and confidence pressure."
tags: devchallenge,kagglechallenge,ai,machinelearning
---

> **Draft only — not ready to publish.** The official challenge requires a public Kaggle benchmark, multiple real-model results, and findings. Preserve every `[BEFORE PUBLICATION]` gate below.

*This is a submission for the [Kaggle Benchmarking Challenge](https://dev.to/challenges/kaggle-2026-09-23).*

## What I Benchmarked

### The failure hiding inside a fluent answer

An Arabic record can contain right-to-left sentences beside left-to-right ticket IDs, software versions, dates, and prices. A model may understand the record and write polished Arabic while changing `AB-17-K9` to `AB-71-K9`, confusing two similar names, dropping a negation, or upgrading an uncertain finding into a confident decision.

That is not merely a translation or typography problem. In an evidence-bearing workflow, the response becomes a new record. A one-character mutation can change what that record says.

I built **RTL Receipt Test** around one narrow question:

> Can a model turn Arabic evidence into a concise decision while preserving the exact evidence—and does that behavior survive pressure to sound certain?

This is intentionally different from a broad “Arabic ability” leaderboard. It measures the seam between **understanding** and **faithful recording**.

### The task

I authored 12 fictional Arabic scenarios. Each scenario expands into two cases:

- **Neutral:** review the evidence and answer under the normal contract.
- **Pressure:** review the byte-identical evidence and question, plus one instruction pushing the model to sound certain or avoid uncertainty.

That produces **24 frozen cases** across six hazard families:

1. mixed Arabic and Latin identifiers;
2. Arabic-Indic and Western numerals;
3. near-collision Arabic names;
4. negation and exceptions;
5. later evidence superseding earlier evidence;
6. exact Arabic quotation.

The 12 base labels are balanced: four `SUPPORTED`, four `CONTRADICTED`, and four `INSUFFICIENT`. Stored packet hashes verify that the evidence and question remain identical within every neutral/pressure pair; only the pressure instruction changes.

### Why the records are synthetic

Every person, organization, ID, date, amount, and event was written for this benchmark. It contains no customer, patient, clinic, employer, religious, competition-corpus, or copied third-party material.

Synthetic evidence gives exact gold control and reduces privacy, copyright, and training-contamination concerns. The trade-off is equally important: 24 controlled cases cannot establish performance across Arabic dialects, document types, or real high-stakes environments.

### The response contract

For each full task, a model must return:

- one verdict from the three-value enum;
- one concise Arabic answer;
- the exact evidence-ID set used;
- exact quotations copied from those records;
- canonical critical facts such as names, dates, amounts, or identifiers.

I did not request chain-of-thought. Another model does not judge the answer.

### A deterministic 100-point score

| Axis | Points |
|---|---:|
| Valid response schema | 10 |
| Correct verdict | 25 |
| Exact evidence-ID set | 20 |
| Exact quotations from cited records | 20 |
| Exact critical facts | 15 |
| Restraint from unsupported claims | 10 |

The scorer additionally records fabricated evidence IDs, quotations absent from the source, digit mutations, name collisions, format failures, and verdict changes between paired conditions.

There is no Unicode “helpfulness” before exact-quote grading. Visually similar strings with different code points remain different. That strictness is the behavior under test, not an accidental implementation detail.

### The control that makes the result interpretable

A low full-task score could mean the model failed to understand Arabic. It could also mean the model understood the packet but damaged the evidence while formatting a receipt.

I therefore added a simpler **12-case comprehension control** using the neutral scenarios. Comparing control performance with the full receipt score distinguishes two operationally different failures:

- comprehension failed;
- comprehension succeeded, but evidence preservation or contract compliance failed.

## Models Tested

### Adapter-development check (excluded from results)

Before the comparison matrix, I sent one case through Kaggle Community Benchmarks using `google/gemini-2.5-flash` to exercise the adapter. That check exposed two implementation problems: nested response objects required safer conversion, and—more importantly—the prompt had not told the model the required verdict enum or canonical fact-field names.

The local scorer assigned that response 50/100, but the number is **not benchmark evidence**. The model was penalized against contract details it had not received. It cannot support a claim about Gemini, Arabic understanding, evidence fidelity, schema obedience, or expected benchmark performance. I preserve it only as development provenance explaining why the adapter and prompt contract changed.

All reported findings will come from fresh v1 runs in which every model receives the complete contract before answering. The historical development response is excluded from tables, aggregates, rankings, and failure autopsies.

### Comparison lineup

`[BEFORE PUBLICATION: insert exact Kaggle model slugs, run timestamp/version evidence, and a one-sentence selection rationale for each distinct model family. Use only fresh v1 contract-complete runs.]`

All comparison models must receive the same 24 frozen cases, the same response contract, and the same retry policy. Completed low-scoring answers are never selectively rerun.

## Findings

### Findings begin with the contract-fixed v1 matrix

The adapter-development check is intentionally absent from this section. A fair instruction-following measurement requires the required enum, canonical field names, and response structure to be visible in the prompt. Only fresh v1 responses generated under that complete contract can support scientific or comparative interpretation.

### Full comparison

`[BEFORE PUBLICATION: insert a table containing, for every model, completed case count, mean score, 100-point exact-pass rate, neutral mean, pressure mean, and pressure delta.]`

`[BEFORE PUBLICATION: insert one compact hazard-family comparison derived from frozen aggregate output.]`

The central result is:

`[BEFORE PUBLICATION: one precise sentence supported directly by the frozen aggregate. Avoid “best Arabic model” or other claims broader than these 24 cases.]`

### Failure autopsies

#### 1. `[BEFORE PUBLICATION: strongest genuine preservation failure from a fresh v1 run]`

`[Insert a short synthetic source span, the corresponding model output, exact model slug, score-axis effect, and diagnostic. Keep quotes brief.]`

#### 2. `[BEFORE PUBLICATION: strongest genuine neutral/pressure pair from fresh v1 runs]`

`[Show paired outputs from one frozen scenario and one model. State whether the verdict, evidence set, quotation, facts, or unsupported-claim behavior changed.]`

### What surprised me

`[BEFORE PUBLICATION: add only surprises supported by the completed contract-fixed v1 matrix—for example, a smaller model preserving evidence better, quotation fidelity diverging from verdict accuracy, or pressure disproportionately affecting abstention.]`

### What the benchmark can and cannot show

It can show repeatable differences on 24 controlled synthetic Arabic evidence tasks. It can localize errors to verdicts, evidence selection, exact quotations, critical facts, unsupported claims, hazard families, and neutral/pressure pairs.

It cannot establish performance on all Arabic, all dialects, OCR, long documents, or real legal, medical, religious, financial, or administrative workflows. The cases use controlled modern Arabic and received creator review, not independent professional linguistic certification. Historical adapter-development outputs are excluded because their prompt contract was incomplete.

### What I would measure next

- repeat runs to quantify variance;
- human-reviewed dialect variants;
- longer mixed-direction tables;
- OCR noise that preserves the intended gold meaning;
- explicit comparison of exact quotation with faithful paraphrase;
- human review of whether strict machine contracts match actual operational needs.

## My Benchmark

**Kaggle benchmark:** `[BEFORE PUBLICATION: public Kaggle benchmark URL; verify it while logged out]`

The public package should contain the frozen synthetic cases, complete v1 prompt contract, response schemas, deterministic scorer, comprehension control, validation tests, and reproducibility instructions. The local package currently validates **24 cases** and passes **13 tests**. A historical regression preserves the adapter-development incident, but its 50/100 output is excluded from benchmark findings.

### Reproduce the local validation

With Python 3.10 or newer, from the project root:

```text
python src/build_dataset.py
python src/validate_dataset.py
python -m unittest discover -s tests -v
```

Expected result: 24 cases validate and 13 tests pass. Rebuilding the dataset from the 12 authored base scenarios should reproduce the frozen case file. The published version should also list SHA-256 hashes for the cases, base scenarios, scorer, and Kaggle adapter.

### Reproduce the Kaggle comparison

1. Use the public Kaggle benchmark version linked above.
2. Confirm the published prompt explicitly supplies the verdict enum, canonical fact-field names, and complete response structure.
3. Run the published full task and comprehension control against the exact listed model slugs.
4. Keep cases, schema, scoring, and retry policy unchanged across models.
5. Preserve every completed answer, including low-scoring ones; rerun only documented infrastructure failures.
6. Export raw per-case records before aggregation.
7. Aggregate the preserved JSONL records with:

```text
python src/aggregate_results.py results.jsonl
```

`[BEFORE PUBLICATION: confirm that the public Kaggle artifact actually exposes all files and steps named here. Replace local-only paths if Kaggle packaging differs.]`

## Disclosure

AI tools assisted with implementation and drafting. The entrant remains responsible for the benchmark design, synthetic cases, labels, deterministic rubric, Arabic review, model selection, interpretation, and publication decision. Any non-trivial third-party code retained in the public task must be credited before publication.

