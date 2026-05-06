# Labs — AI-assisted data pipelines (Week-2 / Day-3)

This folder holds **hands-on labs** from natural-language specs through **Pandas**, **PySpark**, **Prefect**, tests, and optional **Ollama** integration.

## Layout

| Path | Topic |
|------|--------|
| **`genai/`** | Ollama HTTP client, JSON helpers, demo prompts, **runtime `--ai` specs** (labs 1–3) |
| **`lab-1/`** | Healthcare ETL (traditional vs modular Pandas); optional **`pipeline.py --ai`** |
| **`lab-2/`** | Medallion PySpark + Prefect; optional **`main.py --ai`** (watermark JSON) |
| **`lab-3/`** | Retail Pandas workflow; optional **`main.py --ai`** |
| **`lab-4/`** | Banking modular `src/` scaffold |
| **`lab-5/`** | Telecom watermark + CDC (Pandas) |
| **`lab-6/`** | Schema evolution (Pandas + optional Spark union) |
| **`lab-7/`** | PySpark optimization (broadcast, partitions) |
| **`lab-8/`** | Prefect DAG (logistics) |
| **`case-study/`** | End-to-end AgriTech PySpark + Prefect |

Each lab includes **`README.md`** (quick start) and **`STEPS.md`** (detailed run & test steps).

## Gen AI / Ollama

- **Development-time**: use any assistant (including **Ollama** in chat) with prompts from **`STEPS.md`** to draft or refactor code — human review before merge.
- **Runtime (selected labs)**: **`--ai`** or **`USE_OLLAMA_PIPELINE=1`** calls Ollama for **validated JSON parameters only** (no execution of model-generated code). See **`genai/README.md`**.

**Environment variables** (when using runtime AI):

- **`OLLAMA_HOST`** — default `http://127.0.0.1:11434`
- **`OLLAMA_MODEL`** — e.g. `llama3`, `qwen2.5-coder`
- **`PIPELINE_AI_INTENT`** — default intent if you omit `--intent`
- **`USE_OLLAMA_PIPELINE=1`** — enable AI branch without CLI flag (labs 1–3)

## Quick test entrypoints

```powershell
Set-Location Labs\lab-1
python -m pytest .\tests -v
```

```powershell
Set-Location Labs\genai
python -m pytest .\tests -v
```

Use each lab’s **`STEPS.md`** for full pytest paths and Spark/Prefect notes.
