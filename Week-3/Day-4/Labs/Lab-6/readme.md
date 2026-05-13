# Lab 6 — Natural Language Analytics over Snowflake

Turn a natural-language question into SQL, run it against sample revenue data, and summarize the results. Optional Snowflake credentials use the real connector.

## Setup

```bash
cd Labs/Lab-6
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Optional Snowflake (also install `snowflake-connector-python`):

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`

## Steps

1. Review `data/revenue.csv`.
2. Run `python app.py`.
3. Confirm generated SQL, tabular results, and narrative summary.
4. Open `outputs/nl_analytics.json`.

## Exercises

- Replace rule-based SQL generation with an LLM.
- Add chart export from the result set.
- Add KPI templates for executive questions.
