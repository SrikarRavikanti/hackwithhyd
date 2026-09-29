/**
 * Feedback Memory OS: Frontend Application Engine
 * Connects to FastAPI backend and controls all dynamic UI,
 * memory graph, architecture benchmark, and continuous learning lifecycle simulator.
 */

const API_BASE = "";

// State
let currentTab = "tab-overview";
let currentBank = "workspace_nova_analytics";

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  initOverview();
  initWhatChanged();
  initDecisions();
  initAskMemory();
  initMemoryExplorer();
  initCustomerDossier();
  initKnowledgePages();
  initAblation();
  initDemoArc();
  initIngestion();
  initInspectorModal();
});

// -------------------------------------------------------------
// Navigation & Tabs
// -------------------------------------------------------------
function initNavigation() {
  document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
      const targetTab = item.getAttribute("data-tab");
      switchTab(targetTab);
    });
  });

  const quickDemoBtn = document.getElementById("btn-quick-demo");
  if (quickDemoBtn) {
    quickDemoBtn.addEventListener("click", () => switchTab("tab-demo"));
  }
}

function switchTab(tabId) {
  currentTab = tabId;

  // Update sidebar active classes
  document.querySelectorAll(".nav-item").forEach(item => {
    if (item.getAttribute("data-tab") === tabId) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });

  // Switch tab visibility
  document.querySelectorAll(".tab-content").forEach(content => {
    if (content.id === tabId) {
      content.classList.add("active");
    } else {
      content.classList.remove("active");
    }
  });

  // Update header title
  const titles = {
    "tab-overview": "Overview Dashboard",
    "tab-what-changed": "\"What Changed?\" Historical Synthesizer",
    "tab-decisions": "Decision Memory & Closed-Loop Outcomes",
    "tab-ask-memory": "Ask Customer Memory (Hindsight Agent)",
    "tab-memory-explorer": "Memory Explorer & Entity Graph",
    "tab-customers": "Customer Memory Dossiers",
    "tab-knowledge-pages": "Hindsight Mental Models & Living Knowledge",
    "tab-ablation": "Architecture Benchmark: Stateless Baseline vs Continuous Memory OS",
    "tab-demo": "Continuous Learning Lifecycle Simulator",
    "tab-ingestion": "Feedback Ingestion Hub (CSV & Connectors)",
  };
  const heading = document.getElementById("page-heading");
  if (heading && titles[tabId]) {
    heading.textContent = titles[tabId];
  }

  // Trigger specialized loads
  if (tabId === "tab-memory-explorer") {
    loadMemoryExplorer();
    renderMemoryGraph();
  } else if (tabId === "tab-customers") {
    loadCustomerDossier("Acme Corp");
  } else if (tabId === "tab-knowledge-pages") {
    loadKnowledgePages();
  }
}

// -------------------------------------------------------------
// Overview Dashboard
// -------------------------------------------------------------
async function initOverview() {
  try {
    const res = await fetch(`${API_BASE}/api/analytics/overview`);
    const data = await res.json();

    document.getElementById("stat-total-feedback").textContent = data.total_feedback || 535;
    document.getElementById("stat-active-themes").textContent = data.active_themes || 10;
    document.getElementById("stat-emerging-issues").textContent = data.emerging_issues || 3;
    document.getElementById("stat-resolved-issues").textContent = data.resolved_issues || 4;
    document.getElementById("stat-memory-growth").textContent = data.memory_growth || "+214";

    loadEmergingThemes();
    loadSentimentTimeline();
    loadRecentMemories();
  } catch (err) {
    console.error("Failed to load overview analytics:", err);
  }
}

