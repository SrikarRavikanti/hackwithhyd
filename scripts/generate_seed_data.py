"""
Seed Data Generator for Nova Analytics
Produces 520+ rich, narrative-driven customer feedback events, 5 product decisions,
and 32 customer profiles across 12 months (Oct 2025 - Sep 2026).
"""

import csv
import json
import random
import os
from datetime import datetime, timedelta

os.makedirs("data", exist_ok=True)

CUSTOMERS = [
    # Enterprise ($100k+ ARR)
    {"name": "Acme Corp", "segment": "Enterprise", "tier": "Strategic", "users": 1200},
    {"name": "Globex International", "segment": "Enterprise", "tier": "Strategic", "users": 3500},
    {"name": "Initech Systems", "segment": "Enterprise", "tier": "Enterprise", "users": 850},
    {"name": "Massive Dynamic", "segment": "Enterprise", "tier": "Enterprise", "users": 2100},
    {"name": "Umbrella Corp", "segment": "Enterprise", "tier": "Enterprise", "users": 4500},
    {"name": "Hooli Enterprise", "segment": "Enterprise", "tier": "Strategic", "users": 6000},
    {"name": "Stark Industries", "segment": "Enterprise", "tier": "Strategic", "users": 1800},
    {"name": "Wayne Enterprises", "segment": "Enterprise", "tier": "Strategic", "users": 2900},

    # Mid-Market ($25k - $100k ARR)
    {"name": "Cyberdyne Systems", "segment": "Mid-market", "tier": "Growth", "users": 400},
    {"name": "Soylent Corp", "segment": "Mid-market", "tier": "Growth", "users": 320},
    {"name": "Oscorp Tech", "segment": "Mid-market", "tier": "Growth", "users": 280},
    {"name": "Tyrell Corporation", "segment": "Mid-market", "tier": "Growth", "users": 450},
    {"name": "Aperture Science", "segment": "Mid-market", "tier": "Growth", "users": 520},
    {"name": "Black Mesa Research", "segment": "Mid-market", "tier": "Growth", "users": 610},
    {"name": "Wonka Industries", "segment": "Mid-market", "tier": "Growth", "users": 380},
    {"name": "Dunder Mifflin", "segment": "Mid-market", "tier": "Growth", "users": 210},

    # SMB ($5k - $25k ARR)
    {"name": "Pied Piper", "segment": "SMB", "tier": "Core", "users": 75},
    {"name": "Vandelay Industries", "segment": "SMB", "tier": "Core", "users": 45},
    {"name": "Sterling Cooper", "segment": "SMB", "tier": "Core", "users": 90},
    {"name": "Monsters Inc", "segment": "SMB", "tier": "Core", "users": 110},
    {"name": "Bluth Company", "segment": "SMB", "tier": "Core", "users": 35},
    {"name": "Prestige Worldwide", "segment": "SMB", "tier": "Core", "users": 28},
    {"name": "Gekko & Co", "segment": "SMB", "tier": "Core", "users": 85},
    {"name": "Strickland Propane", "segment": "SMB", "tier": "Core", "users": 40},

    # Startup (<$5k ARR / Beta)
    {"name": "Aviato", "segment": "Startup", "tier": "Starter", "users": 12},
    {"name": "Raviga Capital", "segment": "Startup", "tier": "Starter", "users": 18},
    {"name": "Bachmanity", "segment": "Startup", "tier": "Starter", "users": 8},
    {"name": "SeeFood AI", "segment": "Startup", "tier": "Starter", "users": 15},
    {"name": "Endive Logic", "segment": "Startup", "tier": "Starter", "users": 22},
    {"name": "Nucleus App", "segment": "Startup", "tier": "Starter", "users": 14},
    {"name": "Pied Piper Cloud", "segment": "Startup", "tier": "Starter", "users": 30},
    {"name": "Kramerica Labs", "segment": "Startup", "tier": "Starter", "users": 9},
]

SOURCES = ["Support", "Customer Interview", "Sales Call", "App Review", "Survey"]
PRODUCTS = ["Nova Analytics", "Nova API", "Nova Connect"]

