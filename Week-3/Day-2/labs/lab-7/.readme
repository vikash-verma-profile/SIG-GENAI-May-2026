# Lab 7 — Auto-Quarantine Workflow

Isolate rows that fail a simple email rule and persist them under `quarantine/` with an audit-style console log.

## Learning outcomes

- Select invalid rows with vectorized string checks (with safe handling of missing values via `astype(str)` in this teaching example).
- Write quarantine extracts to CSV.
- Emit counts for downstream audit logs.

## Prerequisites

- Python 3.11+

## Step 1 — Environment

```bash
cd labs/lab-7
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 — Review input data

See `data/sales.csv`. One row contains `bademail` without `@`.

## Step 3 — Run quarantine

```bash
python main.py
```

## Step 4 — Expected output

- Console preview of quarantined rows.
- Count printed.
- File `quarantine/invalid.csv` created.

## Exercises

1. Add row-level IDs and store them in a separate `quarantine_manifest.json`.
2. If **any** row in a file fails, also write a `FILE_FLAG.txt` marker (file-level quarantine signal).
3. Append remediation events to `remediation_log.csv` when a human fixes rows (stub function that writes a line).

## Files

- `main.py` — validation + CSV write.
- `data/sales.csv` — sample input.
- `quarantine/` — bad rows output.
