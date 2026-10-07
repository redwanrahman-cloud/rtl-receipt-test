"""Fail-fast deterministic validation for the benchmark dataset."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "cases.json"


def validate(cases: list[dict]) -> None:
    assert len(cases) == 24, f"expected 24 cases, got {len(cases)}"
    assert len({c["case_id"] for c in cases}) == 24
    by_scenario: dict[str, list[dict]] = defaultdict(list)
    for case in cases:
        by_scenario[case["scenario_id"]].append(case)
        assert case["provenance"] == "synthetic_authored_2026_10"
        source_by_id = {e["evidence_id"]: e["text_ar"] for e in case["evidence"]}
        assert len(source_by_id) == len(case["evidence"])
        assert set(case["gold_evidence_ids"]) <= set(source_by_id)
        for quote in case["gold_quotes"]:
            assert quote["evidence_id"] in source_by_id
            assert quote["text"] in source_by_id[quote["evidence_id"]]
    assert len(by_scenario) == 12
    for scenario_id, pair in by_scenario.items():
        assert {c["condition"] for c in pair} == {"neutral", "pressure"}, scenario_id
        assert len({c["packet_sha256"] for c in pair}) == 1, scenario_id
        invariant_keys = {
            "query_ar", "evidence", "gold_verdict", "gold_evidence_ids", "gold_quotes",
            "critical_facts", "banned_claim_tokens"
        }
        for key in invariant_keys:
            assert pair[0][key] == pair[1][key], (scenario_id, key)
    base_cases = [c for c in cases if c["condition"] == "neutral"]
    assert Counter(c["gold_verdict"] for c in base_cases) == {
        "SUPPORTED": 4, "CONTRADICTED": 4, "INSUFFICIENT": 4
    }
    assert Counter(c["hazard_family"] for c in base_cases) == {
        "rtl_ltr_identifier": 2,
        "numeral_system": 2,
        "name_collision": 2,
        "negation_exception": 2,
        "conflicting_evidence": 2,
        "exact_quote": 2,
    }


if __name__ == "__main__":
    cases = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    validate(cases)
    print(f"VALID: {len(cases)} cases, 12 matched pairs, balanced labels and hazards")
