### Lab 3 — Retail workflow pipeline (Spec → Scaffold → Test)

### Prerequisites

- **Python**: 3.10+ recommended
- **Dependencies**:

```bash
pip install -r requirements.txt
```

### Dataset

- **Input**: `data/orders.csv`

### Run (Windows PowerShell)

From `Labs/lab-3`:

```powershell
Set-Location .\pipeline
python .\main.py
```

### Optional — AI-enabled runtime (Ollama)

```powershell
python .\main.py --ai --intent "Default fills stay 1 and 0; do not drop zero-price rows"
```

Same env vars as Lab 1: **`USE_OLLAMA_PIPELINE`**, **`PIPELINE_AI_INTENT`**, **`OLLAMA_MODEL`**.

### Expected outputs

Writes CSV reports under `output/`:

- `output/revenue.csv`
- `output/daily_sales.csv`

### Tests

From `Labs/lab-3/pipeline`:

```powershell
python -m pytest .\test_pipeline.py -v
```

### Suggested “hands-on” checks

- Confirm **`quantity`** nulls become **1** and **`price`** nulls become **0** during cleaning.
- Confirm **`price <= 0` rows are filtered out** (this impacts totals vs raw CSV row counts).

### Documentation

- Labs overview + env vars: **`../README.md`**
- Runtime **`--ai`** details: **`../genai/README.md`**
