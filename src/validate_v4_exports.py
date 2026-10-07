"""Independently re-score private v4 exports and emit public-safe aggregates."""
from __future__ import annotations

import csv
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "results" / "private" / "rtl-receipt-test-v1" / "4"
PUBLIC = ROOT / "results" / "public"
sys.path.insert(0, str(ROOT / "src"))
from scorer import annotate_pressure_flips, score_control_response, score_response  # noqa: E402

CASES = json.loads((ROOT / "data" / "cases.json").read_text(encoding="utf-8"))
FULL_CASES = {c["case_id"]: c for c in CASES}
CONTROL_CASES = {c["scenario_id"]: c for c in CASES if c["condition"] == "neutral"}


def one_json(folder: Path, pattern: str) -> Path:
    matches = list(folder.rglob(pattern))
    if len(matches) != 1:
        raise RuntimeError(f"expected one {pattern} under {folder.name}, got {len(matches)}")
    return matches[0]


def analyze(folder: Path) -> tuple[dict, list[dict], list[dict], dict]:
    rows = json.loads(one_json(folder, "rtl_receipt_results.json").read_text(encoding="utf-8"))
    meta = json.loads(one_json(folder, "*.result.json").read_text(encoding="utf-8"))
    model = meta["agent_info"]["model_info"]["name"]
    if len(rows) != 36 or len({r["case_id"] for r in rows}) != 36:
        raise AssertionError(f"{model}: expected 36 unique records")
    full = [r for r in rows if r["kind"] == "full"]
    controls = [r for r in rows if r["kind"] == "control"]
    if {r["case_id"] for r in full} != set(FULL_CASES) or len(controls) != 12:
        raise AssertionError(f"{model}: case coverage mismatch")
    rescored = []
    for row in rows:
        result = (
            score_response(FULL_CASES[row["case_id"]], row["response"])
            if row["kind"] == "full"
            else score_control_response(CONTROL_CASES[row["scenario_id"]], row["response"])
        )
        if result.total != row["score"] or result.axes != row["axes"]:
            raise AssertionError(f"{model}: score mismatch at {row['case_id']}")
        copy = dict(row)
        copy["diagnostics"] = list(result.diagnostics)
        rescored.append(copy)
    rescored = annotate_pressure_flips(rescored)
    full = [r for r in rescored if r["kind"] == "full"]
    controls = [r for r in rescored if r["kind"] == "control"]
    kaggle_score = float(meta["verifier_result"]["rewards"]["score"])
    local_score = statistics.fmean(r["score"] for r in full)
    if abs(kaggle_score - local_score) > 1e-9:
        raise AssertionError(f"{model}: Kaggle/local mean mismatch")
    neutral = {r["scenario_id"]: r for r in full if r["condition"] == "neutral"}
    pressure = {r["scenario_id"]: r for r in full if r["condition"] == "pressure"}
    pairs = []
    for scenario in sorted(neutral):
        n, p = neutral[scenario], pressure[scenario]
        pairs.append({"model": model, "scenario_id": scenario, "hazard_family": n["hazard_family"],
                      "neutral_score": n["score"], "pressure_score": p["score"],
                      "delta": p["score"] - n["score"],
                      "pressure_flip": "pressure_flip" in p["diagnostics"]})
    hazards = []
    for hazard in sorted({r["hazard_family"] for r in full}):
        group = [r for r in full if r["hazard_family"] == hazard]
        hazards.append({"model": model, "hazard_family": hazard, "cases": len(group),
                        "mean_score": round(statistics.fmean(r["score"] for r in group), 4),
                        "exact_passes": sum(r["score"] == 100 for r in group)})
    diags = Counter(d for r in full for d in r.get("diagnostics", []))
    summary = {"model": model, "status": "completed", "full_cases": 24, "controls": 12,
               "kaggle_score": round(kaggle_score, 10), "local_score": round(local_score, 10),
               "exact_passes": sum(r["score"] == 100 for r in full),
               "exact_pass_rate": round(sum(r["score"] == 100 for r in full) / 24, 6),
               "neutral_mean": round(statistics.fmean(r["score"] for r in neutral.values()), 4),
               "pressure_mean": round(statistics.fmean(r["score"] for r in pressure.values()), 4),
               "pressure_delta": round(statistics.fmean(r["score"] for r in pressure.values()) - statistics.fmean(r["score"] for r in neutral.values()), 4),
               "pressure_flips": sum(p["pressure_flip"] for p in pairs),
               "control_mean": round(statistics.fmean(r["score"] for r in controls), 4),
               "schema_format_failures": diags.get("format_failure", 0),
               "diagnostics": dict(sorted(diags.items())),
               "input_tokens": meta["agent_result"]["n_input_tokens"],
               "output_tokens": meta["agent_result"]["n_output_tokens"],
               "cost_usd": meta["agent_result"]["cost_usd"]}
    return summary, hazards, pairs, meta


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


PUBLIC.mkdir(parents=True, exist_ok=True)
summaries, hazards, pairs = [], [], []
for folder in sorted(p for p in PRIVATE.iterdir() if p.is_dir()):
    summary, hs, ps, _ = analyze(folder)
    summaries.append(summary); hazards.extend(hs); pairs.extend(ps)
summaries.sort(key=lambda x: x["local_score"], reverse=True)
(PUBLIC / "v4-model-summary.json").write_text(json.dumps(summaries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
write_csv(PUBLIC / "v4-model-summary.csv", [{k: v for k, v in s.items() if k != "diagnostics"} for s in summaries])
write_csv(PUBLIC / "v4-hazard-metrics.csv", hazards)
write_csv(PUBLIC / "v4-paired-pressure-metrics.csv", pairs)
print(json.dumps(summaries, indent=2, ensure_ascii=False))
