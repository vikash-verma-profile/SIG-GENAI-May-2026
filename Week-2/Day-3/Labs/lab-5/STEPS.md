### Lab 5 — Telecom incremental ingestion (watermark + CDC simulation)

### Prerequisites

- **Python**: 3.10+ recommended
- **Dependencies**:

```bash
pip install -r requirements.txt
```

### Dataset

- **Day 1 baseline**: `data/cdr_day1.csv`
- **Day 2 changes**: `data/cdr_day2.csv`

### Run (Windows PowerShell)

From `Labs/lab-5`:

```powershell
python .\pipeline.py
```

### What gets produced

Under `output/`:

- `output/duration_by_user.csv`
- `output/daily_call_count.csv`

State:

- `watermark.txt` stores the latest `last_updated` observed after the run.

### Resetting a demo run

Delete **`watermark.txt`** (and optionally `output/`) if you want to rerun from the default watermark (`2024-01-01`) logic.

### Tests

From `Labs/lab-5`:

```powershell
python -m pytest .\tests -v
```

### Suggested “hands-on” checks

- Validate **CDC**: `call_id=3` should reflect the **updated** duration after merging day1 + incremental day2 rows.

### Gen AI / Ollama

Author prompts against **`STEPS.md`** / datasets in your assistant (Ollama). Runtime **`--ai`** is not wired here — patterns in **`../genai/`**, index **`../README.md`**.
