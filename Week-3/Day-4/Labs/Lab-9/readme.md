# Lab 9 — Drift Detection Agent

Compare baseline and current feature distributions, flag drift, and adjust pipeline validation thresholds.

## Setup

```bash
cd Labs/Lab-9
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

1. Review `data/baseline.csv` and `data/current.csv`.
2. Run `python app.py`.
3. Confirm drift detection, KS test, PSI score, and adjustment output.
4. Open `outputs/drift_report.json`.

## Exercises

- Tune mean tolerance and PSI thresholds.
- Trigger automatic retraining when PSI exceeds a limit.
- Monitor multiple features instead of a single column.
