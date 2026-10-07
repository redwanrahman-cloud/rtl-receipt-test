# Official requirements and release audit

**Rechecked:** 2026-10-07, Asia/Riyadh  
**Status:** Local release candidate in progress; not yet eligible for submission

## Authoritative requirements

| Requirement | Official basis | Current state |
|---|---|---|
| Entry deadline | October 11, 2026 at 11:59 PM PDT | Converts to October 12 at 09:59 Riyadh; internal target remains October 11 at 21:00 Riyadh |
| One entry | Contest page and specific rules | PASS plan: one DEV entry only |
| Adult/eligible DEV member | Contest FAQ and general rules | Account gates reported passed; entrant must personally confirm age/eligibility and accept rules |
| Work started during entry period | General rules | PASS: benchmark work began October 7, within September 23–October 11 period |
| Original/non-infringing entry | General rules | PASS locally: newly authored synthetic records; final entrant warranty remains personal/legal responsibility |
| Public Kaggle benchmark | Specific rules | BLOCKED: task/benchmark still private/not created publicly |
| Published DEV post using template and unique tag | Specific rules | BLOCKED: English draft exists but is unpublished and contains result/link placeholders |
| Overview of tasks | Specific rules | READY in draft |
| Models run and lineup rationale | Specific rules | BLOCKED: only one smoke model has run; full comparison lineup/results required |
| Findings and insights | Specific rules | BLOCKED: must come from frozen multi-model results, not invention |
| Public Kaggle link inside post | Contest page/specific rules | BLOCKED until benchmark is public |
| Required tag | Contest page | READY: `#kagglechallenge` / DEV front matter `kagglechallenge` |
| English for prize eligibility | Contest FAQ | READY: draft is English |
| AI assistance allowed | Contest FAQ | READY: disclosure included |
| Credit non-trivial prior/open-source work | Contest FAQ | READY locally; final article must credit Kaggle SDK and any added dependencies |

## Judging alignment

Official criteria, with no published weighting:

1. **Insights Shared** — requires real results, pressure deltas, comprehension-vs-preservation analysis, and bounded conclusions.
2. **Writing Quality** — draft uses a concrete opening, transparent method, failure autopsies, limitations, and reproduction instructions.
3. **Creativity in Approach** — controlled Arabic RTL/LTR evidence transfer, exact code-point fidelity, paired pressure conditions, and deterministic grading without an LLM judge.

Tie-break: highest positive reactions on the DEV post. This is not a reason to publish early with incomplete evidence.

## Submission mechanics

1. Create/save a Kaggle Benchmark task from the release notebook.
2. Run the frozen task against the approved multi-family lineup using included quota only.
3. Preserve exact outputs, model slugs, run URLs, timestamps, failures/retries, and quota display.
4. Build a Kaggle benchmark from the task and approved model runs.
5. Make the benchmark publicly accessible and verify it while logged out.
6. Replace every result/link placeholder in the English DEV article from preserved artifacts.
7. Use the official DEV submission template and `#kagglechallenge` tag.
8. Publish the DEV post.
9. Use the challenge's submission control to submit that post once.
10. Save confirmation URL/time/screenshots or equivalent receipts.

The official public page currently renders a contradictory `Challenge Status: Live Ended` label while the same page and specific rules state the October 11 deadline. Authenticated submission controls are therefore a mandatory final preflight check.

## Sources

- Challenge page: https://dev.to/challenges/kaggle-2026-09-23
- Contest-specific rules: https://dev.to/page/kaggle-2026-09-23-contest-rules
- General rules: https://dev.to/page/official-hackathon-rules
- Kaggle Benchmarks documentation: https://www.kaggle.com/docs/benchmarks
- Official quick start: https://github.com/Kaggle/kaggle-benchmarks/blob/ci/quick_start.md

## Audit verdict

The local methodology, synthetic dataset, scorer, schemas, tests, smoke evidence, runbook, and draft narrative are materially ready. The entry is **not submission-ready** until the full benchmark has real multi-model results, a public Kaggle URL, a placeholder-free article, and an authenticated DEV submission preflight.
