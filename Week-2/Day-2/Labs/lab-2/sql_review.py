"""Lab 2 — SQL review for security, performance, and readability."""

import json
import re

from llm import ask_llm

REVIEW_PROMPT = """You are a principal data platform engineer reviewing SQL.

Evaluate the query for:
1) Security: injection patterns, over-broad SELECT *, unsafe dynamic fragments
2) Performance: missing filters, suspicious CROSS JOINs, non-sargable predicates
3) Readability: naming, formatting, clear intent

SQL dialect assumption unless stated: Snowflake.

Return STRICTLY valid JSON with keys:
{{
  "summary": "one sentence",
  "severity": "low|medium|high",
  "security": ["bullet"],
  "performance": ["bullet"],
  "readability": ["bullet"],
  "suggested_rewrite": "optional improved SQL or empty string"
}}

SQL to review:
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
    prompt = REVIEW_PROMPT.format(sql=sql.strip())
    raw = ask_llm(prompt)
    try:
        return extract_json(raw)
    except json.JSONDecodeError:
        return {
            "summary": "Model did not return parseable JSON.",
            "severity": "low",
            "security": [],
            "performance": [],
            "readability": [],
            "suggested_rewrite": "",
            "raw": raw,
        }
