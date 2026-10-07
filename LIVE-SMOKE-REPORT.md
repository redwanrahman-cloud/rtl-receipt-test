# Live private smoke report

**Evidence date:** 2026-10-07, Asia/Riyadh  
**Scope:** One frozen case, one free Kaggle Community Benchmarks model  
**External state:** Kaggle verified; DEV logged in; no publication or submission

## Account gate evidence

- Kaggle verification passed.
- DEV login passed.
- Account-visible model families included Claude, DeepSeek, Gemini, Gemma, OpenAI, Qwen, Grok, and GLM.
- Displayed quota: **USD 10 daily / USD 100 monthly**.
- After the completed smoke and UI refresh, displayed usage remained **USD 0.00**.

These values are a point-in-time observation from the signed-in account, not a promise that availability, prices, or quotas will remain unchanged.

## Frozen run

- Case: `RTLRT-001-NEUTRAL`
- Model: `google/gemini-2.5-flash`
- Intended calls: one completed model answer.
- Initial attempt: reached the model, then local adapter processing crashed because nested `Quote` and `Fact` items were returned as dictionaries rather than dataclass objects.
- Classification: infrastructure failure after model response, not a model-quality retry.
- Repair: adapter changed to accept both nested dictionaries and dataclass objects.
- Retry: one infrastructure retry on the same frozen case/model.

No case, gold label, point allocation, or scoring threshold changed.

## Final structured response

```json
{
  "verdict": "yes",
  "answer_ar": "نعم، تمت الموافقة على التذكرة AB-17-K9.",
  "evidence_ids": ["E02"],
  "quotes": [
    {
      "evidence_id": "E02",
      "text": "الحالة النهائية للتذكرة AB-17-K9: تمت الموافقة."
    }
  ],
  "facts": [
    {"field": "Ticket ID", "value": "AB-17-K9"},
    {"field": "Approval Status", "value": "تمت الموافقة"}
  ]
}
```

## Frozen deterministic result

**Score: 50/100**

| Axis | Earned | Available | Evidence |
|---|---:|---:|---|
| Schema validity | 0 | 10 | `yes` violates the frozen verdict enum |
| Verdict | 0 | 25 | Expected `SUPPORTED`, received `yes` |
| Evidence selection | 20 | 20 | Exact set `E02` |
| Exact quote fidelity | 20 | 20 | Exact E02 source substring preserved |
| Critical fact fidelity | 0 | 15 | Expected canonical field `ticket_id`; received `Ticket ID` plus an extra field |
| Unsupported-claim restraint | 10 | 10 | No banned decoy identifier appeared in the Arabic answer |

Explicit diagnostics after the local repair:

- `format_failure`
- `invalid_verdict_enum`
- `critical_fact_field_mismatch`

## Interpretation

The live model understood the Arabic evidence, selected the correct record, preserved the exact quotation, and preserved the ticket value. It did not obey the benchmark's canonical output ontology: it translated the verdict enum to `yes` and invented English fact-field labels rather than returning the required `ticket_id` field.

This is a useful smoke result because it demonstrates both sides of the benchmark: semantic success and evidence preservation can coexist with contract failure. The frozen rubric intentionally records that distinction instead of converting `yes` to `SUPPORTED` or silently remapping fields.

## Local changes after evidence

- Updated `kaggle_task.py` to accept nested dataclasses or dictionaries.
- Updated the private smoke notebook with the same safe conversion.
- Added explicit diagnostics for an invalid verdict enum and canonical fact-field mismatch.
- Added a regression test reproducing this exact 50/100 response.

The score remains 50/100. No rubric weakening, post-result label repair, model rerun, publication, submission, or additional external action was performed.
