# Lab 3 — Root Cause Analysis Agent

Categorize incident logs, estimate confidence, and generate remediation-oriented summaries.

## Setup

```bash
cd Labs/Lab-3
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

1. Read `data/incident.log`.
2. Run `python app.py`.
3. Review per-line issue, confidence, and summary in the console.
4. Inspect `outputs/rca_report.json`.

## Exercises

- Swap template summaries for LLM-generated text.
- Add historical incident lookup from a JSON archive.
- Route low-confidence cases to human review.
