# Lab 2 — AI-Based Failure Detection using Logs

Detect failures in operational logs, score severity, cluster messages, and produce a root-cause summary.

## Setup

```bash
cd Labs/Lab-2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

1. Review `data/sample_logs.txt`.
2. Run `python app.py`.
3. Confirm ERROR lines are flagged and a summary is printed.
4. Open `outputs/failure_report.json` for failures, severity scores, clusters, and summary.

## Exercises

- Tune clustering (`k`) and compare groupings.
- Add an isolation-forest anomaly detector on TF-IDF features.
- Replace the template summary with an LLM prompt.
