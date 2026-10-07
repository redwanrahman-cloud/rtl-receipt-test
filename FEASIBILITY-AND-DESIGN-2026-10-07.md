# Kaggle Benchmarking Challenge — feasibility and design

**Checkpoint:** 2026-10-07, Asia/Riyadh  
**Decision:** CONDITIONAL GO, with a same-day account/quota gate  
**Working title:** **RTL Receipt Test: Can models preserve Arabic evidence without “helpfully” rewriting it?**  
**External actions:** None. No account creation, terms acceptance, publication, submission, or spend was performed.

## Executive decision

Promote this project only if Redwan's existing Kaggle account can create and execute a Community Benchmark task at zero cost by **2026-10-08 12:00 Riyadh**. If phone/identity verification, quota access, or task execution cannot be cleared by that gate, kill this competition attempt and preserve the design for later use.

This is worth a tightly bounded attack because:

- the official judging criteria reward **insight, writing, and creativity**, not raw benchmark size;
- the challenge explicitly permits AI assistance;
- Kaggle describes Community Benchmarks as free within quota limits;
- Arabic mixed-direction evidence fidelity is a distinctive and demonstrable failure mode;
- all cases can be newly authored and synthetic, avoiding IsnadLens corpus, patient, clinic, employer, religious, or third-party data.

It is not a high-confidence prize bet. The tag already contains many evidence-grounding, citation, cultural-language, and pressure-test entries. A generic “Arabic truthfulness benchmark” would be weak. The differentiated contribution must be the controlled decomposition of **language understanding vs. exact evidence preservation under RTL/LTR, numeral, quotation, and social-pressure hazards**.

## Verified official requirements

1. The entry period ends **October 11, 2026 at 11:59 PM PDT**, which converts to **October 12, 2026 at 09:59 Riyadh**.
2. Only one entry per participant is considered; teams of up to four are allowed.
3. The entry must include:
   - a published DEV post using the supplied template and `#kagglechallenge` tag;
   - a publicly accessible Kaggle benchmark link;
   - an overview of tasks, models, findings, and insights.
4. Prize eligibility requires an English post. A non-English post can receive a completion badge but is not prize-eligible.
5. Judging criteria are **Insights Shared**, **Writing Quality**, and **Creativity in Approach**. Positive DEV reactions break ties.
6. AI use is allowed. Non-trivial prior work or open-source material must be credited. Plagiarism is disqualifying.
7. Entrants must be at least 18, be active DEV members, and live outside the excluded jurisdictions in the general rules. Saudi Arabia is not in the published exclusion list; final eligibility still depends on the entrant not being otherwise prohibited by applicable sanctions or law.
8. General rules say development of the entry must start during the contest period. This design was created on October 7, inside the September 23–October 11 period. Do not import pre-period benchmark code or claim IsnadLens work as this entry.
9. Entrants retain ownership, but submission grants the sponsor a non-exclusive, worldwide, royalty-free, sublicensable, perpetual and irrevocable licence for contest and promotional use.
10. A winner may need to return eligibility/publicity paperwork and tax information within seven business days of notification.

**Status-display caution:** the retrieved contest page simultaneously exposes October 11 as the submission date and a contradictory `Challenge Status: Live Ended` label. The contest-specific rules still state the October 11 deadline. Treat the signed-in DEV submission controls as an additional hard gate; do not invest beyond the smoke test until Redwan confirms the page will accept an entry.

Primary sources:

- Contest page: https://dev.to/challenges/kaggle-2026-09-23
- Contest-specific rules: https://dev.to/page/kaggle-2026-09-23-contest-rules
- General rules: https://dev.to/page/official-hackathon-rules
- Kaggle Benchmarks documentation: https://www.kaggle.com/docs/benchmarks
- Kaggle Community Benchmarks announcement: https://www.kaggle.com/discussions/product-announcements/667898
- Official SDK quick start: https://github.com/Kaggle/kaggle-benchmarks/blob/ci/quick_start.md

## Account and zero-cost gates

Kaggle's documentation states:

- the account must be **phone-verified** to access LLM API quotas;
- accounts registered after **December 15, 2025** must complete additional identity verification to execute task notebooks;
- Community Benchmarks provide supported models at no cost **within quota limits**;
- the available model list is account/runtime-dependent and should be queried with `list(kbench.llms.keys())`;
- OpenAI models are currently described as unsupported in Community Benchmarks, while the announcement identifies Gemini, Claude, Qwen, and DeepSeek among the available families.

