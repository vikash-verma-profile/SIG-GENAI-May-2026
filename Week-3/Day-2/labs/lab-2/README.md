# Lab 2 — AI-Driven Data Quality Rule Generation

Use Great Expectations (and optionally OpenAI in exercises) to express and run validation rules on tabular data.

## Learning outcomes

- Connect an in-memory pandas DataFrame to GX Core.
- Run individual Expectations and inspect validation results.
- Relate natural-language rules to concrete Expectation objects.

## Prerequisites

- Python 3.11+
- Internet access for `pip install` (first time).

## Step 1 — Environment

```bash
cd labs/lab-2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 — Understand the sample dataset

Open `main.py`. The sample `DataFrame` includes a negative `revenue` so at least one Expectation fails, matching the lab narrative.

## Step 3 — Run validation

```bash
python main.py
```

The script:

1. Builds the GX `DataContext` and a pandas dataframe data source.
2. Creates a whole-dataframe batch definition and passes your `DataFrame` as batch parameters.
3. Validates:
   - `revenue` is between `0` and `+inf` (non-negative).
   - `customer_id` values are unique.

## Step 4 — Expected output

- Printed dataset.
- For each Expectation: `success=True/False` plus result details when available.
- The negative revenue row should cause the `revenue` Expectation to fail.

## Step 5 — Connect to the “AI rules” idea

`EXPECTATION_NOTES` holds plain English. In production you could:

- Use an LLM to propose Expectation JSON from notes (exercise).
- Store approved suites in source control.

## Exercises

1. Add `ExpectColumnValuesToNotBeNull` for `revenue`.
2. Add regex validation on a string column (add a column to the sample data first).
3. Call the OpenAI API to suggest additional Expectations from `EXPECTATION_NOTES`, then map them manually to GX objects (review all suggestions before running in prod).

## Files

- `main.py` — dataset + GX validation.
- `requirements.txt` — `great-expectations`, `pandas`, `openai`.
