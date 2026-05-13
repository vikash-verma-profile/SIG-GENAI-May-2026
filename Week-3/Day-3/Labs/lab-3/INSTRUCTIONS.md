# Lab 3 — AI-powered metadata tagging

Automatically attach **business** and **sensitivity** style tags to a small metadata record, using an **LLM when configured** or a **deterministic fallback** for classroom use.

## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`

## Optional: OpenAI

Set an API key to use the real model:

```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:OPENAI_MODEL = "gpt-4o-mini"   # optional
```

If `OPENAI_API_KEY` is unset, the script uses **heuristic tags** so everyone can complete the lab offline.

## Setup

```bash
cd Labs/lab-3
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Files

| Path | Purpose |
|------|---------|
| `data/metadata.json` | Table name + columns |
| `outputs/tags.json` | Written tags (created on run) |
| `app.py` | Load metadata → generate tags → save |

## Steps

### Step 1 — Review the metadata dataset

Open `data/metadata.json`. It mirrors the course example: table `customer_transactions` with columns including `customer_id` and `amount`.

### Step 2 — Run the tagger

```bash
python app.py
```

With an API key, the script asks the model for JSON `{"tags": [...]}`. Without a key, you still see tags like **Finance**, **Customer Data**, **Confidential** from rules.

### Step 3 — Inspect stored tags

Open `outputs/tags.json` after the run.

## Expected output

- Console: metadata dict and tag list.
- File: `outputs/tags.json` with `table` and `tags`.

## Exercises

1. **Domain classification**: Add a `domain` field (e.g. retail vs HR) via prompt or rules.
2. **Sensitivity scoring**: Produce numeric scores 1–5 per column.
3. **Governance APIs**: POST the JSON to your internal catalog HTTP endpoint (sketch in code comments first).

## Learning outcomes

- Build a small **metadata classification** pipeline.
- Separate **prompting** from **storage** of results.
- Run the same lab with or without cloud keys.
