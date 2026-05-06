### Lab 2 — Medallion pipeline (Bronze → Silver → Gold) with PySpark

### Prerequisites

- **Python**: 3.10+ recommended
- **Java**: required for Spark locally (`java -version` should work)
- **Dependencies**:

```bash
pip install -r requirements.txt
```

### Project layout

- **Spark pipeline code**: `pipeline/` (`bronze/`, `silver/`, `gold/`, `main.py`)
- **Config**: `pipeline/config/settings.yaml` (includes incremental watermark `last_run_date`)
- **Inputs**: `data/patients.csv`
- **Outputs**: Parquet folders under `output/bronze`, `output/silver`, `output/gold`

### Run (Windows PowerShell)

From `Labs/lab-2`:

```powershell
Set-Location .\pipeline
python .\main.py
```

Optional stage runs:

```powershell
python .\main.py --stage bronze
python .\main.py --stage silver
python .\main.py --stage gold
```

### Optional — AI-enabled runtime (Ollama)

`main.py` can ask **Ollama for a JSON watermark** (`last_run_date` → `YYYY-MM-DD`) merged into the loaded YAML for that run:

```powershell
python .\main.py --ai --intent "Keep incremental visits strictly after 2024-01-01"
```

Env vars: **`USE_OLLAMA_PIPELINE`**, **`PIPELINE_AI_INTENT`**, **`OLLAMA_MODEL`**. Details: **`../genai/README.md`**.

### Prefect orchestration (optional)

Still from `Labs/lab-2/pipeline`:

```powershell
python .\dags\prefect_flow.py
```

Note: Prefect may start a temporary local API server on first run; wait until the flow finishes.

### Tests

From `Labs/lab-2/pipeline`:

```powershell
python -m pytest .\tests -v --basetemp $env:TEMP\pytest-basetemp-lab2
```

What’s included:

- **Fast tests**: config YAML sanity checks
- **Optional integration check** (skipped by default): verifies gold parquet exists **after** you’ve run `python main.py` at least once

Run optional integration tests explicitly:

```powershell
$env:RUN_LAB2_SPARK_INTEGRATION="1"
python -m pytest .\tests -v --basetemp $env:TEMP\pytest-basetemp-lab2
```

### Troubleshooting

- **`JAVA_HOME` / Spark errors**: install JDK 11 or 17 and ensure `java` is on `PATH`
- **`Access is denied` pytest cache warnings**: keep using `--basetemp $env:TEMP\...` as shown above
- **Labs index + Ollama env vars**: **`../README.md`**
