# Week-2 Day-2 Labs — Student Step-by-Step Guide

This guide walks you through **creating every file and folder** for Lab 1, Lab 2, Lab 3, and the Case Study, in a sensible order. If this repository already contains the finished files, use this document as a **checklist** while you re-create or trace the project.

**Suggested workspace root:** `Week-2/Day-2/labs/` (the folder that contains `requirements.txt`).

---

## What you will build

| Area | Folder | What it demonstrates |
|------|--------|----------------------|
| Lab 1 | `lab-1/` | NL→SQL with schema context, few-shot examples, Ollama |
| Lab 2 | `lab-2/` | SQL review agent (security, performance, readability) |
| Lab 3 | `lab3/` | dbt staging + marts + tests; optional AI YAML helper |
| Case study | `case-study/` | Chain NL→SQL → review → optional save; Cortex notes |

---

## Prerequisites (before any lab)

1. **Python 3.10+** installed.
2. **Ollama** installed and running (Windows tray app is enough). You do **not** need a second `ollama serve` if port `11434` is already in use — that means Ollama is already up.
3. Pull the model used by the code (default **`llama3`**):

   ```bash
   ollama pull llama3
   ```

4. Optional for Lab 3: **dbt** + adapter for your warehouse (e.g. `dbt-snowflake`), and a **`profiles.yml`** entry named **`retail_dw`** pointing at a database where raw tables will live.

---

## Part 0 — Shared project setup

### Step 0.1 — Create the root folder

1. Create the folder: `labs/` (if it does not exist).
2. Open a terminal **inside** `labs/`.

### Step 0.2 — Create `requirements.txt`

1. In `labs/`, create **`requirements.txt`**.
2. Add one dependency used by all Python labs:

   ```text
   requests>=2.28.0
   ```

### Step 0.3 — Install dependencies

From `labs/`:

```bash
pip install -r requirements.txt
```

### Step 0.4 — Create the shared `llm.py` (used in every Python lab)

Each lab folder keeps its **own copy** of `llm.py` so you can zip or move one lab without fixing imports.

Create **the same file** in:

- `lab-1/llm.py`
- `lab-2/llm.py`
- `lab3/llm.py`
- `case-study/llm.py`

**File contents for each `llm.py`:**

```python
import os

import requests

OLLAMA_URL = os.environ.get(
    "OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate",
)
CONNECT_TIMEOUT_S = float(os.environ.get("OLLAMA_CONNECT_TIMEOUT", "5"))
READ_TIMEOUT_S = float(os.environ.get("OLLAMA_READ_TIMEOUT", "300"))


def ask_llm(prompt: str, model: str | None = None) -> str:
    model = model or os.environ.get("OLLAMA_MODEL", "llama3")
    base = OLLAMA_URL.replace("/api/generate", "").rstrip("/") or "http://127.0.0.1:11434"

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=(CONNECT_TIMEOUT_S, READ_TIMEOUT_S),
        )
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            f"Cannot reach Ollama at {base}. Start the Ollama app or run "
            f"`ollama serve`, then `ollama pull {model}` if needed."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Ollama did not respond in time (first run loads the model into RAM "
            f"and can exceed {READ_TIMEOUT_S:.0f}s). Raise OLLAMA_READ_TIMEOUT if needed."
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        response.raise_for_status()
        raise RuntimeError(
            f"Ollama returned non-JSON body (status {response.status_code}): "
            f"{response.text[:500]}"
        ) from exc

    if not response.ok:
        err = data.get("error", data)
        raise RuntimeError(f"Ollama HTTP {response.status_code}: {err}")

    if "error" in data and "response" not in data:
        raise RuntimeError(f"Ollama error: {data['error']}")

    if "response" not in data:
        raise RuntimeError(
            f"Unexpected Ollama JSON (no 'response' key): {data}"
        )

    return data["response"]
```

**Student checklist:**

- [ ] Four copies of `llm.py` exist (Lab 1, Lab 2, Lab 3, Case Study).

---

## Lab 1 — NL2SQL (`lab-1/`)

### Goal

Turn natural-language questions into **Snowflake-style `SELECT`** statements using **schema context** and **few-shot** SQL examples.

### Step 1.1 — Create folder

Create: `labs/lab-1/`

### Step 1.2 — Add `llm.py`

Copy the shared **`llm.py`** from Part 0 into `lab-1/llm.py`.

### Step 1.3 — Create `nl2sql.py`

