"""
Lab 9: PII detection and coarse classification tags using regex heuristics.
"""
from __future__ import annotations

import re

import pandas as pd

EMAIL_PATTERN = re.compile(r"^\S+@\S+\.\S+$")
# 10-digit Indian-style mobile (simple lab heuristic; not exhaustive)
PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")
# Aadhaar-like 12 digits with optional spaces (format only — not a validator of real IDs)
AADHAAR_PATTERN = re.compile(r"^\d{4}\s?\d{4}\s?\d{4}$")
# Credit card-like 13–19 consecutive digits (Luhn not applied in this lab)
CARD_PATTERN = re.compile(r"^\d{13,19}$")


def classify_value(value: str) -> list[str]:
    tags: list[str] = []
    v = str(value).strip()
    if EMAIL_PATTERN.match(v):
        tags.append("PII_EMAIL")
    if PHONE_PATTERN.match(v):
        tags.append("PII_PHONE")
    if AADHAAR_PATTERN.match(v):
        tags.append("PII_AADHAAR_FORMAT")
    if CARD_PATTERN.match(re.sub(r"\s+", "", v)):
        tags.append("PII_CARD_FORMAT")
    return tags if tags else ["NON_PII_OR_UNKNOWN"]


def main() -> None:
    df = pd.DataFrame(
        {
            "email": ["user@gmail.com", "plain-text"],
            "phone": ["9876543210", "123"],
            "note": ["1234 5678 9012", "4111111111111"],
        }
    )
    for col in df.columns:
        df[f"{col}_tags"] = df[col].map(lambda x: ",".join(classify_value(x)))

    df["classification"] = "Confidential"
    print(df)


if __name__ == "__main__":
    main()
