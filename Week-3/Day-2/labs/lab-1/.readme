# Lab 1 — Building an Autonomous Ingestion Agent

Build an ingestion agent that detects schema automatically, ingests files, validates records, and quarantines bad data.

## Learning outcomes

- Understand schema detection from a loaded dataset.
- Build a small ingestion pipeline with clear stages.
- Validate datasets automatically with rules.
- Implement a quarantine workflow for rejected rows.

## Prerequisites

- Python 3.11+
- VS Code or any editor; optional Jupyter for experiments.

## Step 1 — Environment

1. Open a terminal in `labs/lab-1`.
2. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Step 2 — Sample data

The file `data/sales.csv` is already provided with:

- `customer_id`, `revenue`, `email`
- One row with missing revenue and invalid email (for quarantine).

## Step 3 — Run the ingestion agent

```bash
python app.py
```

The script will:

1. Load `data/sales.csv`.
2. Print the dataframe head and inferred dtypes (schema).
3. Flag rows with null `revenue` or invalid `email` format.
4. Write valid rows to `processed/sales_valid.csv`.
5. Write invalid rows to `quarantine/bad_records.csv`.

## Step 4 — Expected output

- Valid rows in the `processed/` folder.
- Invalid rows in the `quarantine/` folder.
- Console logs showing schema and invalid row preview.

## Exercises (extend the lab)

1. **JSON ingestion**: Add a branch that reads `data/sales.json` (create a small JSON file) and runs the same validation.
2. **Schema drift**: Compare current column set and dtypes to a saved `schema_baseline.json`; print warnings on drift.
3. **Stricter email rules**: Reuse or extend the regex in `app.py` for your organization’s rules.
4. **Alerting**: On any quarantine write, log a message or call a webhook stub function.

## Folder structure

```text
lab-1/
  app.py
  requirements.txt
  README.md
  data/
    sales.csv
  quarantine/
  processed/
```
