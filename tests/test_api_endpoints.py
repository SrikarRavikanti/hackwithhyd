"""
API Endpoints Test Suite
Validates the FastAPI application REST endpoints using Starlette TestClient.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.main import app


class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "online")
        self.assertTrue(data["hindsight_connected"])

    def test_analytics_overview(self):
        res = self.client.get("/api/analytics/overview")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_feedback", data)
        self.assertIn("active_themes", data)

    def test_what_changed(self):
        res = self.client.get("/api/insights/what-changed?topic=onboarding")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["topic"], "onboarding")
        self.assertIn("current_understanding", data)
        self.assertGreater(len(data["narrative_points"]), 0)

    def test_memory_ablation_comparison(self):
        res = self.client.post("/api/ablation/compare", json={"question": "What should we prioritize regarding onboarding?"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("stateless", data)
        self.assertIn("hindsight", data)
        self.assertIn("evaluation_metrics", data)

    def test_decision_fix_evaluation(self):
        res = self.client.get("/api/decisions/DEC-2026-01/evaluate")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("did_it_work", data)
        self.assertIn("before_count", data)
        self.assertIn("after_count", data)

    def test_natural_language_query(self):
        res = self.client.post("/api/memory/query", json={"query": "enterprise onboarding"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("answer", data)
        self.assertIn("evidence", data)


if __name__ == "__main__":
    unittest.main()
