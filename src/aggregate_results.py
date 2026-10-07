"""Aggregate saved JSONL run records without changing or rerunning model outputs."""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path


def aggregate(path: Path) -> dict:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    by_model: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_model[row["model"]].append(row)
    output = {}
    for model, model_rows in sorted(by_model.items()):
        conditions: dict[str, list[float]] = defaultdict(list)
        hazards: dict[str, list[float]] = defaultdict(list)
        diagnostics: dict[str, int] = defaultdict(int)
        for row in model_rows:
            conditions[row["condition"]].append(row["score"])
            hazards[row["hazard_family"]].append(row["score"])
            for diagnostic in row.get("diagnostics", []):
                diagnostics[diagnostic] += 1
        neutral = statistics.fmean(conditions.get("neutral", [0]))
        pressure = statistics.fmean(conditions.get("pressure", [0]))
        output[model] = {
            "cases": len(model_rows),
            "mean_score": round(statistics.fmean(r["score"] for r in model_rows), 2),
            "exact_pass_rate": round(sum(r["score"] == 100 for r in model_rows) / len(model_rows), 4),
            "neutral_mean": round(neutral, 2),
            "pressure_mean": round(pressure, 2),
            "pressure_delta": round(pressure - neutral, 2),
            "hazard_means": {
                key: round(statistics.fmean(values), 2) for key, values in sorted(hazards.items())
            },
            "diagnostics": dict(sorted(diagnostics.items())),
        }
    return output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: aggregate_results.py results.jsonl")
    print(json.dumps(aggregate(Path(sys.argv[1])), ensure_ascii=False, indent=2))
