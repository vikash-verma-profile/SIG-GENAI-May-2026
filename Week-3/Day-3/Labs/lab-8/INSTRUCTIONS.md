# Lab 8 — GDPR compliance monitoring agent

Combine **PII detection** (regex / rules) with a **retention policy** check, then emit a small **compliance report** JSON.

## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`

## Setup

```bash
cd Labs/lab-8
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

### Step 1 — Create dataset

`app.py` uses a one-row DataFrame with `customer_email`, matching the course snippet.

### Step 2 — Detect PII

`has_pii()` scans string values for an email-shaped token using the same style of regex as Lab 5.

### Step 3 — Validate retention rules

`retention_days` is the policy (example **365**). `max_record_age_days` simulates the age of the oldest retained row. The lab sets **400** on purpose so you see a **retention alert**.

### Step 4 — Generate compliance output

The script prints and writes `outputs/compliance_report.json` with booleans and human-readable `alerts`.

## Run

```bash
python app.py
```

## Expected output

- `pii_detected: true`
- `retention_ok: false` (because 400 > 365)
- Alerts list explaining both dimensions.

## Exercises

1. **Consent tracking**: extend the DataFrame with `consent_ts` and validate it is present when PII exists.
2. **Deletion workflows**: emit a CSV of primary keys eligible for erasure requests.
3. **Audit reports**: append a run id and SHA-256 hash of input data for traceability.

## Learning outcomes

- Tie **technical signals** (regex) to **policy thresholds** (retention).
- Produce **machine-readable** compliance artifacts for downstream ticketing systems.
