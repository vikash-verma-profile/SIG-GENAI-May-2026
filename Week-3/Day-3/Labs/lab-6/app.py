"""
Lab 6 — AI-based governance policy draft generation from context.
"""
from __future__ import annotations

import os
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "outputs" / "policy_draft.txt"


def draft_policy(context: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return (
            "Policy draft (offline template):\n"
            "- All datasets containing PII must use encryption at rest and in transit.\n"
            "- Access is limited to authorized roles on a least-privilege basis.\n"
            "- Context supplied by data owner:\n"
            f"{context.strip()}\n"
        )

    client = OpenAI(api_key=api_key)
    prompt = (
        "Generate a concise internal governance policy draft (bullet list) "
        "based on the following dataset context. Keep it practical.\n\n"
        f"{context}"
    )
    resp = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return (resp.choices[0].message.content or "").strip()


def main() -> None:
    context = """Dataset contains PII.
Encryption required.
Access limited to finance and security roles."""
    text = draft_policy(context)
    print(text)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(text, encoding="utf-8")
    print("Wrote:", OUT_PATH)


if __name__ == "__main__":
    main()
