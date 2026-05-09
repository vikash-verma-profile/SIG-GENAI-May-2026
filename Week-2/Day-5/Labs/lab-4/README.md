# Lab 4 — AI-powered log analysis (telecom monitoring)

**Domain:** Telecom monitoring  
**Goal:** Practice using an **LLM** to turn raw logs into **root cause**, **severity**, and **remediation** summaries.

**Architecture (conceptual):** Kafka → Python consumer → Elasticsearch.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `app.log` | Sample production-style errors (consumer lag, broker timeout). |
| `incident_summary.txt` | Example structured write-up after analysis (template you can replace). |

---

## Prerequisites

- Access to **ChatGPT**, **Claude**, or similar.
- Editor for updating your own summary file.

---

## Step-by-step

### 1. Open the sample logs

Read `app.log`. Note repeated themes (lag vs broker connectivity).

### 2. Craft an AI prompt

Example:

> Analyze the following logs. Identify: (1) likely root cause, (2) severity, (3) recommended remediation. Be concise and structured.

### 3. Paste logs into the LLM

Paste the **full** contents of `app.log` under your prompt and submit.

### 4. Compare with expected themes

From the lab narrative, expected angles include:

- **Broker timeout** / unhealthy broker path.
- **Consumer lag** exceeding threshold.

Your model may phrase these differently; focus on whether the reasoning matches operational reality.

### 5. Write your incident summary

Update `incident_summary.txt` (or create your own file) with:

- **RCA** (root cause analysis)
- **Severity**
- **Remediation steps** (restart/scale/network checks as appropriate)

### 6. Optional: iterate

Ask the model for a **runbook-style** checklist or a **customer-facing** vs **internal** version.

---

## Expected results

- A short RCA that mentions **broker** and **lag** tradeoffs.
- Clear severity assignment with justification.
- Actionable remediation (not generic “monitor more” only).

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| Model is vague | Ask for **bullet RCA**, **top 3 hypotheses**, and **what logs would disprove each**. |
| Hallucinated line numbers | Remind the model to quote only from pasted text. |

---

## Learning outcomes

- Using LLMs for **triage acceleration**, not blind trust.
- Structuring **incident communication** from noisy logs.