DECISIONS = [
    {
        "id": "DEC-2026-01",
        "title": "Launch Guided Onboarding V1",
        "date": "2026-03-15",
        "owner": "Sarah Lin (VP Product)",
        "reason": "Address high friction in initial setup navigation identified in Q1 feedback.",
        "expected_outcome": "Reduce onboarding drop-off by 40% and improve SMB setup CSAT.",
        "status": "completed",
        "tags": ["theme:onboarding", "type:decision"]
    },
    {
        "id": "DEC-2026-02",
        "title": "API Setup Wizard & Credential Automation",
        "date": "2026-06-01",
        "owner": "Marcus Chen (Head of Core Platform)",
        "reason": "Resolve persistent API key provisioning friction reported by Enterprise accounts.",
        "expected_outcome": "Decrease developer onboarding support tickets by 50%.",
        "status": "completed",
        "tags": ["theme:api", "theme:onboarding", "type:decision"]
    },
    {
        "id": "DEC-2026-03",
        "title": "Query Engine Performance Overhaul",
        "date": "2026-04-20",
        "owner": "Elena Rostova (Principal Architect)",
        "reason": "Resolve dashboard query timeouts for datasets exceeding 10M rows.",
        "expected_outcome": "Sub-500ms p95 query latency across all analytics widgets.",
        "status": "completed",
        "tags": ["theme:performance", "type:decision"]
    },
    {
        "id": "DEC-2026-04",
        "title": "Predictable Usage Billing & Budget Alerts",
        "date": "2026-05-10",
        "owner": "David Miller (Director of Growth)",
        "reason": "Address mid-market complaints about surprise compute billing overages.",
        "expected_outcome": "Eliminate billing disputes by adding hard spend caps and SMS/Email threshold notifications.",
        "status": "completed",
        "tags": ["theme:pricing", "theme:billing", "type:decision"]
    },
    {
        "id": "DEC-2026-05",
        "title": "Enterprise SSO & Role-Based Access Control V2",
        "date": "2026-08-15",
        "owner": "Marcus Chen (Head of Core Platform)",
        "reason": "Unblock enterprise infosec sign-offs and streamline Okta/SAML provisioning.",
        "expected_outcome": "Zero security compliance escalations during enterprise POCs.",
        "status": "completed",
        "tags": ["theme:security", "theme:onboarding", "type:decision"]
    }
]

# Curated Story Arcs:
# 1. Onboarding Arc (Jan-Sep 2026):
#    - Jan-Feb: Everyone complains "Onboarding is confusing, takes days to configure".
#    - Mar 15: Decision Launch Guided Onboarding.
#    - Apr-May: SMB & Startup say "Guided onboarding is amazing, setup took 15 mins!".
#    - Jun: Enterprise says "Guided UI is fine, but API setup requires 3 engineers. Setup is blocked."
#    - Jun 1: API Setup Wizard launched.
#    - Jul-Sep: SMB praises it. Enterprise says "Wizard is good for basic keys, but advanced API setup, VPC peering & custom webhooks still painful!"
#
# 2. Performance Arc:
#    - Nov 2025 - Mar 2026: Dashboard takes 15+ seconds on big tables.
#    - Apr 2026: Query engine overhauled.
#    - May-Sep 2026: "Dashboards load in milliseconds now! Outstanding speed."
#
# 3. Pricing & Billing Arc:
#    - Jan-Apr 2026: "Unpredictable compute bills! Surprise $400 overage."
#    - May 2026: Budget alerts and caps launched.
#    - Jun-Sep 2026: "Budget alerts saved us from overages. Great change."