async function loadEmergingThemes() {
  const container = document.getElementById("themes-list-container");
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/api/themes`);
    const themes = await res.json();

    container.innerHTML = themes.map(t => `
      <div class="insight-card">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <span class="insight-badge ${t.severity === 'high' ? 'badge-emerging' : 'badge-resolved'}">
            ${t.status}: ${t.trend}
          </span>
          <span style="font-size: 11px; color: var(--text-muted); font-family: monospace;">${t.affected_segment}</span>
        </div>
        <h4 style="font-size: 14.5px; font-weight: 700; margin: 4px 0 6px;">${t.title}</h4>
        <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">${t.current_unresolved_issue}</p>
        <div style="font-size: 11px; color: var(--text-muted); margin-top: 8px;">
          First detected: ${t.first_detected} | Last observed: ${t.last_observed}
        </div>
      </div>
    `).join("");
  } catch (err) {
    container.innerHTML = `<div style="color: var(--text-muted); font-size: 13px;">Themes loading...</div>`;
  }
}

async function loadSentimentTimeline() {
  const container = document.getElementById("sentiment-timeline-container");
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/api/analytics/sentiment`);
    const months = await res.json();

    container.innerHTML = months.map(m => `
      <div class="timeline-item">
        <div class="timeline-dot ${m.positive > 60 ? '' : 'decision'}"></div>
        <div class="timeline-date">${m.month} — Pos: ${m.positive}% | Neg: ${m.negative}%</div>
        <div class="timeline-text" style="font-size: 13px;">${m.explanation}</div>
      </div>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}

async function loadRecentMemories() {
  const tbody = document.getElementById("recent-memories-tbody");
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/api/feedback?limit=6`);
    const data = await res.json();
    const items = data.items || [];

    tbody.innerHTML = items.map(it => `
      <tr>
        <td style="font-family: monospace; font-size: 12px; color: var(--text-muted);">${it.date}</td>
        <td><strong>${it.customer}</strong></td>
        <td><span class="insight-badge badge-enterprise">${it.segment}</span></td>
        <td>${it.source}</td>
        <td style="max-width: 440px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
          "${it.text}"
        </td>
        <td>
          <span style="font-size: 11.5px; font-weight: 600; color: ${it.sentiment === 'positive' ? 'var(--accent-emerald)' : (it.sentiment === 'negative' ? 'var(--accent-rose)' : 'var(--text-muted)')};">
            ${it.sentiment.toUpperCase()}
          </span>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}

// -------------------------------------------------------------
// "What Changed?" Synthesizer
// -------------------------------------------------------------
function initWhatChanged() {
  const runBtn = document.getElementById("btn-run-what-changed");
  if (runBtn) {
    runBtn.addEventListener("click", runWhatChanged);
  }
  // Run automatically on first view
  runWhatChanged();
}

async function runWhatChanged() {
  const topic = document.getElementById("wc-topic-select").value || "onboarding";
  try {
    const res = await fetch(`${API_BASE}/api/insights/what-changed?topic=${topic}`);
    const data = await res.json();

    document.getElementById("wc-current-understanding").textContent = data.current_understanding;
    document.getElementById("wc-confidence-badge").textContent = `${data.confidence} Confidence (${data.evidence_count} Memories)`;
    document.getElementById("wc-evidence-count").textContent = data.evidence_count;

    const stepsContainer = document.getElementById("wc-narrative-steps");
    stepsContainer.innerHTML = data.narrative_points.map((pt, idx) => `
      <div style="display: flex; gap: 12px; align-items: flex-start; padding: 10px 14px; background: rgba(255,255,255,0.02); border-radius: var(--radius-sm); border-left: 3px solid var(--accent-indigo);">
        <span style="font-weight: 800; color: var(--accent-blue); font-size: 13px;">${idx + 1}.</span>
        <span style="font-size: 13.5px; color: var(--text-primary); line-height: 1.5;">${pt}</span>
      </div>
    `).join("");

    const grid = document.getElementById("wc-evidence-grid");
    grid.innerHTML = (data.sample_evidence || []).map(ev => `
      <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px;">
        <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); margin-bottom: 6px;">
          <span>${ev.source} &bull; ${ev.date}</span>
          <span style="color: var(--accent-indigo); font-family: monospace;">${ev.segment}</span>
        </div>
        <div style="font-weight: 600; font-size: 13px; margin-bottom: 4px;">${ev.customer}</div>
        <p style="font-size: 12.5px; color: var(--text-secondary); font-style: italic;">"${ev.text}"</p>
      </div>
    `).join("");
  } catch (err) {
    console.error("What changed error:", err);
  }
}

// -------------------------------------------------------------
// Decision Memory
// -------------------------------------------------------------
function initDecisions() {
  const evalBtn = document.getElementById("btn-eval-decision");
  if (evalBtn) {
    evalBtn.addEventListener("click", runDecisionEvaluation);
  }

  const form = document.getElementById("form-add-decision");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        title: document.getElementById("dec-title").value,
        owner: document.getElementById("dec-owner").value,
        reason: document.getElementById("dec-reason").value,
        expected_outcome: document.getElementById("dec-outcome").value,
        date: document.getElementById("dec-date").value,
      };

      try {
        const res = await fetch(`${API_BASE}/api/decisions`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        alert(`Product decision successfully retained in Hindsight memory! Decision ID: ${data.decision_id}`);
        form.reset();
      } catch (err) {
        alert("Failed to save decision.");
      }
    });
  }

  // Pre-load default evaluation
  runDecisionEvaluation();
}

async function runDecisionEvaluation() {
  const decSelect = document.getElementById("decision-eval-select");
  const decId = decSelect ? decSelect.value : "DEC-2026-01";

  try {
    const res = await fetch(`${API_BASE}/api/decisions/${decId}/evaluate`);
    const data = await res.json();

    document.getElementById("eval-decision-title").textContent = data.decision;
    document.getElementById("eval-before-count").textContent = `${data.before_count} Complaints`;
    document.getElementById("eval-before-breakdown").textContent = `${data.before_enterprise} Enterprise | ${data.before_smb} SMB & Startup`;

    document.getElementById("eval-after-count").textContent = `${data.after_count} Complaints`;
    document.getElementById("eval-after-breakdown").textContent = `${data.after_enterprise} Enterprise | ${data.after_smb} SMB & Startup`;

    document.getElementById("eval-outcome-verdict").textContent = data.outcome_verdict;
    document.getElementById("eval-emerging-pattern").textContent = `"${data.emerging_complaint_pattern}"`;
  } catch (err) {
    console.error("Evaluation error:", err);
  }
}

// -------------------------------------------------------------
// Ask Memory Chat Agent
// -------------------------------------------------------------
function initAskMemory() {
  const sendBtn = document.getElementById("btn-send-chat");
  const input = document.getElementById("chat-query-input");

  if (sendBtn && input) {
    sendBtn.addEventListener("click", () => {
      const q = input.value.trim();
      if (q) askQuestion(q);
    });
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        const q = input.value.trim();
        if (q) askQuestion(q);
      }
    });
  }
}

async function askQuestion(query) {
  const input = document.getElementById("chat-query-input");
  if (input) input.value = query;

  const respCard = document.getElementById("chat-response-card");
  const answerText = document.getElementById("chat-answer-text");
  const citationsGrid = document.getElementById("chat-citations-grid");

  respCard.style.display = "block";
  answerText.textContent = "🧠 Consulting Hindsight Memory Bank (Recall + Reflect)...";
  citationsGrid.innerHTML = "";

  try {
    const res = await fetch(`${API_BASE}/api/memory/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query }),
    });
    const data = await res.json();

    answerText.textContent = data.answer || "No historical memory found.";
    document.getElementById("chat-confidence-badge").textContent = `${data.confidence.toUpperCase()} CONFIDENCE`;
    document.getElementById("chat-evidence-count").textContent = data.evidence_count || 0;

    citationsGrid.innerHTML = (data.evidence || []).slice(0, 6).map(ev => `
      <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 10px;">
        <div style="font-size: 11px; color: var(--accent-blue); display: flex; justify-content: space-between;">
          <span>${ev.source} &bull; ${ev.date}</span>
          <span style="font-family: monospace;">${ev.customer}</span>
        </div>
        <p style="font-size: 12px; color: var(--text-secondary); margin-top: 4px; font-style: italic;">"${ev.text}"</p>
      </div>
    `).join("");
  } catch (err) {
    answerText.textContent = "Memory temporarily unavailable. No evidence-backed answer was generated.";
  }
}

