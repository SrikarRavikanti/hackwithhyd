# REST API Reference

Feedback Memory OS exposes REST endpoints on port 8000. Interactive Swagger documentation is available at `http://localhost:8000/docs`.

---

## 1. Feedback Ingestion
- `POST /api/feedback`: Retain manual customer feedback into Hindsight.
- `POST /api/feedback/import`: Ingest CSV file (validates, normalizes, deduplicates, and retains).
- `GET /api/feedback`: Paginated list of retained memories with segment, source, and theme filters.

---

## 2. Decision Memory
- `POST /api/decisions`: Record a product decision with title, rationale, and expected outcome.
- `GET /api/decisions`: Retrieve all logged product decisions from memory.
- `GET /api/decisions/{id}/evaluate`: Evaluate "Did Our Fix Work?" with before/after complaint counts and sentiment shift.

---

## 3. Memory & Intelligence
- `POST /api/memory/query`: Natural-language "Ask Memory" endpoint (Recall + Reflect).
- `POST /api/memory/recall`: Multi-strategy evidence retrieval with entity badges.
- `POST /api/memory/reflect`: Multi-hop synthesis across historical experiences.
- `GET /api/memory/timeline`: Chronological memory stream.
- `GET /api/memory/graph`: Entity relationship graph (Products, Customers, Decisions, Themes).

---

## 4. Analytics & Insights
- `GET /api/analytics/overview`: SaaS metrics (total feedback, active themes, emerging issues).
- `GET /api/analytics/sentiment`: Monthly sentiment trends with AI contextual explanations.
- `GET /api/insights/what-changed`: 7-point chronological synthesis for a given product & topic.
- `GET /api/themes`: Active emerging and resolved customer themes.
- `GET /api/knowledge-pages`: Dynamic mental models / living knowledge pages.

---

## 5. Demo & Evaluation
- `POST /api/ablation/compare`: Side-by-side Stateless AI vs Hindsight-Powered AI comparison.
- `POST /api/demo/seed`: Seed 535 Nova Analytics experiences and 5 product decisions.
- `POST /api/demo/reset`: Reset memory bank to empty.
- `GET /api/demo/steps`: Fetch 5-step guided learning demo scenario.
