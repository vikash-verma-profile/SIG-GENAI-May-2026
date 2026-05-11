# Lab 4 — Expectation Suite Generation

Turn simple profiling statistics into reusable validation checks (Great Expectations).

## Learning outcomes

- Inspect per-column `describe()` output as a profiling step.
- Map numeric min/max to range Expectations for the current batch.
- Run a small “suite” of checks and persist a lightweight JSON summary.

## Prerequisites

- Python 3.11+

## Step 1 — Environment

```bash
cd labs/lab-4
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 — Run the generator

```bash
python main.py
```

The script:

1. Prints `describe()` for each column.
2. Builds Expectations: not-null + unique on `customer_id`, and min/max range on numeric columns derived from the **current** dataframe (tight bounds — useful as a teaching device; in production you would set bounds from training data or SLAs).
3. Validates the batch with GX and writes `expectation_suite_lab4.json` with pass/fail summaries.

## Step 3 — Expected output

- Console profiling tables.
- JSON file listing each Expectation type and `success`.

## Step 4 — Interpret results

All checks should pass on the default sample data. Introduce a bad row in `build_dataframe()` (for example duplicate `customer_id`) to see failures.

## Exercises

1. Load a real CSV and widen numeric bounds using a safety margin (for example ±10%).
2. Add business rules (for example `revenue` must be `< 1_000_000`).
3. Export full GX validation results to HTML or JSON using GX docs (advanced).

## Files

- `main.py` — profiling + dynamic Expectations + GX validation.
- `expectation_suite_lab4.json` — created when you run the script.