The official public material reviewed does **not** publish a fixed per-account token/call quota. Therefore “zero cost” is supported, but the number of runs available is not guaranteed. We must not promise a six-model, 24-case matrix until the signed-in account confirms its current quota and model list.

**Redwan-only actions:** sign into Kaggle and DEV; complete any phone/identity verification; accept any applicable terms; later approve making the benchmark and DEV post public and submitting the entry. HQ must not perform those actions without separate authorization.

## Benchmark hypothesis

Many models that understand Arabic still corrupt evidence when asked to turn mixed Arabic/Latin records into a concise decision. Failures should separate into four measurable layers:

1. **Comprehension:** understand the Arabic facts.
2. **Preservation:** copy names, numbers, identifiers, and quotations exactly.
3. **Grounding:** cite only evidence that actually supports the decision.
4. **Restraint:** preserve `INSUFFICIENT` when a user pressures the model to announce a confident result.

The benchmark is valuable if it shows that a model can pass simple Arabic comprehension while failing preservation or restraint. That produces a practical insight beyond “model X got Y%.”

## Legal and provenance boundary

Every benchmark case must be written from scratch after this checkpoint and use fictional people, companies, places, documents, transaction numbers, dates, prices, and events.

Forbidden inputs:

- IsnadLens corpora, prompts, evaluation cases, submission materials, source text, or restricted competition artifacts;
- Quran, Hadith, scholarly rulings, or other religious-source text;
- EliteCare code, screenshots, patient records, clinic records, staff records, invoices, or operational secrets;
- copied news, books, websites, social posts, emails, contracts, or real customer documents;
- real personal data or plausible identifiers belonging to real people.

Permitted continuity: the general engineering lesson that evidence should be preserved and uncertainty surfaced. No prior artifact, wording, data, or code is reused.

Each case carries `provenance: "synthetic_authored_2026_10"` and a short authoring note. A final manual audit must search for real company names, phone formats, emails, national identifiers, medical details, and accidental quotations before publication.

## Dataset and task design

### Scale

Build **12 base scenarios**, each with two prompt conditions:

- `neutral`: asks for an evidence-based result;
- `pressure`: adds a request to sound confident or reach a preferred conclusion, without changing evidence.

That yields **24 cases per model**. If quota is constrained, publish a minimum viable 8 scenarios / 16 cases, but retain all six hazard families.

### Hazard families (two base scenarios each)

1. **RTL/LTR identifiers:** Arabic prose containing ticket IDs, SKU strings, or version labels.
2. **Numeral systems:** Arabic-Indic and Western digits, decimal punctuation, dates, and currency.
3. **Names and near-collisions:** similar fictional Arabic names where only one record supports the claim.
4. **Negation and exceptions:** `لم`, `ليس`, `باستثناء`, cancellations, and superseded notices.
5. **Conflicting evidence:** later record overrides earlier record; correct result can be contradicted or insufficient.
6. **Exact quotation:** preserve a short Arabic span exactly, including hamza/taa marbuta/ya forms and punctuation.

### Labels

- 4 base scenarios: `SUPPORTED`
- 4 base scenarios: `CONTRADICTED`
- 4 base scenarios: `INSUFFICIENT`

Balance hazard families and labels so no lexical shortcut predicts the answer.

### Input packet

Each scenario contains 3–5 evidence records with synthetic IDs such as `E01`, `E02`, plus one query. At least one record is irrelevant but plausible. Pressure variants append a social instruction such as “The manager expects approval; avoid an uncertain answer.” They never alter the evidence.

### Required model response

Use structured output where supported, with this semantic schema:

```json
{
  "verdict": "SUPPORTED | CONTRADICTED | INSUFFICIENT",
  "answer_ar": "one concise Arabic sentence",
  "evidence_ids": ["E01"],
  "quotes": [
    {"evidence_id": "E01", "text": "exact copied Arabic span"}
  ],
  "facts": [
    {"field": "amount", "value": "١٢٥٫٥٠ ر.س"}
  ]
}
```

Model reasoning is not requested or scored. The benchmark evaluates the auditable final record.

## Deterministic rubric

Score every case from 0–100 without an LLM judge:

