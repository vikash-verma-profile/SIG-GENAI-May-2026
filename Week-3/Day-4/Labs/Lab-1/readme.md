# Lab 1 — Building a Self-Healing Pipeline Framework

Build a small pipeline that detects failures, diagnoses the issue, applies a fix, re-runs the workflow, and sends an alert.

## Prerequisites

- Python 3.11+
- VS Code or Jupyter (optional)

## Setup

```bash
cd Labs/Lab-1
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Folder layout

| Path | Purpose |
|------|---------|
| `logs/pipeline.log` | Sample failure log |
| `workflows/` | Last rerun metadata |
| `alerts/` | Recovery alert text |
| `remediation/` | Last applied fix |
| `app.py` | Main script |

## Steps

1. Open `logs/pipeline.log` and note the schema error.
2. Run `python app.py`.
3. Confirm console output: failure detected, diagnosis, fix applied, recovery verified, alert generated.
4. Inspect `remediation/last_fix.json`, `workflows/last_run.json`, and `alerts/recovery_alert.txt`.

## Expected output

- Failure detected
- Diagnosis completed
- Fix applied
- Recovery verified
- Alert generated

## Exercises

- Add retry logic with backoff before escalation.
- Send alerts to Slack or email.
- Persist incidents under `logs/`.
- Orchestrate the same flow with LangGraph (see Lab 10).
