"""
Lab 6 — Natural language analytics over warehouse-style data (local demo).
"""
from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "revenue.csv"
OUT_DIR = ROOT / "outputs"


def load_local_warehouse() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def natural_language_to_sql(question: str) -> str:
    lowered = question.lower()
    if "monthly" in lowered and "revenue" in lowered:
        return (
            "SELECT month, region, SUM(revenue) AS total_revenue "
            "FROM revenue GROUP BY month, region ORDER BY month, region"
        )
    if "north" in lowered:
        return "SELECT month, revenue FROM revenue WHERE region = 'North' ORDER BY month"
    return "SELECT region, SUM(revenue) AS total_revenue FROM revenue GROUP BY region"


def execute_sql(df: pd.DataFrame, sql_query: str) -> pd.DataFrame:
    conn = sqlite3.connect(":memory:")
    df.to_sql("revenue", conn, index=False)
    result = pd.read_sql_query(sql_query, conn)
    conn.close()
    return result


def summarize_results(df: pd.DataFrame) -> str:
    if df.empty:
        return "No rows returned for the generated SQL."
    if "total_revenue" in df.columns:
        top = df.sort_values("total_revenue", ascending=False).iloc[0]
        if "region" in df.columns:
            return (
                f"Revenue increased steadily; highest total revenue is in "
                f"{top['region']} at {int(top['total_revenue'])}."
            )
    return "Revenue increased steadily across the queried slice."


def try_snowflake(sql_query: str) -> str | None:
    if not os.getenv("SNOWFLAKE_ACCOUNT"):
        return None
    try:
        import snowflake.connector  # type: ignore
    except ImportError:
        return None

    conn = snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)


def main() -> None:
    question = "Generate SQL for monthly revenue trend."
    sql_query = natural_language_to_sql(question)
    print("Generated SQL:\n", sql_query)

    df = load_local_warehouse()
    result = execute_sql(df, sql_query)
    print("\n--- Query result ---")
    print(result)

    summary = summarize_results(result)
    print("\n--- Narrative ---")
    print(summary)

    snowflake_note = try_snowflake(sql_query)
    if snowflake_note is None:
        snowflake_note = "Snowflake not configured; local SQLite demo used."

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "nl_analytics.json"
    out_path.write_text(
        json.dumps(
            {
                "question": question,
                "sql": sql_query,
                "rows": result.to_dict(orient="records"),
                "summary": summary,
                "snowflake": snowflake_note,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