// -------------------------------------------------------------
// Memory Explorer & Graph
// -------------------------------------------------------------
function initMemoryExplorer() {
  const seg = document.getElementById("filter-segment");
  const src = document.getElementById("filter-source");
  const srch = document.getElementById("filter-search");

  [seg, src, srch].forEach(el => {
    if (el) el.addEventListener("change", loadMemoryExplorer);
  });
}

async function loadMemoryExplorer() {
  const tbody = document.getElementById("explorer-tbody");
  if (!tbody) return;

  const seg = document.getElementById("filter-segment").value;
  const src = document.getElementById("filter-source").value;

  try {
    const res = await fetch(`${API_BASE}/api/feedback?limit=25&segment=${seg}&source=${src}`);
    const data = await res.json();
    const items = data.items || [];

    tbody.innerHTML = items.map(it => `
      <tr>
        <td style="font-family: monospace; font-size: 11px; color: var(--accent-indigo);">${it.id}</td>
        <td style="font-family: monospace; font-size: 12px;">${it.date}</td>
        <td><strong>${it.customer}</strong></td>
        <td><span class="insight-badge badge-enterprise">${it.segment}</span></td>
        <td>${it.source}</td>
        <td><span class="insight-badge badge-resolved" style="font-size: 10px;">${it.type}</span></td>
        <td style="max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
          "${it.text}"
        </td>
        <td>
          <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 11px;" onclick="inspectMemory('${it.id}', '${encodeURIComponent(it.text)}')">Inspect</button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}

async function renderMemoryGraph() {
  const svg = document.getElementById("memory-graph-svg");
  if (!svg) return;

  try {
    const res = await fetch(`${API_BASE}/api/memory/graph`);
    const graph = await res.json();

    const width = svg.clientWidth || 800;
    const height = 380;
    svg.innerHTML = "";

    // Draw central node
    const centerX = width / 2;
    const centerY = height / 2;

    let svgHtml = "";
    // Draw links
    const nodes = graph.nodes || [];
    const angleStep = (2 * Math.PI) / (nodes.length || 1);

    nodes.forEach((n, i) => {
      if (i === 0) {
        n.x = centerX;
        n.y = centerY;
      } else {
        const angle = i * angleStep;
        const radius = i % 2 === 0 ? 130 : 160;
        n.x = centerX + radius * Math.cos(angle);
        n.y = centerY + radius * Math.sin(angle);
      }
    });

    (graph.links || []).forEach(l => {
      const srcNode = nodes.find(n => n.id === l.source);
      const tgtNode = nodes.find(n => n.id === l.target);
      if (srcNode && tgtNode) {
        svgHtml += `<line x1="${srcNode.x}" y1="${srcNode.y}" x2="${tgtNode.x}" y2="${tgtNode.y}" stroke="rgba(99,102,241,0.25)" stroke-width="1.5" />`;
      }
    });

    nodes.forEach((n, i) => {
      const color = n.type === "product" ? "#6366F1" : (n.type === "decision" ? "#EC4899" : (n.type === "theme" ? "#F59E0B" : "#10B981"));
      const r = n.type === "product" ? 18 : 12;
      svgHtml += `
        <circle cx="${n.x}" cy="${n.y}" r="${r}" fill="${color}" stroke="#fff" stroke-width="1.5" style="filter: drop-shadow(0 0 6px ${color}); cursor: pointer;" />
        <text x="${n.x}" y="${n.y + r + 12}" fill="#F8FAFC" font-size="10.5" font-family="'Plus Jakarta Sans', sans-serif" text-anchor="middle">${n.label.substring(0, 16)}</text>
      `;
    });

    svg.innerHTML = svgHtml;
  } catch (err) {
    console.error("Graph error:", err);
  }
}

// -------------------------------------------------------------
// Customer Dossiers
// -------------------------------------------------------------
function initCustomerDossier() {
  const loadBtn = document.getElementById("btn-load-customer");
  if (loadBtn) {
    loadBtn.addEventListener("click", () => {
      const name = document.getElementById("customer-select").value;
      loadCustomerDossier(name);
    });
  }
}

async function loadCustomerDossier(name) {
  const container = document.getElementById("customer-profile-content");
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/api/customers/${encodeURIComponent(name)}`);
    const c = await res.json();

    container.innerHTML = `
      <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
          <div>
            <h2 style="font-size: 20px; font-weight: 800;">${c.customer}</h2>
            <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">
              Segment: <strong style="color: var(--accent-purple);">${c.segment}</strong> &bull; Customer Since: ${c.customer_since} &bull; Products: ${c.products_used.join(", ")}
            </div>
          </div>
          <span class="insight-badge ${c.current_risk === 'High' ? 'badge-emerging' : 'badge-resolved'}">
            Risk: ${c.current_risk}
          </span>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;">
          <div style="background: rgba(0,0,0,0.2); padding: 16px; border-radius: var(--radius-md);">
            <div style="font-size: 12px; font-weight: 700; color: var(--accent-rose); text-transform: uppercase;">Known Issues (Extracted from Memory)</div>
            <ul style="margin-top: 8px; font-size: 13px; line-height: 1.8; list-style-position: inside;">
              ${c.known_issues.map(iss => `<li>${iss}</li>`).join("")}
            </ul>
          </div>
          <div style="background: rgba(0,0,0,0.2); padding: 16px; border-radius: var(--radius-md);">
            <div style="font-size: 12px; font-weight: 700; color: var(--accent-indigo); text-transform: uppercase;">Product Interventions Received</div>
            <ul style="margin-top: 8px; font-size: 13px; line-height: 1.8; list-style-position: inside;">
              ${c.product_interventions_received.map(int => `<li><strong>${int.title}</strong> (${int.date})</li>`).join("")}
            </ul>
          </div>
        </div>

        <h4 style="font-size: 13px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 12px;">Customer Interaction Memory Timeline (${c.timeline.length} Events)</h4>
        <div class="timeline">
          ${c.timeline.map(it => `
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-date">${it.date ? it.date.substring(0, 10) : ''} &bull; Channel: ${it.source}</div>
              <div class="timeline-text">"${it.text}"</div>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  } catch (err) {
    container.innerHTML = `<div style="color: var(--accent-rose);">Failed to load customer dossier.</div>`;
  }
}

