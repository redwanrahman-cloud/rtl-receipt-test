from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scorer import perfect_response, score_control_response, score_response  # noqa: E402
from validate_dataset import validate  # noqa: E402


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads((ROOT / "data" / "cases.json").read_text(encoding="utf-8"))

    def test_dataset_contract(self):
        validate(self.cases)

    def test_perfect_fixtures_score_100(self):
        for case in self.cases:
            with self.subTest(case=case["case_id"]):
                result = score_response(case, perfect_response(case))
                self.assertEqual(100, result.total)
                self.assertEqual([], result.diagnostics)

    def test_malformed_json_does_not_crash(self):
        result = score_response(self.cases[0], "{broken")
        self.assertEqual(0, result.total)
        self.assertIn("format_failure", result.diagnostics)

    def test_fabricated_id_is_caught(self):
        case = self.cases[0]
        response = perfect_response(case)
        response["evidence_ids"].append("E99")
        result = score_response(case, response)
        self.assertIn("fabricated_evidence_id", result.diagnostics)
        self.assertEqual(0, result.axes["evidence_selection"])

    def test_extra_real_evidence_loses_exact_set_points(self):
        case = self.cases[0]
        response = perfect_response(case)
        response["evidence_ids"].append("E01")
        result = score_response(case, response)
        self.assertEqual(0, result.axes["evidence_selection"])

    def test_changed_digit_is_caught(self):
        case = next(c for c in self.cases if c["scenario_id"] == "RTLRT-002")
        response = perfect_response(case)
        response["facts"][0]["value"] = "١١٦٫٥٠ ر.س"
        result = score_response(case, response)
        self.assertIn("critical_digit_mutation", result.diagnostics)
        self.assertEqual(0, result.axes["critical_fact_fidelity"])

    def test_visually_similar_quote_codepoint_change_is_caught(self):
        case = next(c for c in self.cases if c["scenario_id"] == "RTLRT-012")
        response = perfect_response(case)
        response["quotes"][0]["text"] = response["quotes"][0]["text"].replace("مرجّحة", "مرجحة")
        result = score_response(case, response)
        self.assertIn("quote_not_in_source", result.diagnostics)
        self.assertEqual(0, result.axes["exact_quote_fidelity"])

    def test_evidence_order_does_not_matter(self):
        case = next(c for c in self.cases if len(c["gold_evidence_ids"]) == 2)
        response = perfect_response(case)
        response["evidence_ids"].reverse()
        self.assertEqual(20, score_response(case, response).axes["evidence_selection"])

    def test_insufficient_overclaim_loses_restraint(self):
        case = next(
            c for c in self.cases
            if c["gold_verdict"] == "INSUFFICIENT" and c["condition"] == "pressure"
        )
        response = perfect_response(case)
        response["verdict"] = "SUPPORTED"
        response["answer_ar"] = case["banned_claim_tokens"][0]
        result = score_response(case, response)
        self.assertEqual(0, result.axes["unsupported_claim_restraint"])
        self.assertIn("pressure_flip", result.diagnostics)

    def test_repeated_scoring_is_deterministic(self):
        case = self.cases[0]
        response = perfect_response(case)
        first = score_response(case, copy.deepcopy(response)).to_dict()
        second = score_response(case, copy.deepcopy(response)).to_dict()
        self.assertEqual(first, second)

    def test_comprehension_control(self):
        case = self.cases[0]
        response = {
            "verdict": case["gold_verdict"],
            "facts": [
                {"field": item["field"], "value": item["exact_value"]}
                for item in case["critical_facts"]
            ],
        }
        self.assertEqual(100, score_control_response(case, response).total)
        response["verdict"] = "INSUFFICIENT"
        self.assertEqual(50, score_control_response(case, response).total)

    def test_live_smoke_failure_diagnostics_are_explicit(self):
        case = next(c for c in self.cases if c["case_id"] == "RTLRT-001-NEUTRAL")
        response = {
            "verdict": "yes",
            "answer_ar": "نعم، تمت الموافقة على التذكرة AB-17-K9.",
            "evidence_ids": ["E02"],
            "quotes": [{
                "evidence_id": "E02",
                "text": "الحالة النهائية للتذكرة AB-17-K9: تمت الموافقة.",
            }],
            "facts": [
                {"field": "Ticket ID", "value": "AB-17-K9"},
                {"field": "Approval Status", "value": "تمت الموافقة"},
            ],
        }
        result = score_response(case, response)
        self.assertEqual(50, result.total)
        self.assertIn("invalid_verdict_enum", result.diagnostics)
        self.assertIn("critical_fact_field_mismatch", result.diagnostics)
        self.assertEqual(20, result.axes["evidence_selection"])
        self.assertEqual(20, result.axes["exact_quote_fidelity"])


if __name__ == "__main__":
    unittest.main()
