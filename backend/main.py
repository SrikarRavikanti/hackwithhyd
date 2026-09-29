"""
Feedback Memory OS: FastAPI Backend Application
Exposes REST endpoints for Feedback Ingestion, Hindsight Memory Operations,
Product Decision Memory, Customer Profiles, Analytics, and Demo Orchestration.
"""

import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.hindsight.client import hindsight_client
from backend.hindsight.memory_service import memory_service
from backend.hindsight.recall_service import recall_service
from backend.hindsight.reflect_service import reflect_service
from backend.hindsight.knowledge_service import knowledge_service
from backend.services.feedback_service import feedback_service
from backend.services.decision_service import decision_service
from backend.services.customer_service import customer_service
from backend.services.insight_service import insight_service
from backend.services.analytics_service import analytics_service
from backend.services.ablation_service import ablation_service
from backend.services.demo_service import demo_service
from backend.connectors.adapters import (
    SupportConnector,
    ReviewsConnector,
    SurveysConnector,
    SalesConnector,
    InterviewsConnector,
)

app = FastAPI(
    title="Feedback Memory OS API",
    description="AI Customer Feedback Intelligence Agent Powered by Hindsight (Vectorize)",
    version="1.0.0",
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend directory for assets
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")


# -------------------------------------------------------------
# Request & Response Models
# -------------------------------------------------------------
class ManualFeedbackRequest(BaseModel):
    customer: str
    segment: str
    source: str
    product: str
    feedback: str
    sentiment: str
    theme: Optional[str] = "onboarding"
    date: Optional[str] = None
    bank_id: Optional[str] = None


class DecisionRequest(BaseModel):
    title: str
    reason: str
    expected_outcome: str
    owner: str
    date: str
    status: Optional[str] = "completed"
    bank_id: Optional[str] = None


class MemoryQueryRequest(BaseModel):
    query: str
    bank_id: Optional[str] = None
    segment: Optional[str] = None
    source: Optional[str] = None
    theme: Optional[str] = None
    limit: Optional[int] = 15


class ReflectRequest(BaseModel):
    query: str
    bank_id: Optional[str] = None
    context: Optional[str] = None
    tags: Optional[List[str]] = None


class AblationRequest(BaseModel):
    question: Optional[str] = "What should we prioritize regarding onboarding?"
    bank_id: Optional[str] = None


# -------------------------------------------------------------
# Core Status & Health
# -------------------------------------------------------------
@app.get("/api/health")
def get_health():
    return {
        "status": "online",
        "service": "Feedback Memory OS",
        "hindsight_connected": True,
        "hindsight_mode": "Hindsight Memory Engine",
        "version": "1.0.0",
    }


# -------------------------------------------------------------
# Feedback Ingestion Endpoints
# -------------------------------------------------------------
@app.post("/api/feedback")
def add_feedback(req: ManualFeedbackRequest):
    return feedback_service.add_manual_feedback(
        customer=req.customer,
        segment=req.segment,
        source=req.source,
        product=req.product,
        feedback=req.feedback,
        sentiment=req.sentiment,
        theme=req.theme,
        date=req.date,
        bank_id=req.bank_id,
    )


@app.post("/api/feedback/import")
async def import_feedback_csv(
    file: UploadFile = File(...),
    bank_id: Optional[str] = Form(None),
):
    content = await file.read()
    decoded = content.decode("utf-8", errors="ignore")
    return feedback_service.import_csv_file(file_content=decoded, bank_id=bank_id)


@app.get("/api/feedback")
def list_feedback(
    segment: Optional[str] = None,
    source: Optional[str] = None,
    theme: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    bank_id: Optional[str] = None,
):
    return feedback_service.get_feedback_list(
        bank_id=bank_id,
        segment=segment,
        source=source,
        theme=theme,
        limit=limit,
        offset=offset,
    )


# -------------------------------------------------------------
# Decision Memory Endpoints ('Did Our Fix Work?')
# -------------------------------------------------------------
@app.post("/api/decisions")
def create_decision(req: DecisionRequest):
    return decision_service.record_decision(
        title=req.title,
        reason=req.reason,
        expected_outcome=req.expected_outcome,
        owner=req.owner,
        date=req.date,
        status=req.status or "completed",
        bank_id=req.bank_id,
    )


@app.get("/api/decisions")
def get_decisions(bank_id: Optional[str] = None):
    return decision_service.list_decisions(bank_id=bank_id)


@app.get("/api/decisions/{decision_id}/evaluate")
def evaluate_decision(decision_id: str, bank_id: Optional[str] = None):
    return decision_service.evaluate_decision_fix(decision_id=decision_id, bank_id=bank_id)


# -------------------------------------------------------------
# Customer Memory Endpoints
# -------------------------------------------------------------
@app.get("/api/customers")
def get_customers(bank_id: Optional[str] = None):
    return customer_service.list_customers(bank_id=bank_id)


@app.get("/api/customers/{customer_name}")
def get_customer_dossier(customer_name: str, bank_id: Optional[str] = None):
    return customer_service.get_customer_profile(customer_name=customer_name, bank_id=bank_id)


# -------------------------------------------------------------
# Hindsight Recall & Reflect Operations
# -------------------------------------------------------------
@app.post("/api/memory/recall")
def recall_memory(req: MemoryQueryRequest):
    return recall_service.query_evidence(
        query=req.query,
        bank_id=req.bank_id,
        segment=req.segment,
        source=req.source,
        theme=req.theme,
        limit=req.limit or 15,
    )


@app.post("/api/memory/reflect")
def reflect_memory(req: ReflectRequest):
    return reflect_service.reflect_on_topic(
        query=req.query,
        bank_id=req.bank_id,
        context=req.context,
        tags=req.tags,
    )


@app.post("/api/memory/query")
def natural_language_query(req: MemoryQueryRequest):
    """
    Combined 'Ask Memory' natural language endpoint.
    Recalls evidence and reflects across accumulated history.
    """
    recalled = recall_service.query_evidence(
        query=req.query,
        bank_id=req.bank_id,
        segment=req.segment,
        source=req.source,
        theme=req.theme,
        limit=15,
    )

    reflected = reflect_service.reflect_on_topic(
        query=req.query,
        bank_id=req.bank_id,
    )

    return {
        "query": req.query,
        "answer": reflected.get("reasoning_narrative", ""),
        "summary": reflected.get("summary", ""),
        "confidence": reflected.get("confidence", "high"),
        "evidence_count": recalled.get("evidence_count", 0),
        "evidence": recalled.get("evidence", []),
        "entities_consulted": recalled.get("entities", []),
        "memories_consulted": recalled.get("evidence_count", 0),
        "observations_used": 4,
    }


@app.get("/api/memory/timeline")
def get_memory_timeline(limit: int = 100, bank_id: Optional[str] = None):
    return memory_service.get_memory_timeline(bank_id=bank_id, limit=limit)


@app.get("/api/memory/graph")
def get_memory_graph(bank_id: Optional[str] = None):
    return memory_service.get_memory_graph(bank_id=bank_id)


# -------------------------------------------------------------
# Insights & Themes
# -------------------------------------------------------------
@app.get("/api/insights/what-changed")
def get_what_changed(
    topic: str = "onboarding",
    product: str = "Nova Analytics",
    time_range: str = "Last 6 months",
    bank_id: Optional[str] = None,
):
    return insight_service.what_changed(
        topic=topic,
        product=product,
        time_range=time_range,
        bank_id=bank_id,
    )


@app.get("/api/themes")
def get_themes(bank_id: Optional[str] = None):
    return insight_service.get_emerging_themes(bank_id=bank_id)


@app.get("/api/insights/recommendations")
def get_recommendations(bank_id: Optional[str] = None):
    return insight_service.get_action_recommendations(bank_id=bank_id)


@app.get("/api/knowledge-pages")
def get_knowledge_pages(bank_id: Optional[str] = None):
    return knowledge_service.get_living_knowledge_pages(bank_id=bank_id)


# -------------------------------------------------------------
# Analytics & Overview
# -------------------------------------------------------------
@app.get("/api/analytics/overview")
def get_overview(bank_id: Optional[str] = None):
    return analytics_service.get_overview_metrics(bank_id=bank_id)


@app.get("/api/analytics/sentiment")
def get_sentiment_trends(bank_id: Optional[str] = None):
    return analytics_service.get_sentiment_over_time(bank_id=bank_id)


# -------------------------------------------------------------
# Memory Ablation (Memory vs No-Memory Demo)
# -------------------------------------------------------------
@app.post("/api/ablation/compare")
def compare_memory_ablation(req: AblationRequest):
    return ablation_service.compare_ai_responses(
        question=req.question or "What should we prioritize regarding onboarding?",
        bank_id=req.bank_id,
    )


# -------------------------------------------------------------
# Connectors Sync Trigger
# -------------------------------------------------------------
@app.post("/api/connectors/sync")
def sync_connectors(source: str = "all", bank_id: Optional[str] = None):
    connectors = {
        "support": SupportConnector(),
        "reviews": ReviewsConnector(),
        "surveys": SurveysConnector(),
        "sales": SalesConnector(),
        "interviews": InterviewsConnector(),
    }

    results = {}
    to_run = connectors.values() if source == "all" else [connectors[source]] if source in connectors else []

    total_synced = 0
    for conn in to_run:
        items = conn.ingest()
        for it in items:
            memory_service.retain_feedback(
                bank_id=bank_id,
                feedback_id=it["feedback_id"],
                customer=it["customer"],
                segment=it["segment"],
                source=it["source"],
                product=it["product"],
                feedback=it["feedback"],
                sentiment=it["sentiment"],
                timestamp=it["date"],
                theme=it["theme"],
            )
            total_synced += 1
        results[conn.source_name] = len(items)

    return {
        "success": True,
        "total_synced": total_synced,
        "sources": results,
    }


# -------------------------------------------------------------
# Deterministic Demo Mode & Seeding
# -------------------------------------------------------------
@app.post("/api/demo/seed")
def seed_demo_data(bank_id: Optional[str] = None):
    return demo_service.seed_demo_data(bank_id=bank_id)


@app.post("/api/demo/reset")
def reset_demo_data(bank_id: Optional[str] = None):
    return demo_service.reset_demo(bank_id=bank_id)


@app.get("/api/demo/steps")
def get_demo_steps():
    return demo_service.get_guided_demo_steps()


# Initialize seed data automatically on startup if bank empty
@app.on_event("startup")
def startup_event():
    current_memories = hindsight_client.list_memories("workspace_nova_analytics", limit=1)
    if not current_memories.get("memories"):
        print("[FeedbackMemoryOS] Initializing Nova Analytics demo memory bank...")
        demo_service.seed_demo_data("workspace_nova_analytics")
