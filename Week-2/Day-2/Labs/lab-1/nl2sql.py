"""
Lab 1 — NL→dbt SQL (Week-2 Day-2).

Goal: generate dbt model SQL (using ref()/source()) from natural language.

Edge cases to watch in production: ambiguous column names, timezone windows,
NULL aggregates, fan-out from joins, implicit dialect assumptions,
non-deterministic ORDER BY without keys, and permission-sensitive tables.
"""

import re

from llm import ask_llm

SCHEMA_CONTEXT = """
dbt context (Snowflake-style SQL):

Sources (raw_store):
- customers(customer_id, name, region, signup_date)
- orders(order_id, customer_id, order_date, status)
- order_lines(order_line_id, order_id, product_id, quantity, line_total)
- products(product_id, sku, category, unit_price)

Staging models available (use ref()):
- stg_customers(customer_id, customer_name, region, signup_date)
- stg_orders(order_id, customer_id, order_at, order_status)
- stg_order_lines(order_line_id, order_id, product_id, quantity, line_total)

Grain:
- stg_order_lines: one row per product line on an order.
- Revenue for an order is SUM(line_total).
"""

FEW_SHOT = """
Q: Total revenue last month
SQL:
with orders as (
    select * from {{ ref('stg_orders') }}
),
lines as (
    select * from {{ ref('stg_order_lines') }}
)
select
    sum(lines.line_total) as revenue
from lines
inner join orders on orders.order_id = lines.order_id
where orders.order_at >= date_trunc('month', current_date) - interval '1 month'
  and orders.order_at < date_trunc('month', current_date);

Q: Top 5 customers by revenue in 2025
SQL:
with customers as (
    select * from {{ ref('stg_customers') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
),
lines as (
    select * from {{ ref('stg_order_lines') }}
)
select
    customers.customer_id,
    customers.customer_name,
    sum(lines.line_total) as revenue
from customers
inner join orders on orders.customer_id = customers.customer_id
inner join lines on lines.order_id = orders.order_id
where orders.order_at >= '2025-01-01' and orders.order_at < '2026-01-01'
group by customers.customer_id, customers.customer_name
order by revenue desc
limit 5;
"""


SYSTEM_PROMPT = f"""You are an expert analytics engineer. Generate ONE dbt model SQL query (Snowflake-compatible) only.

{SCHEMA_CONTEXT}

Few-shot examples:
{FEW_SHOT}

Rules:
- Output SQL only (optional ```sql fence). No explanation.
- Must start with WITH or SELECT.
- Do not output JSON, Python dicts, YAML, markdown lists, or commentary.
- Prefer using {{ ref('...') }} for upstream models.
- Never mutate data (SELECT only).
- Use clear CTE names and qualify columns when it reduces ambiguity.
"""


def sql_from_llm_output(text: str) -> str:
    text = text.strip()
    match = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text


def natural_language_to_sql(question: str) -> str:
    prompt = SYSTEM_PROMPT.strip() + "\n\nQ: " + question.strip() + "\nSQL:\n"
    raw = ask_llm(prompt)
    sql = sql_from_llm_output(raw)

    # Guardrail: dbt model SQL should look like SQL, not JSON/dicts.
    normalized = sql.lstrip().lower()
    if normalized.startswith("{") or ("select" not in normalized and "with" not in normalized):
        raise RuntimeError(
            "Model did not return SQL. Try a smaller model (e.g. llama3.2:3b) "
            "and re-run. Raw output preview:\n"
            + (raw.strip()[:500])
        )

    return sql
