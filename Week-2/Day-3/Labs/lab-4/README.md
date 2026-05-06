# Lab 4 — Banking Pipeline (NL → scaffold)

## Setup

```bash
pip install -r requirements.txt
```

## Run

From `Labs/lab-4`:

```bash
python banking_pipeline/src/main.py
```

Outputs: `banking_pipeline/output/clean.csv`, `banking_pipeline/output/agg.csv`.

## Tests

```bash
pytest banking_pipeline/tests -v
```

## Gen AI / Ollama

This lab has **no built-in `--ai` runtime hook** yet. Use **Ollama in your IDE/chat** to scaffold modules from **`STEPS.md`**, or extend patterns in **`../genai/`** (`ollama_client.py`, `dynamic_spec.py`). Index: **`../README.md`**.

## Detailed steps & testing

See **`STEPS.md`** for module layout notes and extended pytest guidance.
