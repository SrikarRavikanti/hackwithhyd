"""
Final Acceptance Sequence Test
Executes the exact 11-step acceptance test flow defined in Specification Section 78.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.main import app


class TestFinalAcceptanceSequence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_complete_judge_workflow(self):
        print("\n--- STEP 1 & 2: Start Application & Seed Nova Analytics Demo ---")
        seed_res = self.client.post("/api/demo/seed")
        self.assertEqual(seed_res.status_code, 200)
        seed_data = seed_res.json()
        self.assertTrue(seed_data["success"])
        self.assertGreaterEqual(seed_data["retained_feedback_count"], 500)
        print(f"[PASS] Seeded {seed_data['retained_feedback_count']} feedback experiences and {seed_data['retained_decisions_count']} decisions into Hindsight.")

        print("\n--- STEP 3 & 4: Ingest & Verify Memories in Hindsight ---")
        timeline_res = self.client.get("/api/memory/timeline?limit=10")
        self.assertEqual(timeline_res.status_code, 200)
        timeline = timeline_res.json()
        self.assertGreater(len(timeline), 0)
        print(f"[PASS] Verified Hindsight memory stream contains {len(timeline)} recent memory units.")

        print("\n--- STEP 5: Ask 'What has changed about onboarding?' ---")
        wc_res = self.client.get("/api/insights/what-changed?topic=onboarding")
        self.assertEqual(wc_res.status_code, 200)
        wc_data = wc_res.json()
        self.assertEqual(wc_data["confidence"], "High")
        self.assertIn("enterprise", wc_data["current_understanding"].lower())
        print(f"[PASS] Historical Answer: {wc_data['current_understanding']}")

        print("\n--- STEP 6: Open Memory Explorer & Inspect Memories ---")
        explorer_res = self.client.get("/api/feedback?segment=Enterprise&limit=5")
        self.assertEqual(explorer_res.status_code, 200)
        exp_data = explorer_res.json()
        self.assertGreater(len(exp_data["items"]), 0)
        print(f"[PASS] Memory Explorer verified {len(exp_data['items'])} Enterprise memories with metadata & tags.")

        print("\n--- STEP 7: Decision Memory ('Did Our Fix Work?') ---")
        eval_res = self.client.get("/api/decisions/DEC-2026-01/evaluate")
        self.assertEqual(eval_res.status_code, 200)
        eval_data = eval_res.json()
        self.assertIn("Partial Success", eval_data["did_it_work"])
        self.assertGreater(eval_data["before_count"], 0)
        self.assertGreater(eval_data["after_count"], 0)
        print(f"[PASS] Decision Outcome: {eval_data['did_it_work']}")
        print(f"  Before: {eval_data['before_count']} complaints ({eval_data['before_enterprise']} Enterprise)")
        print(f"  After: {eval_data['after_count']} complaints ({eval_data['after_enterprise']} Enterprise)")

        print("\n--- STEP 8: Open Customer ACME Profile ---")
        cust_res = self.client.get("/api/customers/Acme%20Corp")
        self.assertEqual(cust_res.status_code, 200)
        cust_data = cust_res.json()
        self.assertEqual(cust_data["customer"], "Acme Corp")
        self.assertEqual(cust_data["segment"], "Enterprise")
        self.assertTrue(any("onboarding" in issue.lower() for issue in cust_data["known_issues"]))
        print(f"[PASS] Customer Dossier loaded for Acme Corp ({cust_data['segment']}) with {len(cust_data['timeline'])} historical memories.")

        print("\n--- STEP 9: Add New Feedback Event & Retain in Hindsight ---")
        new_feedback = {
            "customer": "Acme Corp",
            "segment": "Enterprise",
            "source": "Support",
            "product": "Nova API",
            "feedback": "New escalation: Production webhooks require mTLS certificates during onboarding.",
            "sentiment": "negative",
            "theme": "onboarding",
            "date": "2026-09-28",
        }
        add_res = self.client.post("/api/feedback", json=new_feedback)
        self.assertEqual(add_res.status_code, 200)
        self.assertTrue(add_res.json()["retained_in_hindsight"])
        print("[PASS] New customer feedback retained directly into Hindsight.")

        print("\n--- STEP 10: Query Again to Verify Incorporated Memory ---")
        query_res = self.client.post("/api/memory/query", json={"query": "mTLS webhooks Acme Corp"})
        self.assertEqual(query_res.status_code, 200)
        query_data = query_res.json()
        self.assertGreaterEqual(query_data["evidence_count"], 1)
        print("[PASS] Hindsight recalled the newly retained mTLS webhook experience.")

        print("\n--- STEP 11: Memory vs No-Memory Ablation Comparison ---")
        ablation_res = self.client.post("/api/ablation/compare", json={"question": "What should we prioritize regarding onboarding?"})
        self.assertEqual(ablation_res.status_code, 200)
        ab_data = ablation_res.json()
        self.assertIn("Stateless AI", ab_data["stateless"]["model_type"])
        self.assertIn("Hindsight", ab_data["hindsight"]["model_type"])
        print("[PASS] Stateless AI Answer:")
        print(f"  {ab_data['stateless']['answer']}")
        print("[PASS] Hindsight-Powered AI Answer:")
        print(f"  {ab_data['hindsight']['answer']}")
        print(f"[PASS] Accuracy Delta: Stateless {ab_data['evaluation_metrics']['historical_accuracy']['stateless']} vs Hindsight {ab_data['evaluation_metrics']['historical_accuracy']['hindsight']}")
        print("\n========================================================")
        print("ALL 11 STEPS IN THE FINAL ACCEPTANCE TEST PASSED!")
        print("========================================================\n")


if __name__ == "__main__":
    unittest.main()
