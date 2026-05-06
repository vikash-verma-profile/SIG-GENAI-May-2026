### Gen AI + Ollama (`Labs/genai`)

### What this folder is for

- **`ollama_client.py`** — `POST /api/chat` to Ollama (stdlib only). Env: **`OLLAMA_HOST`**, **`OLLAMA_MODEL`**.
- **`json_extract.py`** — pull one JSON object from noisy model text (for safe parsing).
- **`dynamic_spec.py`** — prompts + validation for **runtime pipeline parameters** (labs **1, 2, 3** when using **`--ai`**).
- **`example_lab_prompt.py`** — demo chat (Lab-1-style cleaning outline; does not change pipeline files).

Full lab map + env vars: **`../README.md`**.

### Two modes (both are “Gen AI”)

1. **Development-time**: Ollama / any assistant drafts code from **`STEPS.md`** — you review and commit (human-in-the-loop).
2. **Runtime JSON specs** (labs **1–3**): **`--ai`** or **`USE_OLLAMA_PIPELINE=1`** → model returns **JSON only** → Python applies **whitelisted** keys. **No `exec` of generated code.**

### Runtime `--ai` quick reference

| Lab | Entrypoint | Ollama controls (JSON) |
|-----|------------|-------------------------|
| **lab-1** | `pipeline.py` | `age_missing_strategy` (`mean`/`median`), `billing_missing_fill` |
| **lab-3** | `pipeline/main.py` | `quantity_missing_fill`, `price_missing_fill`, `filter_non_positive_price` |
| **lab-2** | `pipeline/main.py` | `last_run_date` (`YYYY-MM-DD`) merged into YAML for that run |

Examples:

```bash
# Lab 1
cd Labs/lab-1
python pipeline.py --ai --intent "Prefer median imputation for age; billing missing must be 0"

# Lab 3
cd Labs/lab-3/pipeline
python main.py --ai --intent "Keep quantity default 1 but do not filter zero-price rows"

# Lab 2 (PySpark)
cd Labs/lab-2/pipeline
python main.py --ai --intent "Include visits after 2024-01-01 only"
```

If Ollama is unreachable or JSON is invalid, rerun **without** `--ai` for deterministic defaults.

### Prerequisites

1. Install & run Ollama: [https://ollama.com](https://ollama.com)
2. Pull a model, e.g. `ollama pull llama3`
3. Default URL `http://127.0.0.1:11434`

### Demo chat (no pipeline side effects)

From `Labs/genai`:

```bash
python example_lab_prompt.py
```

### Tests

```bash
python -m pytest tests -v
```

### Extending other labs (4–8, case-study)

Copy the **JSON-spec pattern** from `dynamic_spec.py`: strict prompt → `extract_json_object` → validate keys → merge into config. Do **not** execute arbitrary strings as Python.
