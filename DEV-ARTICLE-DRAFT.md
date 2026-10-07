---
title: "RTL Receipt Test: Can AI preserve Arabic evidence without rewriting it?"
published: false
description: "A deterministic benchmark separating Arabic comprehension from evidence preservation under RTL, numeral, quotation, and confidence pressure."
tags: devchallenge,kagglechallenge,ai,machinelearning
---

> **Draft only. Do not publish until every `[RESULT REQUIRED]` marker is replaced from preserved Kaggle outputs and the public benchmark link works.**

## The one-character failure that changes the record

Arabic business records often contain two writing directions at once: Arabic sentences flow right to left, while ticket IDs, software versions, dates, and prices may flow left to right. A response can sound completely fluent while changing `AB-17-K9` into `AB-71-K9`, turning `١١٥٫٥٠` into `١٢٥٫٥٠`, or replacing a qualified sentence with a stronger one that never appeared in the evidence.

That is not a cosmetic formatting error. It can reverse a decision.

I built **RTL Receipt Test** to ask a narrower question than “Does this model know Arabic?”

> When a model understands an Arabic evidence packet, can it preserve the exact evidence while producing a concise decision—and can it still do that when a user pressures it to sound confident?

## What I benchmarked

The benchmark contains 12 newly authored fictional scenarios. Every scenario has two conditions:

- a neutral evidence-review request;
- the same evidence and question plus pressure to sound confident or avoid uncertainty.

The evidence packets are byte-identical across each pair. Only the pressure sentence changes. That creates 24 cases per model across six hazard families:

1. mixed Arabic and Latin identifiers;
2. Arabic-Indic and Western numerals;
3. near-collision Arabic names;
4. negation and exceptions;
5. later evidence that supersedes earlier evidence;
6. exact Arabic quotation.

The gold labels are balanced across `SUPPORTED`, `CONTRADICTED`, and `INSUFFICIENT`.

## Why everything is synthetic

All records, people, organizations, IDs, dates, and events were written specifically for this benchmark. No private records, customer data, medical data, religious texts, competition corpus, or copied documents are included.

Synthetic cases give me exact gold control and reduce privacy, copyright, and training-contamination concerns. The trade-off is realism: this is a small controlled diagnostic, not proof of performance on every Arabic workflow.

## The response contract

Each model returns:

- one of three verdicts;
- one concise Arabic answer;
- the evidence IDs it relied on;
- exact quotations copied from those records;
- critical names, amounts, dates, or identifiers.

I did not request chain-of-thought and did not use another model to grade responses.

## A deterministic 100-point score

| Axis | Points |
|---|---:|
| Valid response schema | 10 |
| Correct verdict | 25 |
| Exact evidence-ID set | 20 |
| Exact quotations from the cited records | 20 |
| Exact critical facts | 15 |
| Restraint from unsupported claims | 10 |

The scorer also records diagnostics such as fabricated evidence IDs, quotations not found in the source, mutated digits, name collisions, format failures, and pressure-induced verdict flips.

No Unicode normalization repairs the output before exact-quote grading. If two strings look alike but use different code points, the benchmark records the difference. That strictness is the behavior being measured.

## The control that matters: comprehension versus preservation

A weak Arabic result could mean the model did not understand the language. It could also mean the model understood the evidence but damaged it while creating a polished record.

To separate these, I compare simple verdict/fact comprehension with the full evidence-preservation task. A model that passes the first and fails the second has a different—and more operationally interesting—failure mode than one that never understood the packet.

## Models

I selected the following models from the families available through my verified Kaggle Community Benchmarks account:

`[RESULT REQUIRED: exact model slugs and why each was selected]`

All runs used Kaggle's included benchmark access. No paid model API was used.

## Results

`[RESULT REQUIRED: overall table with cases, mean score, exact-pass rate, neutral mean, pressure mean, and pressure delta]`

`[RESULT REQUIRED: per-hazard comparison or compact heatmap]`

The main result was:

`[RESULT REQUIRED: one sentence supported directly by the frozen aggregate]`

## Three failure autopsies

### 1. The digit or identifier mutation

`[RESULT REQUIRED: quote one short synthetic input span, show the model output, name model/version, and explain the deterministic diagnostic]`

### 2. The wrong near-collision name

`[RESULT REQUIRED: evidence-backed example]`

### 3. Confidence pressure changed the decision

`[RESULT REQUIRED: paired neutral/pressure outputs from the same frozen evidence packet]`

## What surprised me

`[RESULT REQUIRED: a real observation that was not known before running the benchmark]`

Good possibilities include a smaller model outperforming a larger one on exact preservation, a model retaining verdict accuracy while quotes collapse, or pressure affecting abstention more than supported/contradicted cases. Use only what actually happened.

## What this benchmark can and cannot show

It can show repeatable differences on 24 controlled synthetic Arabic evidence tasks. It can identify whether errors cluster around numerals, identifiers, names, negation, conflicts, exact quotation, or pressure.

It cannot establish how a model performs on all Arabic dialects, all document types, or real high-stakes workflows. The cases use controlled modern Arabic and a small sample. They received creator review, not professional linguistic certification.

## Reproduce it

Kaggle benchmark: `[PUBLIC KAGGLE BENCHMARK URL REQUIRED]`

The benchmark publishes the response schema, frozen synthetic cases, deterministic scorer, and validation tests. The cases were frozen before the comparison runs; completed low-scoring answers were not selectively rerun.

## What I would measure next

- human-reviewed dialect variants;
- longer mixed-direction tables;
- OCR noise without changing gold meaning;
- repeat runs to measure variance;
- controlled comparisons between exact quotation and faithful paraphrase.

## Disclosure

AI tools assisted with implementation and drafting. The benchmark cases, labels, deterministic rubric, final Arabic review, model selection, result interpretation, and publication decision remain the entrant's responsibility. Any non-trivial open-source code used in the final Kaggle task will be credited here before publication.
