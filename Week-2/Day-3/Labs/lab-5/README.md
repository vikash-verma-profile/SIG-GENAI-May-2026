# Lab 5 — Telecom Incremental Ingestion (watermark + CDC)

Run from `Labs/lab-5`:

```bash
pip install -r requirements.txt
python pipeline.py
```

Uses `data/cdr_day1.csv` + `data/cdr_day2.csv`, writes aggregates under `output/` and persists `watermark.txt`.

## Gen AI / Ollama

No runtime **`--ai`** in this lab; use chat + **`STEPS.md`** for exercises. Shared helpers and lab index: **`../genai/README.md`**, **`../README.md`**.

## Detailed steps & testing

See **`STEPS.md`** for incremental/watermark notes and `pytest` samples.
