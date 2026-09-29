"""
Simulated Connector Adapters for Feedback Memory OS:
- SupportConnector (Zendesk / Intercom)
- ReviewsConnector (G2 / Capterra / App Store)
- SurveysConnector (Typeform / Delighted CSAT)
- SalesConnector (Gong / Salesforce)
- InterviewsConnector (User Research / Dovetail)
"""

import uuid
import datetime
from typing import List, Dict, Any
from .base import BaseConnector


class SupportConnector(BaseConnector):
    def __init__(self):
        super().__init__("Support")

    def fetch(self, limit: int = 5) -> List[Dict[str, Any]]:
        return [
            {
                "ticket_id": f"ZD-{uuid.uuid4().hex[:6]}",
                "requester": "Acme Corp",
                "org_tier": "Enterprise",
                "subject": "API Webhook HMAC verification failing",
                "body": "Our security engineers cannot verify webhook signatures. Documentation is missing the secret key format.",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            },
            {
                "ticket_id": f"ZD-{uuid.uuid4().hex[:6]}",
                "requester": "Pied Piper",
                "org_tier": "SMB",
                "subject": "Guided onboarding question",
                "body": "The guided walkthrough was super helpful. Can we replay the checklist for new teammates?",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        ]

    def normalize(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for r in raw_items:
            sentiment = "positive" if "helpful" in r["body"].lower() else "negative"
            theme = "onboarding" if "onboarding" in r["body"].lower() or "webhook" in r["body"].lower() else "support"
            normalized.append({
                "feedback_id": r["ticket_id"],
                "customer": r["requester"],
                "segment": r["org_tier"],
                "source": "Support",
                "product": "Nova API" if "API" in r["body"] else "Nova Analytics",
                "feedback": f"{r['subject']}: {r['body']}",
                "sentiment": sentiment,
                "theme": theme,
                "date": r["created_at"][:10],
            })
        return normalized


class ReviewsConnector(BaseConnector):
    def __init__(self):
        super().__init__("App Review")

    def fetch(self, limit: int = 5) -> List[Dict[str, Any]]:
        return [
            {
                "review_id": f"G2-{uuid.uuid4().hex[:6]}",
                "author_company": "Initech Systems",
                "company_size": "Enterprise",
                "title": "Powerful BI tool, but enterprise setup has a steep curve",
                "review_text": "Once configured, Nova Analytics handles millions of rows effortlessly. However, initial API and SSO onboarding required 4 days of engineering overhead.",
                "rating": 3.5,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        ]

    def normalize(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{
            "feedback_id": r["review_id"],
            "customer": r["author_company"],
            "segment": r["company_size"],
            "source": "App Review",
            "product": "Nova Analytics",
            "feedback": f"{r['title']} - {r['review_text']}",
            "sentiment": "neutral" if r["rating"] >= 3 else "negative",
            "theme": "onboarding",
            "date": r["timestamp"][:10],
        } for r in raw_items]


class SurveysConnector(BaseConnector):
    def __init__(self):
        super().__init__("Survey")

    def fetch(self, limit: int = 5) -> List[Dict[str, Any]]:
        return [
            {
                "survey_id": f"CSAT-{uuid.uuid4().hex[:6]}",
                "respondent_company": "Aviato",
                "segment": "Startup",
                "score": 10,
                "feedback": "Setup took 10 minutes. The guided tour got our seed-stage team up and running immediately.",
                "submitted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        ]

    def normalize(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{
            "feedback_id": r["survey_id"],
            "customer": r["respondent_company"],
            "segment": r["segment"],
            "source": "Survey",
            "product": "Nova Analytics",
            "feedback": r["feedback"],
            "sentiment": "positive",
            "theme": "onboarding",
            "date": r["submitted_at"][:10],
        } for r in raw_items]


class SalesConnector(BaseConnector):
    def __init__(self):
        super().__init__("Sales Call")

    def fetch(self, limit: int = 5) -> List[Dict[str, Any]]:
        return [
            {
                "call_id": f"GONG-{uuid.uuid4().hex[:6]}",
                "prospect": "Globex International",
                "segment": "Enterprise",
                "notes": "VP of Engineering expressed concern over implementation time. Asked whether API onboarding requires custom Terraform or if pre-built templates exist.",
                "date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        ]

    def normalize(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{
            "feedback_id": r["call_id"],
            "customer": r["prospect"],
            "segment": r["segment"],
            "source": "Sales Call",
            "product": "Nova API",
            "feedback": r["notes"],
            "sentiment": "neutral",
            "theme": "onboarding",
            "date": r["date"][:10],
        } for r in raw_items]


class InterviewsConnector(BaseConnector):
    def __init__(self):
        super().__init__("Customer Interview")

    def fetch(self, limit: int = 5) -> List[Dict[str, Any]]:
        return [
            {
                "session_id": f"INT-{uuid.uuid4().hex[:6]}",
                "customer": "Massive Dynamic",
                "segment": "Enterprise",
                "transcript_highlight": "The March Guided Onboarding solved UI orientation for our business analysts, but our platform engineers are still blocked on API VPC peering.",
                "date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        ]

    def normalize(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{
            "feedback_id": r["session_id"],
            "customer": r["customer"],
            "segment": r["segment"],
            "source": "Customer Interview",
            "product": "Nova Analytics",
            "feedback": r["transcript_highlight"],
            "sentiment": "negative",
            "theme": "onboarding",
            "date": r["date"][:10],
        } for r in raw_items]
