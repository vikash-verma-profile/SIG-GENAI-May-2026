### Lab 6 — Schema evolution (union / defaults) + optional PySpark union

### Prerequisites

- **Python**: 3.10+ recommended
- **Dependencies**:

```bash
pip install -r requirements.txt
```

### Dataset

CSV snapshots under `data/`:

- `products_day1.csv` (baseline columns)
- `products_day2.csv` introduces **`brand`**
- `products_day3.csv` introduces **`discount`**

### Run — Pandas pipeline

From `Labs/lab-6`:

```powershell
python .\pipeline.py
```

### Expected output

- **`output/final_products.csv`**
- Columns should include **`brand`** and **`discount`** with safe defaults for older rows.

### Optional PySpark exercise

This repo’s `spark_merge.py` demonstrates **`unionByName(..., allowMissingColumns=True)`** across the three CSV files (more representative than “mergeSchema on a CSV folder” tutorials).

```powershell
python .\spark_merge.py
```

### Tests

From `Labs/lab-6`:

```powershell
python -m pytest .\tests -v
```

### Suggested “hands-on” checks

- Add a new CSV snapshot with a new column (exercise: **`rating`**) and confirm union+clean behavior still works.

### Gen AI / Ollama

Use Ollama while designing union/default rules; no runtime **`--ai`** in this lab. See **`../genai/README.md`** and **`../README.md`**.
