"""
Hindsight Recall Service
Specialized retrieval orchestration: executes multi-strategy searches,
applies tag filters, extracts entity connections, and formats evidence payloads.
"""

from typing import List, Dict, Any, Optional
from .client import hindsight_client


class RecallService:
    def __init__(self, default_bank_id: str = "workspace_nova_analytics"):
        self.default_bank_id = default_bank_id
        self.client = hindsight_client

    def query_evidence(
        self,
        query: str,
        bank_id: Optional[str] = None,
        segment: Optional[str] = None,
        source: Optional[str] = None,
        theme: Optional[str] = None,
        limit: int = 15,
    ) -> Dict[str, Any]:
        target_bank = bank_id or self.default_bank_id

        tags = []
        if segment:
            tags.append(f"segment:{segment.lower()}")
        if source:
            tags.append(f"source:{source.lower()}")
        if theme:
            tags.append(f"theme:{theme.lower()}")

        raw = self.client.recall(
            bank_id=target_bank,
            query=query,
            tags=tags if tags else None,
            limit=limit,
        )

        results = raw.get("results", [])
        evidence_cards = []

        for r in results:
            meta = r.get("metadata", {})
            evidence_cards.append({
                "id": r.get("id"),
                "text": meta.get("raw_feedback") or r.get("text"),
                "customer": meta.get("customer", "Enterprise User"),
                "segment": meta.get("segment", "Enterprise"),
                "source": meta.get("source", "Support"),
                "sentiment": meta.get("sentiment", "neutral"),
                "date": r.get("timestamp", "")[:10] if r.get("timestamp") else "2026-03-01",
                "type": r.get("type", "experience"),
                "relevance_score": r.get("scores", {}).get("relevance", 0.85),
                "tags": r.get("tags", []),
            })

        return {
            "query": query,
            "bank_id": target_bank,
            "evidence_count": len(evidence_cards),
            "evidence": evidence_cards,
            "entities": list(raw.get("entities", {}).keys()),
            "trace": raw.get("trace", {}),
        }


recall_service = RecallService()
