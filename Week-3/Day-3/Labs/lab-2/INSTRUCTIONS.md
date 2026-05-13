# Lab 2 — Automated dbt lineage extraction

Extract a **dependency DAG** from a tiny **dbt-style** project by parsing `{{ ref('...') }}` in model SQL files.

## Prerequisites

- Python 3.11+
- Packages: see `requirements.txt`

## Setup

```bash
cd Labs/lab-2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Layout

| Path | Purpose |
|------|---------|
| `models/*.sql` | dbt model definitions |
| `app.py` | Lists models, parses refs, draws DAG |
| `outputs/dbt_dag.png` | Generated graph (created when you run) |

## Steps

### Step 1 — Inspect model SQL

Open `models/orders.sql`. It references `raw_orders` via `{{ ref('raw_orders') }}`. Open `models/raw_orders.sql` — it reads from `source_orders` (outside dbt refs for this small lab).

### Step 2 — Parse model files

Run:

```bash
python app.py
```

The script lists files in `models/` (equivalent to the doc’s `os.listdir("models")` idea, using `pathlib`).

### Step 3 — Extract dependencies

`extract_ref_dependencies` finds `ref('model_name')` calls and builds edges:

- `raw_orders` → `orders`

### Step 4 — Generate the DAG

NetworkX builds a directed graph; Matplotlib saves **`outputs/dbt_dag.png`**.

## Expected output

- Printed file list and edge list.
- PNG under `outputs/`.

## Exercises

1. **schema.yml**: Parse `models/schema.yml` (if you add one) and attach tests/tags to nodes.
2. **Macro lineage**: Detect `macro_name(...)` patterns and link macro dependencies.
3. **Export**: Save edges to JSON or GraphML in addition to PNG.

## Note

A full dbt project also uses `dbt ls --output json` and the **manifest.json** artifact for authoritative lineage. This lab keeps the parser explicit for learning.
