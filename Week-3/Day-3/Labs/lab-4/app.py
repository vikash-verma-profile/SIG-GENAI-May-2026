"""
Lab 4 — Business glossary auto-generation from table metadata / hints.
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "outputs"


def glossary_entry(table_name: str, columns: list[str] | None = None) -> dict[str, str]:
    columns = columns or []
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        definition = (
            f"{table_name.replace('_', ' ').title()}: "
            "Business-facing dataset derived from the listed columns; "
            "used for reporting and analytics."
        )
        return {"term": table_name, "definition": definition}

    client = OpenAI(api_key=api_key)
    prompt = (
        "Write one concise business glossary entry (1-3 sentences) for a data table. "
        "JSON only: {\"term\": string, \"definition\": string}.\n"
        f"table_name: {table_name}\ncolumns: {columns}"
    )
    resp = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    text = resp.choices[0].message.content or "{}"
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start : end + 1])


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tables = [
        ("customer_revenue", ["customer_id", "revenue_usd", "month"]),
        ("orders", ["order_id", "customer_id", "amount"]),
    ]
    rows = []
    for name, cols in tables:
        entry = glossary_entry(name, cols)
        print(entry)
        rows.append(entry)

    csv_path = OUT_DIR / "glossary.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition"])
        w.writeheader()
        w.writerows(rows)
    print("Wrote:", csv_path)


if __name__ == "__main__":
    main()
