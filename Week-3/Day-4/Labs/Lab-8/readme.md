# Lab 8 — AI-Assisted MLOps Monitoring

Train a sample classifier, log accuracy to MLflow, detect performance drops, and trigger a retraining workflow.

## Setup

```bash
cd Labs/Lab-8
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

1. Run `python app.py`.
2. Confirm accuracy logging and whether retraining is required.
3. Open `outputs/mlops_report.json`.
4. Optional: run `mlflow ui --backend-store-uri mlruns` and inspect the run.

## Exercises

- Track precision and recall alongside accuracy.
- Add a simple performance dashboard.
- Persist retraining history across runs.
