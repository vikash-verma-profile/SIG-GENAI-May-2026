# Lab 8 — AI-generated KPI dashboard from metadata (retail analytics)

**Domain:** Retail analytics  
**Goal:** Drive **dashboard design** from structured **metadata** (pipeline name, SLA, success rate) using an LLM as a design assistant.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `metadata.json` | Minimal pipeline metadata example from the lab. |
| `kpi_dashboard_design.txt` | Example KPI themes (SLA, failures, freshness) you can expand with AI. |

---

## Prerequisites

- Any LLM UI (ChatGPT, Claude, etc.).
- Optional: Grafana / Power BI / Looker for implementing tiles later.

---

## Step-by-step

### 1. Read the metadata

Open `metadata.json`. Fields:

- **`pipeline_name`**
- **`sla`** (here: latency/runtime budget in plain language)
- **`success_rate`**

### 2. Prompt the AI for a dashboard spec

Example prompt:

> Generate a KPI dashboard design from the following metadata. Include suggested charts, metrics, thresholds, and who each chart helps (ops vs leadership). Metadata: …

Paste the JSON contents verbatim.

### 3. Compare with the sample themes

Reasonable KPI families include:

- **SLA compliance** — runs within SLA window; failure budget.
- **Failure trends** — error spikes by hour/day; dependency attribution if available.
- **Data freshness** — lag between source and curated tables.

### 4. Map KPIs to data sources

For each proposed KPI, write down **where** the numbers would come from in your stack (orchestrator DB, metrics backend, warehouse freshness queries).

### 5. Optional: implement one chart

Pick the highest-value tile and prototype it in your BI tool using mock numbers first.

---

## Expected results

- A structured dashboard outline (sections, charts, audiences).
- Traceability from **metadata** → **metric definitions** → **data sources**.

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| Generic AI output | Ask for **table of KPI | formula | source system | alert threshold**. |
| SLA ambiguity | Convert SLA string into measurable **SLO** (e.g., job duration < 15 minutes for 99% of runs). |

---

## Learning outcomes

- **Metadata-driven** reporting specs.
- Separating **dashboard beauty** from **metric correctness**.
