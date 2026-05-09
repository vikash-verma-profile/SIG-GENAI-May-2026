# Lab 6 — Azure Monitor incident summarization (insurance claims)

**Domain:** Insurance claims platform  
**Goal:** Combine **Azure Monitor / Log Analytics** queries with an **LLM** to summarize incidents and spot production risk.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `sample_queries.kql` | Example **KQL** filtering higher-severity traces. |
| `incident_prompt_context.txt` | Text you can paste above logs when prompting an LLM. |

---

## Prerequisites

- **Azure subscription** (for hands-on) or instructor-provided workspace.
- Access to **Application Insights** or **Log Analytics** as specified by your course.

---

## Step-by-step

### 1. Create or open a Log Analytics workspace

In **Azure Portal**:

- Search for **Log Analytics workspaces** → create or select one.
- Note the workspace used by your application insights resource (if linked).

### 2. Connect application logs

Enable diagnostics so **traces / logs** flow into **Application Insights** or **Log Analytics**, per your app stack (.NET, Java, Node, Python OpenTelemetry, etc.).

### 3. Run the sample KQL

Open **Logs** in Application Insights or Log Analytics and run the query from `sample_queries.kql`:

- It filters traces with **`SeverityLevel >= 3`** (adjust field names if your schema differs).

Save useful variations (time range, specific `cloud_RoleName`, `operation_Id`).

### 4. Export result snippets for the LLM

Copy a **bounded** time window of interesting rows (avoid dumping secrets or PII).

### 5. Prompt the LLM

Use `incident_prompt_context.txt` as a prefix, then paste:

- Your **KQL** summary intent.
- **Representative log lines** or a **tabular excerpt**.

Ask for:

- Suspected **failure modes** (API, DB, dependency).
- **Customer impact** framing.
- **Next diagnostic steps** in Azure (metrics blades, failures view, dependency map).

### 6. Produce an incident summary

Write a short internal summary: **what broke**, **blast radius**, **mitigations**.

---

## Expected results

- A KQL starting point you can adapt to your schema.
- An LLM-assisted narrative that ties **logs** to **hypotheses** and **verification steps**.

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| `SeverityLevel` missing | Inspect actual column names via a broad `AppTraces \| take 10`. |
| Too much data | Narrow `TimeGenerated` and filter `OperationId` for one failing trace. |

---

## Learning outcomes

- Bridging **KQL** + **LLMs** for faster incident understanding.
- Keeping prompts **safe** (redact secrets, minimize PII).
