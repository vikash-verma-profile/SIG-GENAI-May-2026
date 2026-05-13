# Lab 4 — Business glossary auto-generation

Generate **short business definitions** for tables using metadata (and optional LLM).

## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`
- Optional: `OPENAI_API_KEY` for live definitions

## Setup

```bash
cd Labs/lab-4
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

### Step 1 — Dataset metadata

The script uses built-in examples starting with `customer_revenue`, matching the course doc. Inspect `app.py` → `tables` list.

### Step 2 — Glossary prompt (in code)

With an API key, `glossary_entry()` sends a structured prompt asking for JSON `term` + `definition`. Without a key, a **template definition** is returned so the pipeline still runs.

### Step 3 — Generate definitions

```bash
python app.py
```

Each table prints a glossary entry; results are appended to **`outputs/glossary.csv`**.

### Step 4 — Exercises direction

- Add approval: write to `glossary_pending.csv` and only promote rows after human review.
- Add more tables from a real catalog export (JSON/CSV input file).

## Expected output

- Console: one dict per table.
- File: `outputs/glossary.csv` with headers `term,definition`.

## Learning outcomes

- Connect **metadata** to **business language**.
- Practice **JSON-only** LLM responses for downstream parsing.