1. Create `lab-1/nl2sql.py`.
2. Implement these pieces **in order** inside the file:
   - **Docstring** at top: one paragraph on NL2SQL **edge cases** (ambiguous columns, time zones, NULL aggregates, join fan-out, dialect drift).
   - **Imports:** `import re` and `from llm import ask_llm`.
   - **`SCHEMA_CONTEXT`** (multi-line string): tables `customers`, `products`, `orders`, `order_lines` with PK/FK notes and **grain** (one row per line item; revenue = sum of `line_total`).
   - **`FEW_SHOT`** (multi-line string): **two** question/SQL pairs, for example:
     - Total revenue last month (join `order_lines` to `orders`, filter on `order_date`).
     - Top 5 customers by revenue in a calendar year (join all needed tables, `GROUP BY`, `ORDER BY`, `LIMIT`).
   - **`SYSTEM_PROMPT`**: an f-string that concatenates role (“expert analytics engineer”), dialect (**Snowflake**), `SCHEMA_CONTEXT`, `FEW_SHOT`, and **rules** (single SELECT only, optional ```sql fence, explicit JOINs, read-only).
   - **`sql_from_llm_output(text)`**: strip optional Markdown ```sql … ``` fences with `re.search(..., re.DOTALL | re.IGNORECASE)`.
   - **`natural_language_to_sql(question)`**: append user question to the system prompt, call `ask_llm`, return cleaned SQL via `sql_from_llm_output`.

You can compare your result with the reference implementation already in this repo: `lab-1/nl2sql.py`.

### Step 1.4 — Create `main.py`

1. Create `lab-1/main.py`.
2. Loop forever:
   - Read a **Question:** line from the user.
   - On **Ctrl+C** or EOF, exit cleanly.
   - Skip empty input.
   - Call `natural_language_to_sql`; catch **`RuntimeError`** from networking/Ollama and print the message.
   - Print the generated SQL.

Reference behavior matches `lab-1/main.py` in this repo.

### Step 1.5 — Run Lab 1

From `labs/`:

```bash
python lab-1/main.py
```

Try: “Total revenue by customer”, “Orders per region last quarter”, etc.

**Student checklist:**

- [ ] `lab-1/llm.py`
- [ ] `lab-1/nl2sql.py`
- [ ] `lab-1/main.py`
- [ ] Lab runs and prints SQL when Ollama is up.

---

## Lab 2 — SQL review agent (`lab-2/`)

### Goal

Send arbitrary SQL to the model and receive **structured JSON** covering security, performance, and readability.

### Step 2.1 — Create folder

Create: `labs/lab-2/`

### Step 2.2 — Add `llm.py`

Copy the shared **`llm.py`** into `lab-2/llm.py`.

### Step 2.3 — Create `sql_review.py`

1. Create `lab-2/sql_review.py`.
2. Add module docstring: purpose (review agent).
3. **Imports:** `json`, `re`, `from llm import ask_llm`.
4. **`REVIEW_PROMPT`**: instruct the model as a principal engineer; require **strict JSON** with keys:
   - `summary`, `severity` (`low|medium|high`), `security`, `performance`, `readability` (arrays of strings), `suggested_rewrite`.
   - Include `{sql}` placeholder inside a fenced SQL block (use **doubled braces** `{{` `}}` where you need literal `{` `}` in an f-string later — or build the string with `.format(sql=...)` as in the reference).
5. **`extract_json(text)`**: optional ```json fence stripping; then `json.loads`.
6. **`review_sql(sql)`**: format prompt with the SQL, call `ask_llm`, parse JSON; on failure return a dict with empty lists and a `raw` field holding the model output.

Reference: `lab-2/sql_review.py`.

### Step 2.4 — Create `main.py`

1. Create `lab-2/main.py`.
2. Loop:
   - Prompt user to paste SQL lines until a **blank line** ends input.
   - Join lines into one string; skip if empty.
   - Call `review_sql`, print `json.dumps(..., indent=2)`.

Reference: `lab-2/main.py`.

### Step 2.5 — Run Lab 2

```bash
python lab-2/main.py
```

Paste a deliberately bad query (e.g. `SELECT *` with a cross join) and inspect the JSON.

**Student checklist:**

- [ ] `lab-2/llm.py`
- [ ] `lab-2/sql_review.py`
- [ ] `lab-2/main.py`

---

## Lab 3 — dbt project + optional generator (`lab3/`)

### Goal

Model **staging** views over **`source()`** tables and **marts** (`dim_customer`, `fct_order_lines`) with **`schema.yml`** tests. Optionally run **`generate_stubs.py`** to draft exposure YAML via Ollama.

### Step 3.1 — Create folders

Create this tree (empty files come next):

```text
lab3/
  llm.py                    ← shared Ollama client (copy from Part 0)
  generate_stubs.py         ← optional Python helper
  retail_dw/
    dbt_project.yml
    models/
      sources.yml
      schema.yml
      staging/
        stg_customers.sql
        stg_orders.sql
        stg_order_lines.sql
      marts/
        dim_customer.sql
        fct_order_lines.sql
```

### Step 3.2 — Copy `lab3/llm.py`

Same contents as Part 0.

### Step 3.3 — Create `retail_dw/dbt_project.yml`

Create `lab3/retail_dw/dbt_project.yml`:

```yaml
name: retail_dw
version: "1.0.0"
config-version: 2

profile: retail_dw

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

models:
  retail_dw:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

### Step 3.4 — Create `models/sources.yml`

Define source **`raw_store`** with tables **`customers`**, **`orders`**, **`order_lines`**, **`products`** and column lists (minimal stubs are fine). Reference copy:

```yaml
version: 2

sources:
  - name: raw_store
    description: Landing-zone tables ingested from operational DB.
    tables:
      - name: customers
        columns:
          - name: customer_id
          - name: name
          - name: region
          - name: signup_date
      - name: orders
        columns:
          - name: order_id
          - name: customer_id
          - name: order_date
          - name: status
      - name: order_lines
        columns:
          - name: order_line_id
          - name: order_id
          - name: product_id
          - name: quantity
          - name: line_total
      - name: products
        columns:
          - name: product_id
          - name: sku
          - name: category
          - name: unit_price
```

### Step 3.5 — Create staging models

**`models/staging/stg_customers.sql`**

```sql
select
    customer_id,
    trim(name) as customer_name,
    region,
    signup_date::date as signup_date
from {{ source("raw_store", "customers") }}
```

**`models/staging/stg_orders.sql`**

```sql
select
    order_id,
    customer_id,
    order_date::timestamp_ntz as order_at,
    lower(trim(status)) as order_status
from {{ source("raw_store", "orders") }}
```

**`models/staging/stg_order_lines.sql`**

```sql
select
    order_line_id,
    order_id,
    product_id,
    quantity::number(18, 4) as quantity,
    line_total::number(18, 2) as line_total
from {{ source("raw_store", "order_lines") }}
```

### Step 3.6 — Create mart models

**`models/marts/dim_customer.sql`**

```sql
with customers as (
    select * from {{ ref("stg_customers") }}
)

select
    customer_id,
    customer_name,
    region,
    signup_date
from customers
```

**`models/marts/fct_order_lines.sql`**

```sql
with lines as (
    select * from {{ ref("stg_order_lines") }}
),
orders as (
    select * from {{ ref("stg_orders") }}
)

select
    lines.order_line_id,
    lines.order_id,
    lines.product_id,
    orders.customer_id,
    orders.order_at,
    orders.order_status,
    lines.quantity,
    lines.line_total
from lines
inner join orders on orders.order_id = lines.order_id
```

### Step 3.7 — Create `models/schema.yml`

Add **`not_null`** / **`unique`** tests for keys and important facts. Reference:

```yaml
version: 2

models:
  - name: stg_customers
    columns:
      - name: customer_id
        tests:
          - not_null
          - unique
      - name: signup_date
        tests:
          - not_null

  - name: stg_orders
    columns:
      - name: order_id
        tests:
          - not_null
          - unique

  - name: stg_order_lines
    columns:
      - name: order_line_id
        tests:
          - not_null
          - unique

  - name: dim_customer
    columns:
      - name: customer_id
        tests:
          - not_null
          - unique

  - name: fct_order_lines
    columns:
      - name: order_line_id
        tests:
          - not_null
          - unique
      - name: line_total
        tests:
          - not_null
```

### Step 3.8 — (Optional) Configure dbt profile

1. Create or edit **`~/.dbt/profiles.yml`** (Windows: `%USERPROFILE%\.dbt\profiles.yml`).
2. Add a **`retail_dw`** target that maps `raw_store` tables to your warehouse database/schema.

Without a live warehouse, treat Lab 3 as **SQL/YAML authoring practice**; run **`dbt parse`** or **`dbt compile`** only after credentials exist.

### Step 3.9 — Create `generate_stubs.py`

1. Create `lab3/generate_stubs.py`.
2. Import `from llm import ask_llm`.
3. Add function **`exposure_yaml_stub(exposure_name, owner_email, depends_on)`** that builds a short prompt asking for minimal **dbt exposures** YAML.
4. Under `if __name__ == "__main__":`, **`input()`** three strings with sensible defaults and print the model output.

Reference: `lab3/generate_stubs.py`.

### Step 3.10 — Run the helper (optional)

From `labs/`:

```bash
python lab3/generate_stubs.py
```

**Student checklist:**

- [ ] Full `lab3/retail_dw/` tree
- [ ] `profiles.yml` planned or configured
- [ ] Optional: `generate_stubs.py` runs

---

## Case study (`case-study/`)

### Goal

Run **NL→SQL**, then **review** the generated SQL, and optionally write **`output/last_query.sql`**. Include a small **`cortex_stub`** describing how **Snowflake Cortex Analyst** relates to governed semantic layers.

### Step 4.1 — Create folder

Create: `labs/case-study/`

### Step 4.2 — Add `llm.py`

Copy shared **`llm.py`** into `case-study/llm.py`.

### Step 4.3 — Create `nl2sql.py`

Slightly **smaller** prompt than Lab 1 is fine: same pattern (`SCHEMA_CONTEXT`, `SYSTEM_PROMPT`, fence stripper, `natural_language_to_sql`). Reference: `case-study/nl2sql.py`.

### Step 4.4 — Create `sql_review.py`

Simpler JSON schema than Lab 2 is acceptable (`summary`, `severity`, `findings`, `suggested_rewrite`). Reference: `case-study/sql_review.py`.

### Step 4.5 — Create `cortex_stub.py`

1. Module docstring explaining **Cortex Analyst** vs local NL2SQL.
2. Function **`describe_cortex_flow()`** returning a multi-line string with numbered steps (semantic views, metadata, routing prompts to Cortex, alignment with dbt marts).

Reference: `case-study/cortex_stub.py`.

### Step 4.6 — Create `main.py`

1. Import `json`, `Path`.
2. Import `describe_cortex_flow`, `natural_language_to_sql`, `review_sql`.
3. Define **`OUTPUT_DIR`** as `case-study/output`.
4. Define **`run(question)`** returning dict with question, sql, review.
5. Loop: read business question; if blank, exit; print SQL and review; optionally **`mkdir`** and write **`last_query.sql`**.

Reference: `case-study/main.py`.

### Step 4.7 — Run case study

```bash
python case-study/main.py
```

**Student checklist:**

- [ ] `case-study/llm.py`
- [ ] `case-study/nl2sql.py`
- [ ] `case-study/sql_review.py`
- [ ] `case-study/cortex_stub.py`
- [ ] `case-study/main.py`

---

## Environment variables (optional)

| Variable | Purpose |
|----------|---------|
| `OLLAMA_URL` | Override API URL (default uses `127.0.0.1:11434`). |
| `OLLAMA_MODEL` | Model tag (default `llama3`). |
| `OLLAMA_CONNECT_TIMEOUT` | Seconds to wait for TCP connect (default `5`). |
| `OLLAMA_READ_TIMEOUT` | Seconds to wait for generation (default `300`). |

PowerShell example:

```powershell
$env:OLLAMA_MODEL="llama3"
python lab-1/main.py
```

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| “Cannot reach Ollama” | Ollama app running; `ollama list` works; model pulled. |
| Hang then Ctrl+C | Previously often **`localhost`** vs IPv6; code uses **`127.0.0.1`** by default. |
| `bind: ... 11434 ... permitted` when running `ollama serve` | Ollama already listening; **do not** start a second server. |
| dbt errors about sources | Raw tables not created or `profiles.yml` schema/database mismatch. |
| Lab 2 JSON parse errors | Model returned prose; retry or tighten prompt; code keeps `raw` for debugging. |

---

## Final folder map (complete solution)

```text
labs/
  requirements.txt
  STUDENT_LAB_GUIDE.md
  lab-1/
    llm.py
    nl2sql.py
    main.py
  lab-2/
    llm.py
    sql_review.py
    main.py
  lab3/
    llm.py
    generate_stubs.py
    retail_dw/
      dbt_project.yml
      models/
        sources.yml
        schema.yml
        staging/
          stg_customers.sql
          stg_orders.sql
          stg_order_lines.sql
        marts/
          dim_customer.sql
          fct_order_lines.sql
  case-study/
    llm.py
    nl2sql.py
    sql_review.py
    cortex_stub.py
    main.py
    output/              ← created at runtime when you choose to save SQL
```

Congratulations — you have implemented the full Week-2 Day-2 lab track end to end.
