import re
import requests
from llm import ask_llm

SYSTEM_PROMPT = """
You are a SQL assistant.

Table:
sales_data(id, region, revenue, sale_date)

Rules:
- Only generate SQL
- No explanation
"""


def _sql_from_llm_output(text: str) -> str:
    """Strip optional ``` / ```sql fences so Snowflake gets raw SQL."""
    text = text.strip()
    m = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return text


def process_prompt(user_input):
    full_prompt = SYSTEM_PROMPT + "\nUser: " + user_input

    sql_query = _sql_from_llm_output(ask_llm(full_prompt))

    print("Generated SQL:", sql_query)

    # Call MCP server
    response = requests.post(
        "http://127.0.0.1:8000/run_sql",
        json={"query": sql_query},
        timeout=120,
    )
    response.raise_for_status()
    if not (response.text or "").strip():
        raise RuntimeError(
            "SQL server returned an empty body. Is `uvicorn app:app --reload` "
            "running on port 8000?"
        )
    try:
        return response.json()
    except ValueError as exc:
        preview = (response.text or "")[:500]
        raise RuntimeError(
            f"SQL server returned non-JSON (HTTP {response.status_code}): {preview!r}"
        ) from exc