// -------------------------------------------------------------
// Mental Models & Living Knowledge Pages
// -------------------------------------------------------------
async function initKnowledgePages() {
  // Handled on tab switch
}

async function loadKnowledgePages() {
  const container = document.getElementById("knowledge-pages-container");
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/api/knowledge-pages`);
    const pages = await res.json();

    container.innerHTML = pages.map(p => `
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
          <div>
            <span class="insight-badge badge-enterprise">${p.category}</span>
            <h3 style="font-size: 17px; font-weight: 700; margin-top: 4px;">${p.title}</h3>
          </div>
          <div style="text-align: right;">
            <span style="font-size: 11px; color: var(--accent-emerald);">● Refreshed Live</span>
            <div style="font-size: 11px; color: var(--text-muted);">${p.confidence}</div>
          </div>
        </div>
        <p style="font-size: 13.5px; color: var(--text-secondary); margin-bottom: 16px;">${p.summary}</p>
        <div style="background: rgba(0,0,0,0.3); padding: 16px; border-radius: var(--radius-md); font-size: 13px; line-height: 1.7; white-space: pre-line; border-left: 3px solid var(--accent-indigo);">
          ${p.content}
        </div>
      </div>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}

// -------------------------------------------------------------
// Memory Ablation (Memory vs No-Memory)
// -------------------------------------------------------------
function initAblation() {
  const btn = document.getElementById("btn-run-ablation");
  if (btn) {
    btn.addEventListener("click", runAblation);
  }
}

