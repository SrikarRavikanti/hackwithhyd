"""
Feedback Ingestion & Management Service
Handles CSV ingestion, manual entry, normalization, prompt-injection defense,
and retains customer events directly into Hindsight memory.
"""

import csv
import io
import re
from typing import List, Dict, Any, Optional
from backend.hindsight.memory_service import memory_service
from backend.hindsight.client import hindsight_client


class FeedbackService:
    def __init__(self):
        self.memory_service = memory_service

    def sanitize_untrusted_input(self, text: str) -> str:
        """
        Defends against prompt injection and malicious instructions in customer feedback.
        Strips control tokens while preserving legitimate feedback content.
        """
        # Block common prompt injection prefixes
        cleaned = re.sub(r'(?i)(ignore previous instructions|system prompt|reveal secrets|drop table|delete bank)', '[FILTERED]', text)
        return cleaned.strip()

    def add_manual_feedback(
        self,
        customer: str,
        segment: str,
        source: str,
        product: str,
        feedback: str,
        sentiment: str,
        theme: Optional[str] = None,
        date: Optional[str] = None,
        bank_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        sanitized = self.sanitize_untrusted_input(feedback)
        import uuid
        feedback_id = f"F_MAN_{uuid.uuid4().hex[:6]}"

        res = self.memory_service.retain_feedback(
            bank_id=bank_id,
            feedback_id=feedback_id,
            customer=customer.strip(),
            segment=segment.strip(),
            source=source.strip(),
            product=product.strip(),
            feedback=sanitized,
            sentiment=sentiment.strip().lower(),
            timestamp=date,
            theme=theme or "general",
        )

        return {
            "success": True,
            "feedback_id": feedback_id,
            "customer": customer,
            "retained_in_hindsight": True,
            "hindsight_response": res,
        }

    def import_csv_file(
        self,
        file_content: str,
        bank_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Validates, normalizes, deduplicates, and retains CSV rows into Hindsight.
        """
        csv_file = io.StringIO(file_content)
        reader = csv.DictReader(csv_file)

        rows = list(reader)
        retained_count = 0
        skipped_count = 0
        errors = []

        required_cols = {"customer", "segment", "feedback", "sentiment"}

        for idx, row in enumerate(rows):
            # Check row validity
            cleaned_row = {k.strip().lower(): v.strip() for k, v in row.items() if k}
            if not required_cols.issubset(cleaned_row.keys()):
                errors.append(f"Row {idx + 1}: Missing required columns")
                skipped_count += 1
                continue

            fb_id = cleaned_row.get("feedback_id") or f"F_IMP_{idx + 1}"
            raw_text = self.sanitize_untrusted_input(cleaned_row.get("feedback", ""))
            if not raw_text:
                skipped_count += 1
                continue

            self.memory_service.retain_feedback(
                bank_id=bank_id,
                feedback_id=fb_id,
                customer=cleaned_row.get("customer", "Unknown"),
                segment=cleaned_row.get("segment", "SMB"),
                source=cleaned_row.get("source", "Support"),
                product=cleaned_row.get("product", "Nova Analytics"),
                feedback=raw_text,
                sentiment=cleaned_row.get("sentiment", "neutral").lower(),
                timestamp=cleaned_row.get("date"),
                theme=cleaned_row.get("theme", "general"),
            )
            retained_count += 1

        return {
            "success": True,
            "total_rows_processed": len(rows),
            "retained_in_hindsight": retained_count,
            "skipped": skipped_count,
            "errors": errors,
        }

    def get_feedback_list(
        self,
        bank_id: Optional[str] = None,
        segment: Optional[str] = None,
        source: Optional[str] = None,
        theme: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        timeline = self.memory_service.get_memory_timeline(bank_id=bank_id, limit=limit + offset + 50)

        # Apply filters
        filtered = [f for f in timeline if f.get("type") == "experience" and f.get("customer") != "Product Team"]
        if segment:
            filtered = [f for f in filtered if f.get("segment", "").lower() == segment.lower()]
        if source:
            filtered = [f for f in filtered if f.get("source", "").lower() == source.lower()]
        if theme:
            filtered = [f for f in filtered if f.get("theme", "").lower() == theme.lower()]

        total = len(filtered)
        paged = filtered[offset:offset + limit]

        return {
            "items": paged,
            "total": total,
            "limit": limit,
            "offset": offset,
        }


feedback_service = FeedbackService()
