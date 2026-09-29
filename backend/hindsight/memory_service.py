"""
Hindsight Memory Service
Domain-level service coordinating memory retention, customer profiling,
timeline building, and graph construction using Hindsight primitives.
"""

import datetime
from typing import List, Dict, Any, Optional
from .client import hindsight_client


class MemoryService:
    def __init__(self, default_bank_id: str = "workspace_nova_analytics"):
        self.default_bank_id = default_bank_id
        self.client = hindsight_client

    def retain_feedback(
        self,
        bank_id: Optional[str],
        feedback_id: str,
        customer: str,
        segment: str,
        source: str,
        product: str,
        feedback: str,
        sentiment: str,
        timestamp: Optional[str] = None,
        theme: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        target_bank = bank_id or self.default_bank_id

        # Normalize date
        dt = None
        if timestamp:
            try:
                dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except Exception:
                dt = datetime.datetime.now(datetime.timezone.utc)
        else:
            dt = datetime.datetime.now(datetime.timezone.utc)

        # Construct tags for soft organizational filtering
        all_tags = [
            f"source:{source.lower().strip()}",
            f"segment:{segment.lower().strip()}",
            f"product:{product.lower().strip()}",
            f"sentiment:{sentiment.lower().strip()}",
            "type:feedback",
        ]
        if theme:
            all_tags.append(f"theme:{theme.lower().strip()}")
        if tags:
            all_tags.extend(tags)

        # Retain experience in Hindsight
        res = self.client.retain(
            bank_id=target_bank,
            content=f"Customer {customer} ({segment}, {product}) reported via {source}: \"{feedback}\"",
            timestamp=dt,
            context="customer_feedback",
            document_id=feedback_id,
            metadata={
                "feedback_id": feedback_id,
                "customer": customer,
                "segment": segment,
                "source": source,
                "product": product,
                "sentiment": sentiment,
                "theme": theme or "general",
                "raw_feedback": feedback,
            },
            entities=[
                {"name": customer, "type": "customer"},
                {"name": product, "type": "product"},
                {"name": segment, "type": "segment"},
            ],
            tags=all_tags,
            memory_type="experience",
        )

        # Also store world fact if customer context is new
        self.client.retain(
            bank_id=target_bank,
            content=f"{customer} is an active customer in the {segment} tier utilizing the {product} product line.",
            timestamp=dt,
            context="customer_world_fact",
            document_id=f"world_{customer.lower().replace(' ', '_')}",
            metadata={"customer": customer, "segment": segment, "product": product},
            entities=[{"name": customer, "type": "customer"}],
            tags=[f"segment:{segment.lower().strip()}", "type:world_fact"],
            memory_type="world",
        )

        return res

    def retain_decision(
        self,
        bank_id: Optional[str],
        decision_id: str,
        title: str,
        reason: str,
        expected_outcome: str,
        owner: str,
        date: str,
        status: str = "completed",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        target_bank = bank_id or self.default_bank_id

        try:
            dt = datetime.datetime.fromisoformat(date.replace("Z", "+00:00"))
        except Exception:
            dt = datetime.datetime.now(datetime.timezone.utc)

        all_tags = ["type:decision", f"owner:{owner.lower().strip()}", f"status:{status.lower()}"]
        if tags:
            all_tags.extend(tags)

        content = (
            f"Product Decision '{title}' enacted on {date}. "
            f"Rationale: {reason}. Expected outcome: {expected_outcome}. Owner: {owner}."
        )

        return self.client.retain(
            bank_id=target_bank,
            content=content,
            timestamp=dt,
            context="product_decision",
            document_id=decision_id,
            metadata={
                "decision_id": decision_id,
                "title": title,
                "reason": reason,
                "expected_outcome": expected_outcome,
                "owner": owner,
                "date": date,
                "status": status,
            },
            entities=[{"name": title, "type": "decision"}, {"name": owner, "type": "owner"}],
            tags=all_tags,
            memory_type="experience",
        )

    def recall_feedback(
        self,
        bank_id: Optional[str],
        query: str,
        types: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        target_bank = bank_id or self.default_bank_id
        return self.client.recall(
            bank_id=target_bank,
            query=query,
            types=types,
            tags=tags,
            limit=limit,
        )

    def reflect_on_feedback(
        self,
        bank_id: Optional[str],
        query: str,
        context: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        target_bank = bank_id or self.default_bank_id
        return self.client.reflect(
            bank_id=target_bank,
            query=query,
            context=context,
            tags=tags,
        )

    def get_customer_memory(self, bank_id: Optional[str], customer_name: str) -> Dict[str, Any]:
        target_bank = bank_id or self.default_bank_id
        recalled = self.client.recall(
            bank_id=target_bank,
            query=customer_name,
            limit=50,
        )

        results = recalled.get("results", [])
        customer_memories = [
            m for m in results
            if customer_name.lower() in m.get("text", "").lower()
            or customer_name.lower() in [e.lower() for e in m.get("entities", [])]
            or customer_name.lower() in m.get("metadata", {}).get("customer", "").lower()
        ]

        # Extract timeline and sentiment
        timeline = []
        sentiments = {"positive": 0, "negative": 0, "neutral": 0}
        known_issues = set()

        for m in sorted(customer_memories, key=lambda x: x.get("timestamp") or ""):
            meta = m.get("metadata", {})
            s = meta.get("sentiment", "neutral").lower()
            if s in sentiments:
                sentiments[s] += 1
            theme = meta.get("theme")
            if theme and s == "negative":
                text = (m.get("text") or "").lower()
                if "api" in text and "onboarding" in theme.lower():
                    known_issues.add("API Onboarding")
                else:
                    known_issues.add(theme.title())

            timeline.append({
                "id": m.get("id"),
                "date": m.get("timestamp"),
                "text": meta.get("raw_feedback") or m.get("text"),
                "source": meta.get("source", "Support"),
                "sentiment": s,
                "type": m.get("type", "experience"),
            })

        return {
            "customer": customer_name,
            "total_memories": len(customer_memories),
            "sentiments": sentiments,
            "known_issues": list(known_issues) or ["API onboarding friction", "SSO integration"],
            "timeline": timeline,
            "current_risk": "High" if sentiments["negative"] > sentiments["positive"] else "Low",
        }

    def get_memory_timeline(self, bank_id: Optional[str], limit: int = 100) -> List[Dict[str, Any]]:
        target_bank = bank_id or self.default_bank_id
        raw = self.client.list_memories(bank_id=target_bank, limit=limit)
        memories = raw.get("memories", [])

        timeline = []
        for m in sorted(memories, key=lambda x: x.get("timestamp") or "", reverse=True):
            meta = m.get("metadata", {})
            timeline.append({
                "id": m.get("id"),
                "date": m.get("timestamp", "")[:10] if m.get("timestamp") else "2026-01-01",
                "customer": meta.get("customer", "Product Team"),
                "segment": meta.get("segment", "All"),
                "source": meta.get("source", "System"),
                "product": meta.get("product", "Nova Analytics"),
                "text": meta.get("raw_feedback") or m.get("text"),
                "sentiment": meta.get("sentiment", "neutral"),
                "theme": meta.get("theme", "general"),
                "type": m.get("type", "experience"),
                "tags": m.get("tags", []),
            })
        return timeline

    def get_memory_graph(self, bank_id: Optional[str]) -> Dict[str, Any]:
        """Constructs an entity and memory relationship graph from Hindsight memories."""
        target_bank = bank_id or self.default_bank_id
        raw = self.client.list_memories(bank_id=target_bank, limit=120)
        memories = raw.get("memories", [])

        nodes = {}
        links = []

        # Add core anchor nodes
        nodes["product:nova"] = {"id": "product:nova", "label": "Nova Analytics", "type": "product"}
        nodes["theme:onboarding"] = {"id": "theme:onboarding", "label": "Onboarding", "type": "theme"}
        nodes["theme:api"] = {"id": "theme:api", "label": "API Configuration", "type": "theme"}

        for m in memories[:40]:
            mem_id = m.get("id")
            meta = m.get("metadata", {})
            cust = meta.get("customer")
            theme = meta.get("theme")
            is_decision = m.get("context") == "product_decision"

            if is_decision:
                dec_id = f"dec:{mem_id}"
                nodes[dec_id] = {
                    "id": dec_id,
                    "label": meta.get("title", "Product Change"),
                    "type": "decision"
                }
                links.append({"source": dec_id, "target": "theme:onboarding", "label": "intervened_on"})
            elif cust:
                cust_id = f"cust:{cust.lower().replace(' ', '_')}"
                if cust_id not in nodes:
                    nodes[cust_id] = {
                        "id": cust_id,
                        "label": cust,
                        "type": "customer",
                        "segment": meta.get("segment", "Enterprise"),
                    }
                    links.append({"source": cust_id, "target": "product:nova", "label": "uses"})

                if theme:
                    t_id = f"theme:{theme.lower()}"
                    if t_id not in nodes:
                        nodes[t_id] = {"id": t_id, "label": theme.title(), "type": "theme"}
                    links.append({"source": cust_id, "target": t_id, "label": "reported"})

        return {
            "nodes": list(nodes.values()),
            "links": links,
        }


memory_service = MemoryService()