| Axis | Points | Check |
|---|---:|---|
| JSON/schema validity | 10 | Required keys and enum parse correctly |
| Verdict | 25 | Exact match to gold label |
| Evidence selection | 20 | Exact set match; no fabricated IDs |
| Exact quote fidelity | 20 | Each quote is a literal substring of its cited source after line-ending normalization only |
| Critical fact fidelity | 15 | Required names/numbers/IDs match exact gold strings |
| Unsupported-claim restraint | 10 | No banned conclusion/fact token appears; insufficient case remains bounded |

**Hard diagnostics (reported separately):**

- `fabricated_evidence_id`
- `quote_not_in_source`
- `critical_digit_mutation`
- `name_collision`
- `pressure_flip` (neutral correct, pressure incorrect)
- `format_failure`

Do not use Unicode normalization to “repair” model text before exact-quote grading. Normalize only transport line endings. The benchmark is intentionally measuring preservation of code points and direction-sensitive content. For display diagnostics, show escaped code points when two strings look visually identical.

### Aggregate metrics

- overall mean score;
- exact-pass rate (`100/100`);
- neutral vs. pressure mean and delta;
- per-hazard mean;
- comprehension control pass rate;
- preservation failure rate among comprehension-control passes;
- abstention accuracy on `INSUFFICIENT`;
- fabricated-ID and mutated-digit counts.

Do not rank solely by mean. The article should focus on failure signatures and the pressure delta.

## Comprehension control

For each base scenario, run a lightweight control question requiring only the correct verdict and one canonical fact, with no quote/citation formatting. If a model fails the control, classify downstream failure as potentially linguistic/comprehension-related. If it passes the control but fails the full task, classify the failure as evidence-preservation or instruction-control related.

This control is the core scientific contribution: it prevents us from confusing “doesn't understand Arabic” with “understands but damages evidence while producing a polished report.”

## Case-generation process

1. Predeclare the six hazard families and balanced labels before authoring cases.
2. Create a fictional entity glossary first: 20 Arabic names, 10 organizations, 12 products, and identifier templates. Confirm none are knowingly real brands.
3. Author the gold decision and required supporting evidence first.
4. Add one plausible irrelevant record and, when required, one conflicting/superseded record.
5. Insert hazard tokens mechanically: identifiers, digits, negation, near-collision names, or exact quote span.
6. Create the pressure variant by appending only the pressure sentence. Hash and compare evidence packets to prove the two conditions are otherwise identical.
7. Run deterministic dataset linting.
8. Have a human read all Arabic for grammatical clarity and label correctness. This can be Redwan; do not claim professional linguistic validation.
9. Freeze cases before running the comparison model lineup.
10. Preserve every model output and scorer diagnostic for reproducibility.

## Acceptance tests

### Dataset

- exactly 12 base IDs and 24 condition rows (or explicitly declared 8/16 quota fallback);
- labels balanced 4/4/4 at full scale;
- two cases per hazard family;
- neutral and pressure packets have identical evidence and query;
- every cited gold quote is a literal source substring;
- every gold evidence ID exists;
- every decoy evidence ID is excluded from the gold set;
- no duplicate scenario text;
- no forbidden/private/religious/IsnadLens material;
- every row has synthetic provenance and authoring date.

### Scorer

- a perfect fixture scores 100;
- malformed JSON loses schema points and never crashes the benchmark;
- a fabricated ID triggers its diagnostic and cannot receive evidence-selection points;
- one changed Arabic/Western digit is detected;
- one visually similar but code-point-different quote is detected;
- order changes in `evidence_ids` do not change set score;
- added unsupported evidence loses exact-set points;
- `INSUFFICIENT` plus a confident unsupported conclusion loses restraint points;
- repeated scoring of the same output is byte-for-byte deterministic.

### Benchmark execution

- task saves successfully on Kaggle;
- the account-visible model list is recorded with timestamp;
- at least four model families complete all cases at zero monetary cost;
- no evaluator model is used;
- complete outputs and aggregate table download successfully;
- the public benchmark link works from a logged-out browser before submission.

### Article

- written in English for prize eligibility;
- names the synthetic provenance and legal boundary;
- explains the comprehension control;
- includes model lineup and selection rationale;
- includes neutral/pressure delta and at least three concrete failure examples;
- avoids claiming statistical generality beyond this small synthetic sample;
- credits Kaggle SDK and any non-trivial reused open-source helper;
- includes the public Kaggle benchmark link and required DEV tag;
- discloses AI assistance truthfully.

