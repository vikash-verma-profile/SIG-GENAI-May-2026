# Lab 3 — Great Expectations schema validation (banking)

**Domain:** Banking transactions  
**Goal:** Implement **schema / contract testing** with **Great Expectations** so bad rows (e.g., null keys) are caught before downstream loads.

**Architecture (conceptual):** Core banking → Delta Lake → Snowflake.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `data/transactions.csv` | Sample extract: includes a row with **empty** `customer_id`. |
| `validate_transactions.py` | Programmatic validation: `customer_id` must not be null (matches lab expectation). |
| `requirements.txt` | `pandas`, `great-expectations`. |

---

## Prerequisites

- Python **3.10+**.
- Terminal access.

---

## Step-by-step (CLI path — as in many course labs)

### 1. Install Great Expectations

```bash
cd lab-3
pip install -r requirements.txt
```

### 2. Initialize a Great Expectations project (interactive)

```bash
great_expectations init
```

Follow prompts to create the `great_expectations/` directory and config. Paths may vary by GX version.

### 3. Connect your dataset

Point GE at `data/transactions.csv` (or load it into pandas and register as a batch) according to your instructor’s GX version docs.

### 4. Create an expectation suite

```bash
great_expectations suite new
```

### 5. Add the key expectation

Add an expectation equivalent to:

- **`expect_column_values_to_not_be_null`** on column **`customer_id`**.

### 6. Create a checkpoint (e.g., `transactions_checkpoint`)

Wire the suite + datasource/batch into a checkpoint named to match your lab sheet (example name from course materials: **`transactions_checkpoint`**).

### 7. Run validation

```bash
great_expectations checkpoint run transactions_checkpoint
```

Review HTML or CLI validation results for failed expectations.

---

## Step-by-step (this repo — quick verification)

From `lab-3`:

```bash
pip install -r requirements.txt
python validate_transactions.py
```

You should see validation **FAIL** for this CSV (by design): one row has a null `customer_id`. That proves the rule fires.

---

## Expected results

- Validation surfaces the bad **`customer_id`** row.
- You can explain **contract testing** vs only unit tests.

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| GX CLI differs from docs | Check `great_expectations --help` and your installed **version** (`pip show great-expectations`). |
| Ephemeral vs file context | Course labs often use **file** context; this repo adds a **script** for quick demos. |

---

## Learning outcomes

- **Schema / quality contracts** on tabular data.
- Connecting **business rules** (non-null keys) to automated validation.
