# Lab 3 — Automated Data Profiling

Profile a dataset and review distributions, nulls, and cardinality in an HTML report.

## Learning outcomes

- Generate a profiling report with `ydata-profiling`.
- Interpret null counts, cardinality, min/max, and distribution hints from the report.

## Prerequisites

- Python 3.11+

## Step 1 — Environment

```bash
cd labs/lab-3
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 — Run the profiler

```bash
python main.py
```

This will:

1. Create `data/customers.csv` with a mix of values (including null revenue and a skewed outlier).
2. Build a **minimal** `ProfileReport` (faster for class use).
3. Save `reports/profile.html`.

## Step 3 — Analyze the report

Open `reports/profile.html` in a browser and check:

- Null counts (especially `revenue`).
- Cardinality of `region`.
- Min/max and histogram shape for `revenue` (skew / outlier).

## Step 4 — Expected output

- Console: path to the HTML file and printed null counts.
- On disk: `reports/profile.html`.

## Exercises

1. Turn off `minimal=True` for a richer (slower) report on larger CSVs.
2. Profile two CSVs and compare alerts side by side (duplicate `main.py` logic with two inputs).
3. Summarize top findings in a short paragraph (manual “AI summary” of the report).

## Files

- `main.py` — builds data, runs `ProfileReport`, writes HTML.
- `data/` — sample CSV output.
- `reports/` — `profile.html`.
