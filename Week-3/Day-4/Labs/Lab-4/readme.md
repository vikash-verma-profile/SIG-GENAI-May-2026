# Lab 4 — AI-Assisted Runbook Lookup

Retrieve remediation steps from a runbook catalog and rank the closest match for a free-text incident description.

## Setup

```bash
cd Labs/Lab-4
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

1. Open `data/runbooks.json`.
2. Run `python app.py`.
3. Confirm direct lookup for Schema Drift and similarity match output.
4. Review `outputs/runbook_recommendation.json`.

## Exercises

- Replace TF-IDF matching with embeddings and a vector store.
- Add incident history retrieval from past tickets.
- Generate step-by-step action plans with an LLM.
