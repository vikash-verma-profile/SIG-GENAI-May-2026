# Lab 1 — Traditional vs AI-Powered Healthcare ETL

## Setup

```bash
pip install -r requirements.txt
```

## Run

- Modular pipeline (recommended): `python pipeline.py` — writes `output/billing.csv` and `output/daily.csv`.
- Traditional baseline: from repo root `Labs/lab-1`, run `python pipeline_traditional.py` (expects `data/patients.csv`).

## Data

Sample patients are in `data/patients.csv`.

## Gen AI / Ollama (optional)

- **Runtime JSON spec** (validated; no generated-code execution):  
  `python pipeline.py --ai --intent "Prefer median for missing age; billing missing must be 0"`  
  Or set **`USE_OLLAMA_PIPELINE=1`** (and optional **`PIPELINE_AI_INTENT`**). Requires **`ollama serve`** and **`OLLAMA_MODEL`**.
- **Chat demo only** (outline / tutoring text): **`../genai/example_lab_prompt.py`**  
- Full reference: **`../genai/README.md`**

## Detailed steps & testing

See **`STEPS.md`** for walkthrough, troubleshooting, and **`pytest`** commands.

All labs + Gen AI env vars: **`../README.md`**.
