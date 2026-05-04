import os
from datetime import date, datetime
from decimal import Decimal

from fastapi import FastAPI
import snowflake.connector

app = FastAPI()


def _snowflake_account(raw: str) -> str:
    raw = (raw or "").strip()
    for prefix in ("https://", "http://"):
        if raw.startswith(prefix):
            raw = raw[len(prefix) :]
    if ".snowflakecomputing.com" in raw:
        raw = raw.split(".snowflakecomputing.com")[0]
    return raw


def get_connection():
    account = _snowflake_account(os.environ["SNOWFLAKE_ACCOUNT"])
    return snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account=account,
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "OrderDB"),
        schema=os.environ.get("SNOWFLAKE_SCHEMA", "PUBLIC"),
    )

def _json_safe_cell(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value


def run_query(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [[_json_safe_cell(c) for c in row] for row in rows]

@app.post("/run_sql")
def run_sql(payload: dict):
    query = payload["query"]
    result = run_query(query)
    return {"query": query, "result": result}