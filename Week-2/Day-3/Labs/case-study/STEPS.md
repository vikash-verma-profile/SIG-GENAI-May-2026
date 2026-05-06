### Case Study — Smart Agriculture pipeline (PySpark medallion + Prefect)

### Prerequisites

- **Python**: 3.10+ recommended
- **Java**: required for Spark locally (`java -version` should work)
- **Dependencies**:

```bash
pip install -r requirements.txt
```

### Dataset

Under `data/`:

- `sensor_day1.csv`
- `sensor_day2.csv` (adds **`humidity`** — schema evolution exercise)
- `fields.csv` (small dimension table joined via **broadcast** in gold)

### Run — Full PySpark pipeline

From `Labs/case-study`:

```powershell
Set-Location .\pipeline
python .\main.py
```

Artifacts are written under `output/`:

- `output/bronze/` (incremental slice landed as parquet)
- `output/silver/` (partitioned by `field_id`)
- `output/gold/alerts/` and `output/gold/field_summary/`
- `output/watermark.txt`

### Run — Prefect orchestration (optional)

Still from `Labs/case-study/pipeline`:

```powershell
python .\prefect_flow.py
```

Note: Prefect may start a temporary local API server on first run.

### Tests

From `Labs/case-study`:

```powershell
python -m pytest .\tests -v --basetemp $env:TEMP\pytest-basetemp-case-study
```

What’s included:

- **Fast tests**: config + alert rule logic (mirrors the Spark `when(...)` ordering)

### Troubleshooting

- **Spark/Java errors**: verify JDK is installed and `java` works in PowerShell.
- **pytest cache permission warnings on Windows**: use `--basetemp $env:TEMP\\...` as shown above.

### Gen AI / Ollama

Authoring: prompt from **`STEPS.md`** / **`data/`** in Ollama. Medallion **`main.py`** does not call LLMs per batch; for experiments with JSON-driven behavior reuse **`../genai/dynamic_spec.py`** patterns. Overview: **`../README.md`**.
