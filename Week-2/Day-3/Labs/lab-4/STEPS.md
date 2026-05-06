### Lab 4 — Banking scaffold pipeline (modular `src/` package)

### Prerequisites

- **Python**: 3.10+ recommended
- **Dependencies**:

```bash
pip install -r requirements.txt
```

### Dataset

- **Input**: `data/transactions.csv`

### Run (Windows PowerShell)

From `Labs/lab-4`:

```powershell
python .\banking_pipeline\src\main.py
```

### Expected outputs

Writes CSVs under `banking_pipeline/output/`:

- `banking_pipeline/output/clean.csv` (includes `is_fraud`)
- `banking_pipeline/output/agg.csv` (totals per `account_id`)

### Tests

From `Labs/lab-4`:

```powershell
python -m pytest .\banking_pipeline\tests -v
```

### Suggested “hands-on” checks

- **`amount` missing → 0** after cleaning (but fraud flags operate before aggregation semantics vary — inspect outputs).
- **Duplicates**: verify duplicates collapse after cleaning step.

### Gen AI / Ollama

No built-in **`--ai`** runtime hook in this lab. Use chat + this **`STEPS.md`** to scaffold code; shared client/spec helpers live in **`../genai/`**. Labs overview: **`../README.md`**.
