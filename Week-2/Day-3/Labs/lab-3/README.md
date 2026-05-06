# Lab 3 — Retail AI Workflow Pipeline

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
cd pipeline
python main.py
```

Writes `output/revenue.csv` and `output/daily_sales.csv`.

## Gen AI / Ollama (optional)

From `pipeline/`: **`python main.py --ai --intent "..."`** — Ollama returns JSON for quantity/price fills and whether to filter non-positive prices. Env: **`USE_OLLAMA_PIPELINE`**, **`PIPELINE_AI_INTENT`**, **`OLLAMA_MODEL`**. See **`../genai/README.md`**.

## Tests

```bash
cd pipeline
python -m pytest test_pipeline.py -v
```

## Detailed steps & testing

See **`STEPS.md`** for the full workflow notes and validation tips.

All labs + Gen AI env vars: **`../README.md`**.