async function runAblation() {
  const q = document.getElementById("ablation-question").value;
  try {
    const res = await fetch(`${API_BASE}/api/ablation/compare`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q }),
    });
    const data = await res.json();

    document.getElementById("stateless-answer-box").textContent = `"${data.stateless.answer}"`;
    document.getElementById("hindsight-answer-box").textContent = `"${data.hindsight.answer}"`;
  } catch (err) {
    console.error(err);
  }
}

// -------------------------------------------------------------
// Continuous Learning Lifecycle Simulator
// -------------------------------------------------------------
function initDemoArc() {
  const resetBtn = document.getElementById("btn-reset-demo");
  const runBtn = document.getElementById("btn-run-full-demo");

  if (resetBtn) {
    resetBtn.addEventListener("click", async () => {
      if (confirm("Reset workspace memory bank to initial state?")) {
        await fetch(`${API_BASE}/api/demo/reset`, { method: "POST" });
        alert("Workspace memory reset.");
        loadDemoSteps();
      }
    });
  }

  if (runBtn) {
    runBtn.addEventListener("click", async () => {
      await fetch(`${API_BASE}/api/demo/seed`, { method: "POST" });
      loadDemoSteps();
      alert("Workspace memory initialized! Continuous learning progression active.");
    });
  }

  loadDemoSteps();
}

