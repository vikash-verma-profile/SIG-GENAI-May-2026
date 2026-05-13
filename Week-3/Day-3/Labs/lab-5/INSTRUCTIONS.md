# Lab 5 — PII discovery and classification agent

Detect **personally identifiable** patterns in tabular data using **regex**, then attach a **governance classification** column.

## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`

## Setup

```bash
cd Labs/lab-5
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

### Step 1 — Sample dataset

`app.py` builds a small `pandas.DataFrame` with `email` and `phone` columns, matching the course outline.

### Step 2 — Regex-based detection

- **Email**: pattern `\S+@\S+` (matches typical addresses; tune for your org).
- **Phone**: strict **10 digits** for the lab demo row `9876543210`.

The script prints whether each email value matches.

### Step 3 — Apply classification

Rows with a detected email or valid 10-digit phone get **`Confidential`**; others **`Internal`** (demo policy).

### Step 4 — Column-level signals

`scan_dataframe()` aggregates quick signals per column (extensible for Aadhaar / card-like patterns).

### Step 5 — Output artifact

`outputs/classified.json` stores column signals and a row preview.

## Run

```bash
python app.py
```

## Expected output

- Console: DataFrame, per-email match lines, classified DataFrame.
- File: `outputs/classified.json`.

## Exercises

1. **Aadhaar**: feed values like `1234 5678 9012` and confirm `aadhaar_like` appears in signals.
2. **Credit cards**: add a synthetic PAN and tune `CC_RE`; consider **Luhn** validation.
3. **Masking**: write `email_masked` column showing `u***@gmail.com`.

## Note on the original doc snippet

The course doc escaped backslashes in `r'\\S+@\\S+'`. In Python source you should use **`r'\S+@\S+'`** (single backslashes) for word characters around `@`.
