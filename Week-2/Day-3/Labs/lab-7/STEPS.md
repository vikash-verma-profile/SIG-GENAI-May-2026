### Lab 7 — PySpark optimization (broadcast join + filter pushdown + partitioning)

### Prerequisites

- **Python**: 3.10+ recommended
- **Java**: required for Spark locally (`java -version` should work)
- **Dependencies**:

```bash
pip install -r requirements.txt
```

### Dataset

- `data/rides.csv`
- `data/drivers.csv`

### Run — Optimized pipeline

From `Labs/lab-7`:

```powershell
python .\optimized_pipeline.py
```

### Run — Baseline (lab comparison)

```powershell
python .\baseline_pipeline.py
```

### Expected outputs

- Optimized path writes partitioned parquet under `output/partitioned_final/`
- Baseline path writes parquet under `output/baseline/`

### Tests

These tests spin up a **local Spark session** (first run can take ~30–60s on some machines).

From `Labs/lab-7`:

```powershell
python -m pytest .\tests -v
```

### What to compare when experimenting

- Remove **`broadcast(...)`** or remove **`filter(city == "Bangalore")`** and observe runtime differences on larger synthetic data.

### Gen AI / Ollama

Use local LLM for optimization experiments and code review; Spark jobs do not call Ollama here. Helpers + index: **`../genai/README.md`**, **`../README.md`**.
