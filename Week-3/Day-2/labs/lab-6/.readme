# Lab 6 — Configurable Threshold Monitoring

Compute null percentages per column and trigger a simple alert when a column crosses a configured threshold.

## Learning outcomes

- Express SLAs as constants (thresholds).
- Compute `null_rate` as a percentage of row count.
- Branch on threshold breach (foundation for Slack or PagerDuty later).

## Prerequisites

- Python 3.11+

## Step 1 — Environment

```bash
cd labs/lab-6
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 — Inspect thresholds

Open `main.py` and note `NULL_THRESHOLD_PERCENT = 5.0`.

## Step 3 — Run the monitor

```bash
python main.py
```

The sample dataframe has two nulls in five rows for `revenue` (40%), which should exceed 5% and print an alert.

## Step 4 — Expected output

- Printed null rate series.
- Alert line when `revenue` crosses the threshold.

## Exercises

1. Add multiple thresholds per column (dictionary config).
2. Add a simple severity score (for example low / medium / high) from how far over threshold you are.
3. Integrate Slack: use a webhook URL from an environment variable and `urllib.request` to POST a JSON payload (do not commit secrets).

## Files

- `main.py` — threshold logic and sample data.
