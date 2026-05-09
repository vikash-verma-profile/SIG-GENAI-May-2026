# Lab 1: AI-Generated Streamlit Sales Dashboard

**Domain:** E-Commerce Analytics

## Objective

Build a **Sales Pipeline Health Dashboard** using [Streamlit](https://streamlit.io/) and AI-assisted coding (e.g. Claude Code, GitHub Copilot).

## Architecture

```
Shopify API → Metadata JSON → Streamlit Dashboard
```

*(In this lab you use a local `metadata.json` file to simulate pipeline metadata.)*

## What you need

- Python 3.11 (or compatible 3.x)
- Streamlit, pandas
- An AI coding assistant (Claude Code, Copilot, or Cursor)

Install dependencies:

```bash
pip install streamlit pandas
```

## Steps

### 1. Create the project folder

```bash
mkdir ecommerce-dashboard
cd ecommerce-dashboard
```

### 2. Create the metadata file

Create `metadata.json` in the project root with sample pipeline runs, for example:

```json
[
  {
    "pipeline": "sales_etl",
    "status": "Success",
    "last_run": "2026-05-07 09:00",
    "row_count": 150000
  },
  {
    "pipeline": "inventory_etl",
    "status": "Failed",
    "last_run": "2026-05-07 09:15",
    "row_count": 0
  }
]
```

### 3. Use an AI prompt

Ask your assistant to generate a Streamlit dashboard for monitoring ETL pipelines. Include in your request:

- Status cards  
- Last execution time  
- Row count metrics  
- Failure alerts  

### 4. Create `app.py`

Start from a minimal version, then iterate with AI:

```python
import streamlit as st
import pandas as pd
import json

with open("metadata.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)
st.title("Pipeline Health Dashboard")
st.dataframe(df)
```

### 5. Run the dashboard

```bash
streamlit run app.py
```

### 6. Enhance the dashboard

Add at least a few of:

- Charts (e.g. status breakdown, row counts)  
- Filters  
- Search  
- SLA-style alerts (e.g. highlight failed pipelines or stale runs)  

## Deliverables

- Working Streamlit dashboard  
- Code in a Git repository (e.g. GitHub)  
- Short demo walkthrough (video or written)  

## Learning outcomes

- Practice AI-generated dashboard code  
- Streamlit basics  
- Rapid prototyping with AI assistance  

## Tips

- Run from the same folder as `metadata.json`, or use a path relative to your script.  
- Commit small changes so you can compare AI-generated versions.  
