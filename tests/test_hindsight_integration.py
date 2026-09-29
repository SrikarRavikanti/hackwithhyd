"""
Hindsight Integration Test Suite
Validates that retain(), recall(), reflect(), and observation consolidation work end-to-end.
"""

import sys
import os
import unittest
from datetime import datetime, timezone

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.hindsight.client import hindsight_client, LocalHindsightEngine
from backend.hindsight.memory_service import memory_service
from backend.hindsight.recall_service import recall_service
from backend.hindsight.reflect_service import reflect_service


class TestHindsightIntegration(unittest.TestCase):
    def setUp(self):
        self.test_bank = "test_bank_integration"
        hindsight_client.reset_bank(self.test_bank)

    def test_retain_and_recall_experience(self):
        # 1. Retain an experience
        res = memory_service.retain_feedback(
            bank_id=self.test_bank,
            feedback_id="TEST_001",
            customer="Acme Corp",
            segment="Enterprise",
            source="Support",
            product="Analytics",
            feedback="API configuration during onboarding takes 3 days and requires dev help.",
            sentiment="negative",
            timestamp="2026-02-10T12:00:00Z",
            theme="onboarding",
        )
        self.assertTrue(res.get("success"), "Retain operation must succeed")

        # 2. Recall the experience
        recalled = recall_service.query_evidence(
            bank_id=self.test_bank,
            query="API configuration onboarding",
            limit=5,
        )
        self.assertGreaterEqual(recalled["evidence_count"], 1, "Should recall at least one memory")
        evidence = recalled["evidence"][0]
        self.assertEqual(evidence["customer"], "Acme Corp")
        self.assertIn("API configuration", evidence["text"])

    def test_reflection_and_decision_tracking(self):
        # 1. Retain early feedback
        memory_service.retain_feedback(
            bank_id=self.test_bank,
            feedback_id="F1",
            customer="Acme Corp",
            segment="Enterprise",
            source="Support",
            product="Analytics",
            feedback="Initial onboarding is too confusing.",
            sentiment="negative",
            timestamp="2026-01-15T10:00:00Z",
            theme="onboarding",
        )
        memory_service.retain_feedback(
            bank_id=self.test_bank,
            feedback_id="F2",
            customer="Globex",
            segment="SMB",
            source="Interview",
            product="Analytics",
            feedback="Onboarding dashboard navigation is hard to follow.",
            sentiment="negative",
            timestamp="2026-02-01T10:00:00Z",
            theme="onboarding",
        )

        # 2. Retain product decision
        memory_service.retain_decision(
            bank_id=self.test_bank,
            decision_id="DEC_01",
            title="Launch Guided Onboarding V1",
            reason="Reduce onboarding navigation friction",
            expected_outcome="Reduce onboarding complaints by 50%",
            owner="Sarah (Product Lead)",
            date="2026-03-01T00:00:00Z",
            status="completed",
        )

        # 3. Retain post-decision feedback
        memory_service.retain_feedback(
            bank_id=self.test_bank,
            feedback_id="F3",
            customer="Globex",
            segment="SMB",
            source="Survey",
            product="Analytics",
            feedback="Guided onboarding makes setup instantaneous!",
            sentiment="positive",
            timestamp="2026-04-10T10:00:00Z",
            theme="onboarding",
        )
        memory_service.retain_feedback(
            bank_id=self.test_bank,
            feedback_id="F4",
            customer="Acme Corp",
            segment="Enterprise",
            source="Sales Call",
            product="Analytics",
            feedback="The UI guide is nice, but our developers still struggle with API keys and SSO setup.",
            sentiment="negative",
            timestamp="2026-05-15T10:00:00Z",
            theme="onboarding",
        )

        # 4. Reflect across memory
        reflection = reflect_service.reflect_on_topic(
            bank_id=self.test_bank,
            query="How has onboarding evolved, and did our fix work?",
        )
        self.assertIsNotNone(reflection.get("reasoning_narrative"))
        self.assertGreater(reflection.get("evidence_count", 0), 0)

        # 5. Closed-loop decision evaluation
        eval_res = reflect_service.evaluate_decision_outcome(
            decision_title="Launch Guided Onboarding V1",
            decision_date="2026-03-01",
            topic="onboarding",
            bank_id=self.test_bank,
        )
        self.assertEqual(eval_res["decision"], "Launch Guided Onboarding V1")
        self.assertGreaterEqual(eval_res["before_count"], 2)
        self.assertGreaterEqual(eval_res["after_count"], 2)
        self.assertIn("Partial Success", eval_res["did_it_work"])

    def test_tenant_isolation(self):
        # Retain in Bank A
        hindsight_client.retain(
            bank_id="tenant_a_bank",
            content="Top secret feature request from Tenant A",
            tags=["tenant:a"],
        )
        # Recall in Bank B
        recalled_b = hindsight_client.recall(
            bank_id="tenant_b_bank",
            query="Tenant A feature request",
        )
        self.assertEqual(len(recalled_b.get("results", [])), 0, "Hard isolation between banks must prevent leakage")


if __name__ == "__main__":
    unittest.main()
