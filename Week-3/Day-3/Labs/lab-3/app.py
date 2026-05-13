"""
Lab 3 — AI-powered metadata tagging (OpenAI optional; heuristic fallback).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "metadata.json"
OUT_PATH = ROOT / "outputs" / "tags.json"


def load_metadata() -> dict:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def heuristic_tags(meta: dict) -> list[str]:
    """Rule-based tags when no API key is configured."""
    tags = ["Finance", "Customer Data"]
    name = meta.get("table", "").lower()
    if "customer" in name or "pii" in str(meta.get("columns", [])).lower():
        tags.append("Confidential")
    return list(dict.fromkeys(tags))


def llm_tags(meta: dict) -> list[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return heuristic_tags(meta)

    client = OpenAI(api_key=api_key)
    prompt = (
        "Generate 3-6 short business and data-sensitivity tags for this dataset. "
        "Respond as JSON only: {\"tags\": [\"...\", ...]}\n\n"
        f"{json.dumps(meta)}"
    )
    resp = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    text = resp.choices[0].message.content or "{}"
    start, end = text.find("{"), text.rfind("}")
    payload = json.loads(text[start : end + 1])
    return list(payload.get("tags", heuristic_tags(meta)))


def main() -> None:
    meta = load_metadata()
    print("Metadata:", meta)
    tags = llm_tags(meta)
    print("Generated tags:", tags)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps({"table": meta["table"], "tags": tags}, indent=2), encoding="utf-8")
    print("Wrote:", OUT_PATH)


if __name__ == "__main__":
    main()
