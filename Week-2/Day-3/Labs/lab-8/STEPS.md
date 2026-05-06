### Lab 8 — DAG-style orchestration with Prefect (Logistics)

### Prerequisites

- **Python**: 3.10+ recommended
- **Dependencies**:

```bash
pip install -r requirements.txt
```

### Dataset

- **Input**: `data/shipments.csv`

### Run (Windows PowerShell)

From `Labs/lab-8`:

```powershell
python .\pipeline.py
```

Prefect may start a **temporary local API server** on first run—wait until tasks complete.

### Expected output

- **`output/avg_delivery_by_destination.csv`** (mean `delivery_time` grouped by `destination`)

### Optional Airflow direction

See `airflow_dag_stub.py` for a commented starter DAG outline (requires Apache Airflow installed separately).

### Tests

These tests validate the **pure pandas transforms** used by the Prefect tasks (fast, no Prefect runtime required):

From `Labs/lab-8`:

```powershell
python -m pytest .\tests -v
```

### Gen AI / Ollama

Iterate on Prefect DAG shape with chat + **`STEPS.md`**. Runtime **`--ai`** not in this lab; see **`../genai/README.md`** and **`../README.md`**.
