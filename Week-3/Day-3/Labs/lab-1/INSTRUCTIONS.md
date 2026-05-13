# Lab 1 — Automated SQL lineage extraction using LLMs (foundation)

This lab builds a **small end-to-end lineage pipeline**: read SQL → parse with `sqlparse` → infer source tables → build a **directed graph** → export **JSON** and a **PNG** diagram.

## Prerequisites

- Python **3.11+** (3.10+ usually works)
- VS Code or any editor; optional Jupyter for experiments
- Terminal / PowerShell

## Setup

1. Open a terminal in `Labs/lab-1`.
2. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Folder layout

| Path | Purpose |
|------|---------|
| `sql/query.sql` | Sample SQL to analyze |
| `lineage/` | Exported lineage metadata (JSON) |
| `outputs/` | Generated graph image |
| `app.py` | Main script |

## Steps (follow in order)

### Step 1 — Inspect the sample SQL

Open `sql/query.sql`. You should see a join between `customers` and `orders`. These are the **upstream** tables for an imaginary **output** node named `output_table`.

### Step 2 — Read the SQL in Python

`app.py` calls `read_sql()` which opens `sql/query.sql` and loads the text. Run:

```bash
python app.py
```

Confirm the SQL prints under `--- SQL ---`.

### Step 3 — Parse with sqlparse

The script uses `sqlparse.parse(...)` and prints how many statements were parsed. This matches the course idea of using a parser before any LLM enrichment.

### Step 4 — Extract table names

`extract_tables()` uses a **heuristic** on `FROM` / `JOIN` clauses (good for teaching; production systems often use deeper AST walks or specialized engines). Check the printed list: expect `customers` and `orders`.

### Step 5 — Build lineage mapping

Each source table maps to the logical target `output_table`, matching the lab brief (`customers → output_table`, `orders → output_table`).

### Step 6 — Visualize and export

- **JSON**: `lineage/lineage.json` lists edges `from` → `to`.
- **Graph**: `outputs/lineage_graph.png` shows the directed graph.

## Expected result

- Console: parsed statement count, table list, lineage dict.
- Files: `lineage/lineage.json` and `outputs/lineage_graph.png`.

## Exercises (from course doc)

1. **CTEs**: Add a `WITH` clause in `query.sql` and extend extraction to include CTE names vs base tables.
2. **Column-level lineage**: For each selected column, record which source column it came from (requires richer parsing or an LLM-assisted mapper).
3. **More exports**: Add CSV or GraphML export alongside JSON.

## Notes on LLMs

This lab uses **deterministic parsing** first—the doc’s “LLMs for semantic extraction” is the natural next step: pass ambiguous SQL or business names to a model **after** you have parser output as context.
