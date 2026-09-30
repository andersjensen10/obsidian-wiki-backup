from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import mission_card  # noqa: E402


class MissionCardTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((ROOT / "fixtures" / name).read_text())

    def test_ready_fixture_is_deterministic_and_reviewable(self):
        card = self.load("ready-local-cpu.json")
        first = mission_card.render(card)
        second = mission_card.render(card)
        self.assertEqual(first, second)
        self.assertIn("**Status:** READY FOR REVIEW", first)
        self.assertIn("## Morning question", first)

    def test_busy_spark_is_explicitly_deferred(self):
        rendered = mission_card.render(self.load("busy-spark.json"))
        self.assertIn("**Status:** DEFERRED", rendered)
        self.assertIn("- **State:** busy", rendered)

    def test_missing_rollback_is_rejected(self):
        with self.assertRaisesRegex(mission_card.MissionCardError, "rollback"):
            mission_card.validate(self.load("invalid-missing-rollback.json"))

    def test_busy_spark_cannot_claim_promotion(self):
        card = self.load("busy-spark.json")
        card["promotionDecision"] = "prototype complete"
        with self.assertRaisesRegex(mission_card.MissionCardError, "requires promotionDecision = deferred"):
            mission_card.validate(card)

    def test_missing_morning_question_is_rejected(self):
        card = self.load("ready-local-cpu.json")
        card["morningQuestion"] = ""
        with self.assertRaisesRegex(mission_card.MissionCardError, "morningQuestion"):
            mission_card.validate(card)


if __name__ == "__main__":
    unittest.main()
