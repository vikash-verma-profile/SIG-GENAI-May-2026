# Lab 6 — Schema Evolution (E-commerce)

## Pandas pipeline

```bash
pip install -r requirements.txt
python pipeline.py
```

Writes `output/final_products.csv`.

## Optional PySpark

```bash
python spark_merge.py
```

Demonstrates **`unionByName(..., allowMissingColumns=True)`** across all CSV snapshots under `data/`.

## Gen AI / Ollama

Use Ollama while authoring changes (prompt against **`STEPS.md`** / CSV headers). Runtime **`--ai`** is not wired here; see **`../genai/README.md`** and **`../README.md`**.

## Detailed steps & testing

See **`STEPS.md`** for schema-evolution exercises and `pytest` samples.