STORY_FEEDBACK_TEMPLATES = [
    # Onboarding Phase 1 (Jan - Feb 2026)
    {
        "period": ("2026-01-01", "2026-02-28"),
        "theme": "onboarding",
        "templates": [
            ("The onboarding process is confusing and our team spent 3 days trying to figure out initial project configuration.", "negative"),
            ("Dashboard setup is difficult to understand. Documentation lacks a clean step-by-step tutorial.", "negative"),
            ("We had to schedule two support calls just to get our first dashboard running.", "negative"),
            ("Getting started was confusing. There is no walkthrough when you first log in.", "negative"),
            ("Initial onboarding navigation feels clunky. Lost 4 hours trying to find data connectors.", "negative"),
        ]
    },
    # Onboarding Phase 2 (Apr - May 2026) - SMB Success
    {
        "period": ("2026-03-20", "2026-05-30"),
        "theme": "onboarding",
        "segments": ["SMB", "Startup"],
        "templates": [
            ("The new Guided Onboarding is fantastic! Got our startup fully onboarded in under 15 minutes.", "positive"),
            ("Love the new onboarding wizard. Clean, fast, and intuitive setup flow.", "positive"),
            ("Huge improvement over last month. The step-by-step checklist made setup a breeze.", "positive"),
            ("Onboarding was so smooth our non-technical marketer setup their first funnel without engineering help.", "positive"),
        ]
    },
    # Onboarding Phase 3 (Jun - Sep 2026) - Enterprise API Friction
    {
        "period": ("2026-06-05", "2026-09-28"),
        "theme": "onboarding",
        "segments": ["Enterprise"],
        "templates": [
            ("The UI wizard is fine for basic teams, but advanced API configuration still requires 3 engineering days.", "negative"),
            ("Enterprise onboarding remains painful. Setting up API webhooks and VPC peering is completely undocumented.", "negative"),
            ("Our developers are stuck on API key role provisioning during onboarding. Wizard doesn't support custom IAM.", "negative"),
            ("Enterprise setup takes too long. Wizard helps with UI, but we are stuck on backend API integration.", "negative"),
            ("API onboarding friction is delaying our company-wide rollout by another 3 weeks.", "negative"),
            ("We still need hands-on technical architecture support to complete the enterprise API integration.", "negative"),
        ]
    },
    # Performance Pre-Fix (Oct 2025 - Mar 2026)
    {
        "period": ("2025-10-01", "2026-03-31"),
        "theme": "performance",
        "templates": [
            ("Dashboards take over 12 seconds to load when querying our Q4 historical data.", "negative"),
            ("Frequent query timeouts when filtering more than 500,000 events.", "negative"),
            ("Performance is sluggish during peak hours. Analytics widgets spin forever.", "negative"),
        ]
    },
    # Performance Post-Fix (May 2026 - Sep 2026)
    {
        "period": ("2026-05-01", "2026-09-28"),
        "theme": "performance",
        "templates": [
            ("The query engine performance update is incredible. Dashboards render almost instantly now.", "positive"),
            ("Sub-second queries across 15M records! Night and day difference compared to Q1.", "positive"),
            ("Performance is lightning fast now. Kudos to the engineering team.", "positive"),
        ]
    },
    # Pricing & Billing (Nov 2025 - Sep 2026)
    {
        "period": ("2025-11-01", "2026-04-30"),
        "theme": "pricing",
        "templates": [
            ("Surprise $450 compute overage bill this month. We need predictable spend limits.", "negative"),
            ("Usage-based billing is hard to predict for our finance team. Please offer fixed monthly caps.", "negative"),
        ]
    },
    {
        "period": ("2026-05-20", "2026-09-28"),
        "theme": "pricing",
        "templates": [
            ("The new budget threshold alerts and spend caps are exactly what our finance team wanted.", "positive"),
            ("Predictable billing caps prevent surprise charges. Much more trustworthy pricing model now.", "positive"),
        ]
    },
    # General themes: UX, Documentation, Integrations, Mobile App
    {
        "period": ("2025-10-01", "2026-09-28"),
        "theme": "ux",
        "templates": [
            ("The dark mode interface is gorgeous and easy on the eyes during late night query sessions.", "positive"),
            ("Cohort builder filter dropdowns feel slightly cluttered on 13-inch laptop screens.", "negative"),
            ("Keyboard shortcuts for fast SQL editing are super productive!", "positive"),
        ]
    },
    {
        "period": ("2025-10-01", "2026-09-28"),
        "theme": "integrations",
        "templates": [
            ("Snowflake and BigQuery sync integrations work reliably without data loss.", "positive"),
            ("Would love a native HubSpot connector to pull closed-won CRM attribution.", "neutral"),
            ("Slack webhook alerts for anomaly detection alert us within seconds of metric drops.", "positive"),
        ]
    },
    {
        "period": ("2025-10-01", "2026-09-28"),
        "theme": "mobile",
        "templates": [
            ("Mobile browser dashboard layout doesn't render chart legends properly.", "negative"),
            ("iOS web app is responsive enough for quick revenue metric checks on the go.", "neutral"),
        ]
    }
]

