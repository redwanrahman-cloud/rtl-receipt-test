# RTL Receipt Test — local Gate 1 package

This package tests whether language models preserve Arabic evidence exactly when records mix right-to-left prose with Latin identifiers, multiple numeral systems, similar names, negation, superseded records, exact quotations, and social pressure.

Everything in `data/cases.json` is fictional and newly authored. The package contains no IsnadLens material, religious source text, patient/clinic/employer/customer data, or copied third-party text.

## Current status

- 12 frozen base scenarios.
- 24 expanded cases: one neutral and one pressure condition per scenario.
- Balanced base labels: 4 `SUPPORTED`, 4 `CONTRADICTED`, 4 `INSUFFICIENT`.
- Six hazard families, two scenarios each.
- Deterministic scorer; no LLM judge.
- A 12-case verdict/fact comprehension control separates language understanding from full evidence-preservation behavior.
- Twelve local validation tests pass, including the exact live 50/100 smoke regression.
- No Kaggle or DEV account action has been taken.

## Files

- `data/cases.json` — frozen 24-case dataset.
- `src/base_scenarios.json` — human-authored 12-scenario source.
- `src/build_dataset.py` — deterministic pair expansion.
- `src/scorer.py` — 100-point deterministic grader.
- `src/validate_dataset.py` — dataset integrity checks.
- `src/aggregate_results.py` — analysis of preserved JSONL outputs.
- `schemas/response.schema.json` — public response contract.
- `tests/test_benchmark.py` — validation and adversarial scorer tests.
- `kaggle_task.py` — Kaggle Benchmarks adapter pending signed-in smoke test.
- `DEV-ARTICLE-DRAFT.md` — submission narrative with explicit result placeholders.

## Local verification

Use a functioning Python 3.10+ interpreter:

```text
python src/build_dataset.py
python src/validate_dataset.py
python -m unittest discover -s tests -v
```

Expected result: 24 cases validate and 10 tests pass.

## Frozen retry policy

- Infrastructure failures may be rerun and must be logged as such.
- A completed answer is never selectively rerun because its score is poor.
- If a platform supplies stochastic retries, use the same attempt count for every model and case or disable retries.
- Do not edit cases, gold labels, rubric, or banned tokens after observing comparison-model results. Any repair requires a new benchmark version and full rerun.

## Exact remaining signed-in actions for Redwan

These steps change external account state and must be done or explicitly authorized by Redwan:

1. Sign into DEV and confirm the challenge still exposes a working submission path despite the contradictory public “Live Ended” label.
2. Sign into the existing Kaggle account.
3. Confirm phone verification. If the account was created after December 15, 2025, complete Kaggle's additional identity verification if requested.
4. Open Kaggle Benchmarks → Create task. This may involve accepting Kaggle terms; Redwan must do that himself.
5. In the task notebook, run `list(kbench.llms.keys())` and save the visible model slugs plus timestamp.
6. Confirm the account shows free quota and does not request billing or payment. Stop if payment is required.
7. Upload/copy `kaggle_task.py`, `src/scorer.py`, and `data/cases.json` into the task environment, adjusting only file paths/import packaging—not cases or scoring.
8. Run one smoke case on one free model. Confirm the structured response parses and the deterministic score is saved.
9. If the smoke test works, save the task privately first and record its task URL/version.
10. Confirm at least four distinct model families can run all 24 cases within remaining free quota. If not, stop; do not add API credits.
11. Only after local and account gates pass, run the frozen matrix and download all raw results.
12. Review the Arabic cases and article claims personally. The package does not claim professional linguistic validation.
13. Approve making the Kaggle benchmark public.
14. Approve publishing the English DEV article with the required template and `#kagglechallenge` tag.
15. Test the public benchmark URL while logged out, then submit the DEV entry before the internal 21:00 Riyadh target on October 11.

No one should invent results in the article. Replace placeholders only from downloaded Kaggle run artifacts.
