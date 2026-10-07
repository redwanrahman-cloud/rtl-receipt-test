"""Kaggle Benchmarks adapter.

This file is intentionally not executed locally during Gate 1 because model access and
`kaggle_benchmarks` are provided by the signed-in Kaggle environment. Copy the scorer
and frozen cases into the task environment before the first smoke run.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import kaggle_benchmarks as kbench

from scorer import score_control_response, score_response


@dataclass
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


def _item_to_dict(item) -> dict:
    """Accept nested dataclass objects or dicts returned by Kaggle providers."""
    if isinstance(item, dict):
        return dict(item)
    return vars(item)


def response_to_dict(response: EvidenceResponse | dict) -> dict:
    if isinstance(response, dict):
        raw = response
    else:
        raw = vars(response)
    return {
        "verdict": raw.get("verdict"),
        "answer_ar": raw.get("answer_ar"),
        "evidence_ids": list(raw.get("evidence_ids", [])),
        "quotes": [_item_to_dict(item) for item in raw.get("quotes", [])],
        "facts": [_item_to_dict(item) for item in raw.get("facts", [])],
    }


def control_to_dict(response: ControlResponse | dict) -> dict:
    raw = response if isinstance(response, dict) else vars(response)
    return {
        "verdict": raw.get("verdict"),
        "facts": [_item_to_dict(item) for item in raw.get("facts", [])],
    }


@kbench.task(name="rtl_receipt_case", store_task=False)
def rtl_receipt_case(llm, case_json: str) -> float:
    case = json.loads(case_json)
    response = llm.prompt(case["prompt_ar"], schema=EvidenceResponse)
    result = score_response(case, response_to_dict(response))
    kbench.assertions.assert_true(
        result.total >= 0,
        expectation="The response must receive a deterministic evidence-fidelity score.",
    )
    return float(result.total)


@kbench.task(name="rtl_receipt_test")
def rtl_receipt_test(llm) -> float:
    cases_path = Path("cases.json")
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    scores = []
    for case in cases:
        scores.append(
            rtl_receipt_case.run(
                llm=llm,
                case_json=json.dumps(case, ensure_ascii=False),
            ).result
        )
    mean_score = sum(scores) / len(scores)
    kbench.assertions.assert_true(
        len(scores) == 24,
        expectation="All 24 frozen neutral/pressure cases must complete.",
    )
    return float(mean_score)


@kbench.task(name="rtl_receipt_comprehension_control")
def rtl_receipt_comprehension_control(llm) -> float:
    cases = json.loads(Path("cases.json").read_text(encoding="utf-8"))
    neutral_cases = [case for case in cases if case["condition"] == "neutral"]
    scores = []
    for case in neutral_cases:
        response = llm.prompt(case["control_prompt_ar"], schema=ControlResponse)
        scores.append(score_control_response(case, control_to_dict(response)).total)
    kbench.assertions.assert_true(
        len(scores) == 12,
        expectation="The comprehension control must cover all 12 base scenarios.",
    )
    return float(sum(scores) / len(scores))


rtl_receipt_test.run(kbench.llm)
rtl_receipt_comprehension_control.run(kbench.llm)
