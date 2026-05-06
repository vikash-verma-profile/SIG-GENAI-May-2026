# Case Study — AI-Powered Smart Agriculture Pipeline

End-to-end PySpark medallion flow with watermarking, schema evolution (`unionByName` / `mergeSchema`), broadcast enrichment, Prefect orchestration, and alert logic.

## Setup

From `Labs/case-study`:

```bash
pip install -r requirements.txt
```

## Run PySpark pipeline

```bash
cd pipeline
python main.py
```

Artifacts land under `output/` (bronze/silver/gold parquet plus `watermark.txt`).

## Prefect

```bash
cd pipeline
python prefect_flow.py
```

## Tests

```bash
pytest tests -v
```

## Gen AI / Ollama

- **Authoring**: prompt against **`STEPS.md`** / sample data in chat (Ollama) for refactors and design notes.
- **Runtime**: Spark pipeline does **not** call Ollama per batch (by design). To experiment with **JSON-driven thresholds or configs**, reuse patterns in **`../genai/dynamic_spec.py`** + **`ollama_client.py`** (see **`../genai/README.md`**).
- **Labs index**: **`../README.md`**

## Detailed steps & testing

See **`STEPS.md`** for end-to-end commands (including recommended `--basetemp` on Windows) and what each output folder contains.
