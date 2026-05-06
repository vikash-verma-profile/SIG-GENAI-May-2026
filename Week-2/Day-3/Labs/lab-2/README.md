# Lab 2 — Medallion Healthcare Pipeline (PySpark)

## Setup

From `Labs/lab-2`:

```bash
pip install -r requirements.txt
```

## Run Spark pipeline

```bash
cd pipeline
python main.py
```

Bronze applies incremental filter `visit_date > last_run_date` (see `pipeline/config/settings.yaml`). Outputs land under `output/bronze`, `output/silver`, `output/gold`.

Optional **Ollama-driven watermark**: from `pipeline`, run `python main.py --ai` (see **`STEPS.md`** / **`../genai/README.md`**).

## Prefect flow

```bash
cd pipeline
python dags/prefect_flow.py
```

## Tests

```bash
cd pipeline
python -m pytest tests -v
```

## Detailed steps & testing

See **`STEPS.md`** (repo root of this lab) for PowerShell-oriented commands, `--basetemp` guidance, and optional Spark integration checks.

All labs overview + env vars: **`../README.md`**.
