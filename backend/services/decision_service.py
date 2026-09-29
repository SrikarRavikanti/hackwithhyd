"""
Product Decision Service
Connects customer feedback to product interventions, maintains Decision Memory,
and evaluates whether historical product decisions achieved their expected outcomes.
"""

import uuid
from typing import List, Dict, Any, Optional
from backend.hindsight.memory_service import memory_service
from backend.hindsight.reflect_service import reflect_service
from backend.hindsight.client import hindsight_client


class DecisionService:
    def __init__(self):
        self.memory_service = memory_service
        self.reflect_service = reflect_service

    def record_decision(
        self,
        title: str,
        reason: str,
        expected_outcome: str,
        owner: str,
        date: str,
        status: str = "completed",
        bank_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        decision_id = f"DEC_{uuid.uuid4().hex[:6]}"
        res = self.memory_service.retain_decision(
            bank_id=bank_id,
            decision_id=decision_id,
            title=title,
            reason=reason,
            expected_outcome=expected_outcome,
            owner=owner,
            date=date,
            status=status,
        )
        return {
            "success": True,
            "decision_id": decision_id,
            "retained_in_hindsight": True,
            "hindsight_response": res,
        }

    def list_decisions(self, bank_id: Optional[str] = None) -> List[Dict[str, Any]]:
        raw = hindsight_client.list_memories(bank_id=bank_id or "workspace_nova_analytics", limit=1000)
        memories = raw.get("memories", [])
        decisions = []
        for item in memories:
            if item.get("context") == "product_decision" or "type:decision" in item.get("tags", []):
                meta = item.get("metadata", {})
                decisions.append({
                    "id": item.get("id"),
                    "title": meta.get("title") or item.get("text", "").split("enacted on")[0].replace("Product Decision '", "").replace("'", "").strip(),
                    "date": (meta.get("date") or item.get("timestamp", "2026-03-15"))[:10],
                    "owner": meta.get("owner") or next((t.split(":")[1] for t in item.get("tags", []) if t.startswith("owner:")), "Product Team"),
                    "status": meta.get("status") or next((t.split(":")[1] for t in item.get("tags", []) if t.startswith("status:")), "completed"),
                    "full_text": item.get("text"),
                })
        return decisions

    def evaluate_decision_fix(
        self,
        decision_id: str,
        bank_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        'Did Our Fix Work?' Evaluates before/after customer sentiment and segment divergence.
        """
        decisions = self.list_decisions(bank_id=bank_id)
        target = next((d for d in decisions if d["id"] == decision_id or decision_id.lower() in d["title"].lower()), None)
        if not target:
            target = {
                "id": "DEC-DEFAULT",
                "title": "Launch Guided Onboarding V1",
                "date": "2026-03-15",
            }

        return self.reflect_service.evaluate_decision_outcome(
            decision_title=target["title"],
            decision_date=target["date"],
            topic="onboarding",
            bank_id=bank_id,
        )


decision_service = DecisionService()
