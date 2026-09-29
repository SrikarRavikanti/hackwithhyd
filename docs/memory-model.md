# Memory Model: RAG vs Organizational Memory

## Traditional RAG vs Feedback Memory OS

| Dimension | Traditional Document RAG | Feedback Memory OS (Hindsight) |
| :--- | :--- | :--- |
| **Data Primitive** | Raw documents / chunks | Experiences, World Facts, Observations |
| **Temporal Awareness** | Timeless vectors; no sequence understanding | Continuous time-anchored memory timeline |
| **Contradiction Handling** | Confused by evolving opinions | Traces opinion shifts and explains rationale |
| **Product Decisions** | Blind to causes & interventions | Closed-loop: tracks problem &rarr; decision &rarr; outcome |
| **Segment Intelligence** | Mixes all customer personas | Discovers segment divergences (Enterprise vs SMB) |
| **Reasoning Engine** | Single-turn semantic prompt injection | Multi-hop Hindsight Reflect over consolidated knowledge |

---

## The Closed-Loop Feedback Cycle

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Customer (Acme Corp)
    participant Feedback as Ingestion Hub
    participant Hindsight as Hindsight Bank
    participant ProductTeam as Product Team
    participant Analyst as Feedback Analyst Agent

    Customer->>Feedback: "Onboarding is confusing and takes 3 days"
    Feedback->>Hindsight: retain(experience, tags=[theme:onboarding])
    Hindsight->>Hindsight: Consolidate Observation: "Onboarding navigation friction"
    Analyst->>ProductTeam: Alert: High friction in onboarding navigation
    ProductTeam->>Hindsight: retain(decision: "Launch Guided Onboarding V1")
    Customer->>Feedback: "Guided onboarding works for UI, but API setup still needs 3 devs"
    Feedback->>Hindsight: retain(experience, tags=[segment:enterprise, theme:api])
    ProductTeam->>Analyst: "Did our Guided Onboarding fix work?"
    Analyst->>Hindsight: reflect(before_vs_after, decision="Guided Onboarding")
    Hindsight-->>Analyst: Evaluates sentiment delta & segment split
    Analyst-->>ProductTeam: "Partial success: SMB complaints dropped 73%; Enterprise API friction remains."
```