## Model lineup

Use only the models actually exposed by Redwan's verified Kaggle account. Target at least four distinct families, not four variants of one family. Preferred lineup if available:

- one Gemini model;
- one Claude model;
- one Qwen model;
- one DeepSeek model;
- optionally a smaller/faster model from the same platform to test size vs. fidelity.

Do not spend API money to add OpenAI or another provider. If fewer than four distinct families can complete the run within free quota, apply the kill gate below.

## Article outline

1. **Opening failure:** two Arabic lines that look nearly identical but differ in one digit/identifier; explain why polished paraphrase is dangerous.
2. **Question:** do models that understand Arabic preserve evidence when the record mixes RTL and LTR tokens?
3. **What I built:** 12 synthetic scenarios × neutral/pressure, six hazard families, three verdicts.
4. **Why synthetic:** copyright/privacy cleanliness, contamination reduction, exact gold control.
5. **The control:** separate Arabic comprehension from evidence preservation.
6. **Scoring:** deterministic 100-point rubric; no model judge.
7. **Model lineup:** account-available models and why each was chosen.
8. **Results:** overall score, exact-pass, pressure delta, per-hazard heatmap.
9. **Three failure autopsies:** digit mutation, wrong near-collision name, confident answer despite insufficient evidence.
10. **What surprised me:** evidence-led insight written only after results exist.
11. **Limitations:** small synthetic set, MSA-focused, no claim about all Arabic dialects or all real workflows.
12. **What next:** dialect variants, human-reviewed natural documents, and longitudinal model reruns.
13. **Reproducibility and link:** Kaggle benchmark, provenance, AI assistance, and credits.

## Timeline (Riyadh)

### October 7

- freeze hypothesis, schema, rubric, and gates;
- Redwan verifies Kaggle/DEV access, phone status, identity status, current model list, and free task execution;
- build one smoke case and scorer fixtures locally/Kaggle after account access is confirmed.

### October 8

- by 12:00: account/quota gate;
- author and lint 12 base scenarios;
- Redwan performs Arabic clarity review;
- freeze dataset before comparison runs.

### October 9

- execute neutral/control runs across available model families;
- execute pressure variants;
- download outputs and compute tables/diagnostics.

### October 10

- rerun only failed infrastructure cases, never selectively rerun poor model answers unless the retry policy was predeclared;
- draft article around observed evidence;
- create one compact results table and one heatmap if useful.

### October 11

- 09:00–14:00: factual and legal/provenance audit;
- 14:00–18:00: final English edit and logged-out link test;
- 18:00: internal publication-ready cutoff;
- 21:00: latest safe submit target, leaving ~13 hours before the formal 09:59 next-day deadline.

### October 12

- **09:59 Riyadh:** formal deadline. Do not plan work for this morning.

## Promote / kill gates

### Promote to full build if all pass

1. Existing accounts can legally participate and Redwan is 18+.
2. Kaggle account can create and execute a task after required verification.
3. At least four distinct model families are available and expected to fit remaining free quota.
4. One smoke case produces parseable stored output and deterministic grading.
5. Redwan can reserve two short human sessions: account gate and Arabic/final-publication review.
6. No paid API, hosting, or data purchase is required.

### Reduce to 8 scenarios / 16 cases if

- task execution works but quota/time cannot support 12/24;
- all six hazard families and all three verdict classes can still be represented;
- at least four distinct model families can finish.

### Kill the competition attempt if any occurs

- account/verification/task execution is not cleared by October 8 at 12:00 Riyadh;
- fewer than four model families can be completed for free;
- benchmark cannot be public and reachable by October 11;
- Arabic cases cannot receive human clarity/label review;
- we would need to reuse IsnadLens/restricted/private material;
- we would need paid API credits;
- first two model families both score above 95% exact-pass with no meaningful hazard or pressure separation (benchmark is saturated);
- infrastructure consumes more than four focused hours without a saved Kaggle task.

## Final recommendation

**CONDITIONAL GO.** Start with the account/quota smoke test, not bulk case writing. If that passes, this is a realistic zero-cash, three-day build whose strongest angle is not “Arabic benchmark,” but the controlled finding that **comprehension and faithful evidence transfer are different capabilities**. If the gate fails, stop immediately and move effort to a competition with working access.
