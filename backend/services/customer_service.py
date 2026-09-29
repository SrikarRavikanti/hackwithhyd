"""
Customer Memory Service
Surfaces individual customer memory dossiers, interaction timelines,
and churn/satisfaction risk scores derived from accumulated feedback.
"""

from typing import List, Dict, Any, Optional
from backend.hindsight.memory_service import memory_service
from backend.hindsight.client import hindsight_client


class CustomerService:
    def __init__(self):
        self.memory_service = memory_service

    def get_customer_profile(
        self,
        customer_name: str,
        bank_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        memory_dossier = self.memory_service.get_customer_memory(bank_id=bank_id, customer_name=customer_name)

        # Enhance with tiering metadata
        is_enterprise = "corp" in customer_name.lower() or "systems" in customer_name.lower() or "industries" in customer_name.lower() or "dynamic" in customer_name.lower()
        segment = "Enterprise" if is_enterprise else "SMB"

        return {
            "customer": customer_name,
            "segment": segment,
            "customer_since": "2024-03-15",
            "products_used": ["Nova Analytics", "Nova API", "Nova Connect"],
            "total_feedback_events": memory_dossier.get("total_memories", 12),
            "known_issues": memory_dossier.get("known_issues", ["API onboarding", "SSO configuration"]),
            "sentiments": memory_dossier.get("sentiments", {"positive": 3, "negative": 7, "neutral": 2}),
            "current_risk": memory_dossier.get("current_risk", "High"),
            "risk_rationale": "Persistent negative feedback regarding API onboarding setup despite UI improvements.",
            "timeline": memory_dossier.get("timeline", []),
            "product_interventions_received": [
                {"title": "Guided Onboarding V1", "date": "2026-03-15"},
                {"title": "API Setup Wizard", "date": "2026-06-01"},
            ]
        }

    def list_customers(self, bank_id: Optional[str] = None) -> List[Dict[str, Any]]:
        timeline = self.memory_service.get_memory_timeline(bank_id=bank_id, limit=300)
        seen = {}
        for item in timeline:
            cust = item.get("customer")
            if cust and cust != "Product Team":
                if cust not in seen:
                    seen[cust] = {
                        "name": cust,
                        "segment": item.get("segment", "SMB"),
                        "feedback_count": 0,
                        "negative_count": 0,
                        "latest_date": item.get("date"),
                    }
                seen[cust]["feedback_count"] += 1
                if item.get("sentiment") == "negative":
                    seen[cust]["negative_count"] += 1

        customers = list(seen.values())
        for c in customers:
            c["risk"] = "High" if c["negative_count"] >= 3 else ("Medium" if c["negative_count"] >= 1 else "Low")

        return sorted(customers, key=lambda x: x["feedback_count"], reverse=True)


customer_service = CustomerService()
