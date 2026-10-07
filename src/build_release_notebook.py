"""Build the self-contained private Kaggle release notebook."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "RTL-Receipt-Test-KAGGLE-TASK.ipynb"
CASES = json.loads((ROOT / "data" / "cases.json").read_text(encoding="utf-8"))
SCORER = (ROOT / "src" / "scorer.py").read_text(encoding="utf-8")

def cell(kind: str, source: str) -> dict:
    item = {"cell_type": kind, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code":
        item.update({"execution_count": None, "outputs": []})
    return item

ADAPTER = '''@dataclass
class Quote:
    evidence_id: str
    text: str
@dataclass
class Fact:
    field: str
    value: str
@dataclass
class EvidenceResponse:
    verdict: str
    answer_ar: str
    evidence_ids: list[str]
    quotes: list[Quote]
    facts: list[Fact]
@dataclass
class ControlResponse:
    verdict: str
    facts: list[Fact]

def item_to_dict(item):
    return dict(item) if isinstance(item, dict) else vars(item)
def response_to_dict(response):
    raw = response if isinstance(response, dict) else vars(response)
    return {"verdict": raw.get("verdict"), "answer_ar": raw.get("answer_ar"),
            "evidence_ids": list(raw.get("evidence_ids", [])),
            "quotes": [item_to_dict(x) for x in raw.get("quotes", [])],
            "facts": [item_to_dict(x) for x in raw.get("facts", [])]}
def control_to_dict(response):
    raw = response if isinstance(response, dict) else vars(response)
    return {"verdict": raw.get("verdict"),
            "facts": [item_to_dict(x) for x in raw.get("facts", [])]}
'''

TASK = '''@kbench.task(name="rtl_receipt_test_v1")
def rtl_receipt_test_v1(llm) -> float:
    records, full_scores = [], []
    for case in CASES:
        with kbench.chats.new("full_" + case["case_id"]):
            raw = llm.prompt(case["prompt_ar"], schema=EvidenceResponse)
        response = response_to_dict(raw)
        scored = score_response(case, response).to_dict()
        full_scores.append(scored["total"])
        records.append({"kind": "full", "case_id": case["case_id"],
            "scenario_id": case["scenario_id"], "condition": case["condition"],
            "gold_verdict": case["gold_verdict"],
            "hazard_family": case["hazard_family"], "response": response,
            "score": scored["total"], "axes": scored["axes"],
            "diagnostics": scored["diagnostics"]})
    for case in (c for c in CASES if c["condition"] == "neutral"):
        with kbench.chats.new("control_" + case["scenario_id"]):
            raw = llm.prompt(case["control_prompt_ar"], schema=ControlResponse)
        response = control_to_dict(raw)
        scored = score_control_response(case, response).to_dict()
        records.append({"kind": "control", "case_id": case["scenario_id"] + "-CONTROL",
            "scenario_id": case["scenario_id"], "condition": "control",
            "hazard_family": case["hazard_family"], "response": response,
            "score": scored["total"], "axes": scored["axes"],
            "diagnostics": scored["diagnostics"]})
    records = annotate_pressure_flips(records)
    Path("rtl_receipt_results.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    kbench.assertions.assert_true(len(full_scores) == 24,
        expectation="All 24 frozen full cases must complete.")
    return float(sum(full_scores) / len(full_scores))
'''

GATE = '''RUN_AUTHORIZED = False
MODEL_SLUG = "google/gemini-2.5-flash"
if RUN_AUTHORIZED:
    if MODEL_SLUG not in VISIBLE_MODELS:
        raise ValueError(f"Model slug is not visible in this account: {MODEL_SLUG}")
    print(f"Running frozen task on exact model slug: {MODEL_SLUG}")
    run = rtl_receipt_test_v1.run(llm=kbench.llms[MODEL_SLUG])
    print(run)
    print(Path("rtl_receipt_results.json").resolve())
else:
    print("No model calls made. Set RUN_AUTHORIZED=True only after HQ approves the run.")
'''

NB = {"cells": [
    cell("markdown", "# RTL Receipt Test — Kaggle Community Benchmark task\n\nSelf-contained private release candidate with 24 frozen cases, 12 controls, and deterministic scoring. No credentials or paid-provider calls. The final cell defaults to no execution.\n"),
    cell("code", 'import json\nfrom dataclasses import dataclass\nfrom pathlib import Path\nimport kaggle_benchmarks as kbench\nVISIBLE_MODELS = sorted(str(x) for x in kbench.llms.keys())\nprint(f"Visible model count: {len(VISIBLE_MODELS)}")\nfor slug in VISIBLE_MODELS: print(slug)\n'),
    cell("markdown", "## Frozen release-v1 data\n\nGenerated from `data/cases.json`; SHA-256 `E5F4433A2A3D3B9E854428835BC836137EBE11632696D3F7E35C59D886AA5093`. Prompts disclose the exact verdict enum and required fact-field names, never gold values.\n"),
    cell("code", "CASES = " + repr(CASES) + '\nprint(f"Embedded cases: {len(CASES)}")\n'),
    cell("markdown", "## Deterministic scorer\n\nNo LLM judge or post-result synonym mapping.\n"),
    cell("code", SCORER), cell("code", ADAPTER),
    cell("markdown", "## Task\n\nEach model gets 24 full prompts and 12 controls. Low scores are never selectively retried; infrastructure failures fail the task and must be logged.\n"),
    cell("code", TASK),
    cell("markdown", "## Deliberate private execution gate\n\nOne run makes 36 prompts. Confirm included quota and exact model slug first. This does not publish.\n"),
    cell("code", GATE),
    cell("markdown", "## Post-run\n\nDownload `rtl_receipt_results.json`; record slug, run URL, timestamp, retries, and quota. Keep private until HQ review.\n")],
    "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                 "language_info": {"name": "python", "version": "3"}},
    "nbformat": 4, "nbformat_minor": 5}

OUT.write_text(json.dumps(NB, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"Wrote {OUT}")
