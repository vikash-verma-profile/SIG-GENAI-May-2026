import re

from llm import ask_llm

SCHEMA_CONTEXT = """
customers(customer_id PK, name, region, signup_date)
products(product_id PK, sku, category, unit_price)
orders(order_id PK, customer_id FK, order_date, status)
order_lines(order_line_id PK, order_id FK, product_id FK, quantity, line_total)
"""

SYSTEM_PROMPT = f"""You are a warehouse analyst assistant (Snowflake SQL).

{SCHEMA_CONTEXT}

Rules:
- Respond with one SELECT only.
- Optional ```sql fence.
"""


def sql_from_llm_output(text: str) -> str:
    text = text.strip()
    match = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text


def natural_language_to_sql(question: str) -> str:
    prompt = SYSTEM_PROMPT.strip() + "\n\nQuestion: " + question.strip() + "\nSQL:\n"
    return sql_from_llm_output(ask_llm(prompt))
