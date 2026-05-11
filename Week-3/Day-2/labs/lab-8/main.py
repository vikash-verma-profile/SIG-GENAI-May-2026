"""
Lab 8: AI-assisted remediation — detect issues and apply deterministic fixes (LLM suggestions as text).
"""
from __future__ import annotations

import re

import pandas as pd


def email_valid(series: pd.Series) -> pd.Series:
    pattern = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    return series.astype(str).str.match(pattern, na=False)


def suggest_fix(bad_value: str) -> str:
    """Stub for an LLM: return a human-readable suggestion."""
    return (
        f"Suggested fix for '{bad_value}': insert '@' and a domain, "
        "trim spaces, and lowercase (example: user@company.com)."
    )


def main() -> None:
    df = pd.DataFrame(
        {
            "customer_id": [1, 2],
            "email": ["User@GMAIL.COM", "not-an-email"],
        }
    )
    invalid_mask = ~email_valid(df["email"])
    invalid_emails = df.loc[invalid_mask, "email"]
    print("Invalid emails:\n", invalid_emails)

    for val in invalid_emails:
        print("\n", suggest_fix(str(val)))

    # Deterministic correction: normalize casing and spacing for valid pattern rows
    df["email"] = df["email"].astype(str).str.strip().str.lower()
    print("\nAfter lower/strip:\n", df)

    # Optional: replace obvious placeholder (exercise: call OpenAI here)
    df.loc[invalid_mask, "email"] = df.loc[invalid_mask, "email"].replace(
        {"not-an-email": "unknown@pending.review"}
    )
    print("\nAfter placeholder remediation:\n", df)


if __name__ == "__main__":
    main()
