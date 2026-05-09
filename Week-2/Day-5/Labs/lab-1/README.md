# Lab 1 — AI-generated pytest suite for e-commerce sales pipeline

**Domain:** E-commerce analytics  
**Goal:** Use AI-assisted testing (e.g., Claude Code / Copilot) with **pytest** to validate an ETL-style transformation.

**Architecture (conceptual):** Shopify API → Python ETL → Snowflake.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `ecommerce-pipeline/pipeline/sales_transform.py` | Transformation: drop rows with null `customer_id`, fill null `sales_amount` with `0`. |
| `ecommerce-pipeline/tests/test_sales_transform.py` | pytest suite (positive, null handling, edge cases). |
| `ecommerce-pipeline/requirements.txt` | Dependencies. |
| `ecommerce-pipeline/pytest.ini` | pytest config (`pythonpath` so `pipeline` imports work). |

---

## Prerequisites

- Python **3.11** recommended (3.10+ works).
- VS Code or similar editor.
- Optional: Claude Code / GitHub Copilot for generating or extending tests.

---

## Step-by-step

### 1. Create / use the project layout

You should have:

```text
ecommerce-pipeline/
  pipeline/
    __init__.py
    sales_transform.py
  tests/
    test_sales_transform.py
  requirements.txt
  pytest.ini
```

### 2. Install dependencies

Open a terminal, go to the pipeline root:

```bash
cd ecommerce-pipeline
pip install -r requirements.txt
```

This installs **pandas**, **pytest**, and **pytest-cov** (and transitive deps).

### 3. Understand the transformation

Open `pipeline/sales_transform.py`. The function `clean_sales_data(df)`:

- Drops rows where `customer_id` is null.
- Fills missing `sales_amount` with `0`.

### 4. Review or regenerate tests with AI (optional)

Prompt idea:

> Generate a complete pytest suite for `clean_sales_data` including positive tests, null handling, edge cases, and coverage-friendly structure.

Compare AI output with `tests/test_sales_transform.py` and merge improvements.

### 5. Run tests

From `ecommerce-pipeline`:

```bash
pytest
```

### 6. Run tests with coverage (terminal)

```bash
pytest --cov=.
```

### 7. HTML coverage report

```bash
pytest --cov=. --cov-report=html
```

Open `htmlcov/index.html` in a browser to review line coverage.

---

## Expected results

- All tests **pass**.
- Coverage report shows execution of `sales_transform.py` and tests.
- You understand how AI can accelerate pytest authoring while you keep architectural control.

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| `ModuleNotFoundError: pipeline` | Run pytest from `ecommerce-pipeline` (same folder as `pytest.ini`). |
| Import errors | Ensure `pipeline/__init__.py` exists. |

---

## Learning outcomes

- AI-generated / AI-assisted **pytest** patterns.
- **ETL-style** unit validation without a live warehouse.
