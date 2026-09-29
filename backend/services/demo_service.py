"""
Deterministic Demo Service
Powers the 90-second winning demo sequence and guided step-by-step learning arc.
Provides 1-click dataset seeding and bank reset.
"""

import os
import csv
import json
from typing import Dict, Any, Optional, List
from backend.hindsight.memory_service import memory_service
from backend.hindsight.client import hindsight_client
from backend.services.feedback_service import feedback_service


class DemoService:
    def __init__(self):
        self.memory_service = memory_service
        self.feedback_service = feedback_service

    def seed_demo_data(self, bank_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Seeds the full Nova Analytics dataset into Hindsight.
        """
        target_bank = bank_id or "workspace_nova_analytics"
        csv_path = "data/nova_analytics_feedback.csv"
        decisions_path = "data/nova_analytics_decisions.json"

        # 1. Reset target bank first
        hindsight_client.reset_bank(target_bank)

        # 2. Ingest feedback CSV
        retained_feedback = 0
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.memory_service.retain_feedback(
                        bank_id=target_bank,
                        feedback_id=row.get("feedback_id", ""),
                        customer=row.get("customer", ""),
                        segment=row.get("segment", "SMB"),
                        source=row.get("source", "Support"),
                        product=row.get("product", "Nova Analytics"),
                        feedback=row.get("feedback", ""),
                        sentiment=row.get("sentiment", "neutral"),
                        timestamp=row.get("date"),
                        theme=row.get("theme", "general"),
                    )
                    retained_feedback += 1

        # 3. Ingest product decisions
        retained_decisions = 0
        if os.path.exists(decisions_path):
            with open(decisions_path, "r", encoding="utf-8") as f:
                decisions = json.load(f)
                for dec in decisions:
                    self.memory_service.retain_decision(
                        bank_id=target_bank,
                        decision_id=dec.get("id"),
                        title=dec.get("title"),
                        reason=dec.get("reason"),
                        expected_outcome=dec.get("expected_outcome"),
                        owner=dec.get("owner"),
                        date=dec.get("date"),
                        status=dec.get("status", "completed"),
                        tags=dec.get("tags", []),
                    )
                    retained_decisions += 1

        return {
            "success": True,
            "bank_id": target_bank,
            "retained_feedback_count": retained_feedback,
            "retained_decisions_count": retained_decisions,
            "status": f"Successfully initialized memory bank with {retained_feedback} experiences and {retained_decisions} decisions.",
        }

    def reset_demo(self, bank_id: Optional[str] = None) -> Dict[str, Any]:
        target_bank = bank_id or "workspace_nova_analytics"
        hindsight_client.reset_bank(target_bank)
        return {
            "success": True,
            "bank_id": target_bank,
            "message": f"Memory bank '{target_bank}' has been reset to empty.",
        }

    def get_guided_demo_steps(self) -> List[Dict[str, Any]]:
        """Returns the 5-step guided learning demo scenario."""
        return [
            {
                "step": 1,
                "title": "Single Isolated Feedback Event",
                "action": "Add feedback: Acme Corp - 'Onboarding is confusing.'",
                "question": "What is our customer onboarding problem?",
                "agent_response": "I don't have enough historical context or corroborating memories yet (1 isolated memory). Insufficient evidence to establish a pattern.",
                "hindsight_state": "1 experience retained; 0 observations consolidated.",
            },
            {
                "step": 2,
                "title": "Accumulation & Consolidation",
                "action": "Ingest 5 more customer feedback events across Support and Interviews.",
                "question": "What is the biggest onboarding problem?",
                "agent_response": "Enterprise customers consistently report that API configuration and credential provisioning is the primary onboarding friction point.",
                "hindsight_state": "6 experiences retained; Observation 'Enterprise API Bottleneck' consolidated.",
            },
            {
                "step": 3,
                "title": "Product Team Intervention",
                "action": "Record Product Decision: 'Launch API Setup Wizard' (March 15).",
                "question": "What product changes were made?",
                "agent_response": "Product team enacted 'API Setup Wizard' to automate credential provisioning and reduce enterprise friction.",
                "hindsight_state": "Decision retained in memory with context='product_decision'.",
            },
            {
                "step": 4,
                "title": "New Post-Decision Feedback Arrives",
                "action": "Ingest subsequent feedback: 'The wizard is better for basic keys, but advanced API configuration and SSO still requires engineering support.'",
                "question": "Did the API wizard solve the problem?",
                "agent_response": "The intervention was a partial success. It eliminated simple credential generation friction, but unmasked a deeper enterprise requirement for custom IAM and VPC peering.",
                "hindsight_state": "Closed-loop feedback completed: Problem -> Decision -> Outcome.",
            },
            {
                "step": 5,
                "title": "Long-term Strategic Synthesis",
                "action": "Query high-level product priority.",
                "question": "If we prioritize onboarding this quarter, what should we do?",
                "agent_response": "Focus exclusively on Enterprise API and SSO automation rather than another general UI redesign. SMBs are already satisfied (CSAT 92%), while enterprise deals face 3-week delays.",
                "hindsight_state": "Multi-hop temporal reasoning across 7 months of memory.",
            }
        ]


demo_service = DemoService()