def generate_dataset():
    random.seed(42)
    records = []
    feedback_idx = 1000

    # 1. Generate story-specific narrative feedback events (approx 350 rows)
    for story in STORY_FEEDBACK_TEMPLATES:
        start_d = datetime.fromisoformat(story["period"][0])
        end_d = datetime.fromisoformat(story["period"][1])
        days_range = (end_d - start_d).days

        # Allowed segments
        allowed_segs = story.get("segments")
        target_custs = [c for c in CUSTOMERS if not allowed_segs or c["segment"] in allowed_segs]

        num_events = 35 if story["theme"] in ["onboarding", "performance"] else 20
        for _ in range(num_events):
            feedback_idx += 1
            cust = random.choice(target_custs)
            template, sentiment = random.choice(story["templates"])
            date = start_d + timedelta(days=random.randint(0, days_range))
            source = random.choice(SOURCES)
            product = "Nova API" if "API" in template else "Nova Analytics"

            records.append({
                "feedback_id": f"F{feedback_idx}",
                "date": date.strftime("%Y-%m-%d"),
                "source": source,
                "customer": cust["name"],
                "segment": cust["segment"],
                "product": product,
                "feedback": template,
                "sentiment": sentiment,
                "theme": story["theme"]
            })

    # 2. Generate contextual background feedback across all customers to reach 530+ rows
    all_themes = ["reliability", "documentation", "export", "support", "billing", "security", "collaboration"]
    background_templates = {
        "reliability": [
            ("Uptime has been 99.99% for the last 6 months. Very dependable platform.", "positive"),
            ("Minor 5-minute blip during Tuesday 2am maintenance window.", "neutral"),
            ("API response times are consistently solid under 80ms.", "positive")
        ],
        "documentation": [
            ("API reference docs have clear curl examples, but Python SDK samples need updating.", "neutral"),
            ("Webhook documentation helped us deploy custom alerting in an afternoon.", "positive"),
            ("Need more advanced code examples for batch ingestion endpoints.", "negative")
        ],
        "export": [
            ("CSV and Parquet export feature exports 500k rows in under 10 seconds.", "positive"),
            ("Scheduled PDF reports via email look clean and executive-ready.", "positive"),
            ("Would like automated exports directly to S3 buckets.", "neutral")
        ],
        "support": [
            ("Support team answered my ticket in 8 minutes with the exact SQL syntax needed.", "positive"),
            ("Chat support was helpful, although resolution took an extra escalation.", "neutral"),
        ],
        "security": [
            ("SOC2 Type II report and audit logs satisfied our security review quickly.", "positive"),
            ("Role-based permissions allow us to cleanly restrict PII access by department.", "positive"),
        ],
        "collaboration": [
            ("Shared dashboard links with view-only permissions make cross-team sharing easy.", "positive"),
            ("Commenting on chart annotations has streamlined our monthly business reviews.", "positive"),
        ],
        "billing": [
            ("Invoice PDF download is easy to retrieve from the billing portal.", "positive"),
            ("Need option to split invoices across multiple departmental cost centers.", "neutral")
        ]
    }

    start_date = datetime(2025, 10, 1)
    end_date = datetime(2026, 9, 28)
    total_days = (end_date - start_date).days

    while len(records) < 535:
        feedback_idx += 1
        cust = random.choice(CUSTOMERS)
        theme = random.choice(all_themes)
        template, sentiment = random.choice(background_templates[theme])
        date = start_date + timedelta(days=random.randint(0, total_days))
        source = random.choice(SOURCES)
        product = random.choice(PRODUCTS)

        records.append({
            "feedback_id": f"F{feedback_idx}",
            "date": date.strftime("%Y-%m-%d"),
            "source": source,
            "customer": cust["name"],
            "segment": cust["segment"],
            "product": product,
            "feedback": template,
            "sentiment": sentiment,
            "theme": theme
        })

    # Sort records chronologically
    records.sort(key=lambda x: x["date"])

    # Write CSV
    csv_file = "data/nova_analytics_feedback.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "feedback_id", "date", "source", "customer", "segment", "product", "feedback", "sentiment", "theme"
        ])
        writer.writeheader()
        writer.writerows(records)

    # Write Decisions JSON
    with open("data/nova_analytics_decisions.json", "w", encoding="utf-8") as f:
        json.dump(DECISIONS, f, indent=2)

    # Write Customers JSON
    with open("data/nova_analytics_customers.json", "w", encoding="utf-8") as f:
        json.dump(CUSTOMERS, f, indent=2)

    print(f"Generated {len(records)} feedback records in {csv_file}")
    print(f"Generated {len(DECISIONS)} decisions in data/nova_analytics_decisions.json")
    print(f"Generated {len(CUSTOMERS)} customers in data/nova_analytics_customers.json")


if __name__ == "__main__":
    generate_dataset()