async function loadDemoSteps() {
  const container = document.getElementById("demo-steps-container");
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/api/demo/steps`);
    const steps = await res.json();

    container.innerHTML = steps.map(s => `
      <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span style="font-size: 12px; font-weight: 800; color: var(--accent-indigo); text-transform: uppercase;">
            STEP ${s.step}: ${s.title}
          </span>
          <span class="insight-badge badge-resolved" style="font-size: 11px;">Verified Production State</span>
        </div>
        <div style="font-size: 12.5px; color: var(--accent-blue); margin-bottom: 4px;"><strong>Action:</strong> ${s.action}</div>
        <div style="font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 8px;"><strong>Query:</strong> "${s.question}"</div>
        <div style="background: rgba(0,0,0,0.3); border-radius: var(--radius-md); padding: 12px; font-size: 13.5px; line-height: 1.6; color: #E0E7FF; margin-bottom: 8px;">
          🧠 <strong>Hindsight Agent Answer:</strong> "${s.agent_response}"
        </div>
        <div style="font-size: 11.5px; color: var(--accent-emerald);">
          <strong>Memory Telemetry:</strong> ${s.hindsight_state}
        </div>
      </div>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}

// -------------------------------------------------------------
// Ingestion Hub & Connectors
// -------------------------------------------------------------
function initIngestion() {
  const syncBtn = document.getElementById("btn-sync-connectors");
  if (syncBtn) {
    syncBtn.addEventListener("click", async () => {
      syncBtn.disabled = true;
      syncBtn.textContent = "Syncing...";
      try {
        const res = await fetch(`${API_BASE}/api/connectors/sync`, { method: "POST" });
        const data = await res.json();
        alert(`Successfully synced ${data.total_synced} fresh customer experiences into Hindsight memory!`);
        initOverview();
      } catch (err) {
        alert("Failed to sync connectors.");
      } finally {
        syncBtn.disabled = false;
        syncBtn.textContent = "🔄 Sync Connectors";
      }
    });
  }

  // Manual Feedback form
  const form = document.getElementById("form-manual-feedback");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        customer: document.getElementById("mf-customer").value,
        segment: document.getElementById("mf-segment").value,
        source: document.getElementById("mf-source").value,
        sentiment: document.getElementById("mf-sentiment").value,
        feedback: document.getElementById("mf-feedback").value,
        product: "Nova Analytics",
        date: new Date().toISOString().substring(0, 10),
      };

      try {
        const res = await fetch(`${API_BASE}/api/feedback`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        alert(`Feedback successfully retained in Hindsight memory! Memory ID: ${data.feedback_id}`);
        form.reset();
        initOverview();
      } catch (err) {
        alert("Failed to retain manual feedback.");
      }
    });
  }

  // CSV file input
  const fileInput = document.getElementById("csv-file-input");
  if (fileInput) {
    fileInput.addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append("file", file);

      const statusBox = document.getElementById("csv-upload-status");
      statusBox.style.display = "block";
      statusBox.innerHTML = "<span style='color: var(--accent-indigo);'>Uploading and retaining into Hindsight memory...</span>";

      try {
        const res = await fetch(`${API_BASE}/api/feedback/import`, {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        statusBox.innerHTML = `
          <span style='color: var(--accent-emerald); font-weight: 600;'>
            ✓ Successfully retained ${data.retained_in_hindsight} feedback records into Hindsight memory!
          </span>
        `;
        initOverview();
      } catch (err) {
        statusBox.innerHTML = "<span style='color: var(--accent-rose);'>CSV Ingestion failed.</span>";
      }
    });
  }
}

// -------------------------------------------------------------
// Hindsight Memory Inspector Modal
// -------------------------------------------------------------
function initInspectorModal() {
  const openBtn = document.getElementById("btn-open-inspector");
  const closeBtn = document.getElementById("btn-close-inspector");
  const modal = document.getElementById("inspector-modal");

  if (openBtn && modal) {
    openBtn.addEventListener("click", () => {
      modal.classList.add("active");
      document.getElementById("inspector-sample-memory").textContent = JSON.stringify({
        hindsight_bank: currentBank,
        active_memory_types: ["experience", "world_fact", "observation", "mental_model"],
        retrieval_strategies: ["semantic_vector", "keyword_bm25", "entity_graph", "temporal_reranker"],
        decision_memory_enabled: true,
        tenant_isolation: "hard_boundary",
      }, null, 2);
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => modal.classList.remove("active"));
  }

  window.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.remove("active");
  });
}

function inspectMemory(id, encodedText) {
  const modal = document.getElementById("inspector-modal");
  if (modal) {
    modal.classList.add("active");
    document.getElementById("inspector-sample-memory").textContent = JSON.stringify({
      memory_id: id,
      type: "experience",
      context: "customer_feedback",
      content: decodeURIComponent(encodedText),
      retained_in_bank: currentBank,
      hindsight_indexed: true,
    }, null, 2);
  }
}
