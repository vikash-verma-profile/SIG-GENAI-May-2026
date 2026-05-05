import json
import re

from llm import ask_llm

REVIEW_PROMPT = """Review this SQL for security, performance, readability (Snowflake).

Return STRICT JSON:
{{ "summary": "", "severity": "low|medium|high", "findings": [], "suggested_rewrite": "" }}

SQL:
```
{sql}
```
"""


def extract_json(text: str) -> dict:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    return json.loads(text)


def review_sql(sql: str) -> dict:
    raw = ask_llm(REVIEW_PROMPT.format(sql=sql.strip()))
    try:
        return extract_json(raw)
    except json.JSONDecodeError:
        return {"summary": "Unparseable JSON", "severity": "low", "findings": [], "raw": raw}
