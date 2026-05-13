"""
Lab 7 — AI-driven catalogue enrichment (descriptions, ownership, SLA hints).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "outputs" / "enriched.json"


def enrich(dataset: dict) -> dict:
    """Return enriched catalogue fields."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {
            "table": dataset.get("table"),
            "description": "Contains customer sales transaction history (template).",
            "owner": "finance_team",
            "sla_recommendation": "Daily refresh",
        }

    client = OpenAI(api_key=api_key)
    prompt = (
        "Given this dataset metadata, return JSON only with keys: "
        "description (string), owner (string team name), sla_recommendation (string).\n"
        f"{json.dumps(dataset)}"
    )
    resp = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    text = resp.choices[0].message.content or "{}"
    start, end = text.find("{"), text.rfind("}")
    body = json.loads(text[start : end + 1])
    return {
        "table": dataset.get("table"),
        "description": body.get("description", ""),
        "owner": body.get("owner", ""),
        "sla_recommendation": body.get("sla_recommendation", ""),
    }


def main() -> None:
    dataset = {"table": "sales_transactions", "columns": ["txn_id", "amount", "ts"]}
    record = enrich(dataset)
    print(json.dumps(record, indent=2))
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print("Wrote:", OUT_PATH)


if __name__ == "__main__":
    main()
