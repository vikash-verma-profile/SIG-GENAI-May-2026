# Lab 8 — Auto DAG (Logistics, Prefect)

```bash
pip install -r requirements.txt
python pipeline.py
```

Writes `output/avg_delivery_by_destination.csv`. See `airflow_dag_stub.py` for an optional Airflow outline.

## Gen AI / Ollama

Pipeline tasks call pure functions testable without Prefect; use Ollama in chat to iterate on DAG structure. Runtime **`--ai`** not wired here — **`../genai/README.md`**, **`../README.md`**.

## Detailed steps & testing

See **`STEPS.md`** for Prefect runtime expectations and pure-Pandas `pytest` coverage.
