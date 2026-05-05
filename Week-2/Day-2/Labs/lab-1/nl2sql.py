"""
Lab 1 — NL2SQL patterns (Week-2 Day-2).

Edge cases to watch in production: ambiguous column names, timezone windows,
NULL aggregates, fan-out from joins, implicit dialect assumptions,
non-deterministic ORDER BY without keys, and permission-sensitive tables.
"""

import re

from llm import ask_llm

SCHEMA_CONTEXT = """
Database: analytic_dw (Snowflake-style SQL)

customers(customer_id PK, name, region, signup_date)
products(product_id PK, sku, category, unit_price)
orders(order_id PK, customer_id FK, order_date, status)
order_lines(order_line_id PK, order_id FK, product_id FK, quantity, line_total)

Grain:
- order_lines is one row per product line on an order.
- Revenue for an order is SUM(order_lines.line_total).
"""

FEW_SHOT = """
Q: Total revenue last month
SQL:
SELECT SUM(ol.line_total) AS revenue
FROM order_lines ol
JOIN orders o ON o.order_id = ol.order_id
WHERE o.order_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'
  AND o.order_date < DATE_TRUNC('month', CURRENT_DATE);

Q: Top 5 customers by revenue in 2025
SQL:
SELECT c.customer_id, c.name, SUM(ol.line_total) AS revenue
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_lines ol ON ol.order_id = o.order_id
WHERE o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01'
GROUP BY c.customer_id, c.name
ORDER BY revenue DESC
LIMIT 5;
"""


SYSTEM_PROMPT = f"""You are an expert analytics engineer. Generate ONE Snowflake-compatible SELECT query only.

{SCHEMA_CONTEXT}

Few-shot examples:
{FEW_SHOT}

Rules:
- Answer with SQL only (optional ```sql fence).
- Prefer explicit JOINs and qualified column names.
- Never mutate data (SELECT only).
- If the question is ambiguous, choose the most reasonable business interpretation and encode it in SQL comments only if needed.
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
    return sql_from_llm_output(raw)
