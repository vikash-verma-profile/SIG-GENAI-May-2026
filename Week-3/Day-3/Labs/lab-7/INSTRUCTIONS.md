# Lab 7 — AI-driven catalogue enrichment

Given a **minimal dataset record** (table name, optional columns), produce **catalogue-ready fields**: human description, suggested **owner**, and **SLA** text.

## Prerequisites

- Python 3.11+
- Optional: `OPENAI_API_KEY`

## Setup

```bash
cd Labs/lab-7
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

### Step 1 — Dataset metadata

`app.py` defines `dataset = {"table": "sales_transactions", ...}` mirroring the course doc.

### Step 2 — Generate description / owner / SLA

Run:

```bash
python app.py
```

Without an API key you get the **template** values (`finance_team`, `Daily refresh`, etc.). With a key, the model returns JSON that the script merges into the same shape.

### Step 3 — Consume enriched JSON

Open `outputs/enriched.json`. In a real system you would **PATCH** your catalog API (DataHub, OpenMetadata, Collibra, etc.).

## Exercises

1. Predict **refresh frequency** from column names like `_dt`, `_snapshot_date`.
2. Summarize **recent query activity** if you join audit logs (sketch the integration).
3. Build a **search document** (title + keywords) for Elasticsearch / OpenSearch.

## Learning outcomes

- Practice **structured enrichment** outputs for metadata stores.
- Keep **fallbacks** for demos without external services.
