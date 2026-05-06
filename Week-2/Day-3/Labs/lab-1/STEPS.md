### Lab 1 — Traditional vs AI-powered Healthcare ETL (Pandas)

### Prerequisites

- **Python**: 3.10+ recommended
- **Dependencies**:

```bash
pip install -r requirements.txt
```

### What this lab demonstrates

- **Traditional baseline**: quick script-style ETL (`pipeline_traditional.py`)
- **Modular “AI-style” pipeline**: functions + docstrings + basic error handling (`pipeline.py`)

### Dataset

- **Input**: `data/patients.csv`

### Run (Windows PowerShell)

From `Labs/lab-1`:

```powershell
python .\pipeline.py
python .\pipeline_traditional.py
```

### Optional — AI-enabled runtime (Ollama)

`pipeline.py` can ask **Ollama for JSON cleaning parameters** (validated; **no generated code execution**):

```powershell
python .\pipeline.py --ai --intent "Use median for missing age; billing missing must be 0"
```

Or set **`USE_OLLAMA_PIPELINE=1`** (and optional **`PIPELINE_AI_INTENT`**). Requires `ollama serve` + a pulled model (`OLLAMA_MODEL`).

### Expected outputs

Both approaches write CSVs under `output/`:

- **`output/billing.csv`**: total billing grouped by `diagnosis`
- **`output/daily.csv`**: daily patient counts (`pipeline.py` names the count column `patient_count`)

### Tests

From `Labs/lab-1`:

```powershell
python -m pytest .\tests -v
```

### Troubleshooting

- **`ModuleNotFoundError: pandas` / `pytest`**: rerun `pip install -r requirements.txt`
- **Labs index / Ollama env vars**: **`../README.md`**
