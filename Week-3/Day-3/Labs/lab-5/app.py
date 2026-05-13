"""
Lab 5 — PII discovery and classification (regex-first agent pattern).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "outputs" / "classified.json"

EMAIL_RE = re.compile(r"\S+@\S+")
# Simple 10-digit phone (India-style example from course doc); refine for production.
PHONE_RE = re.compile(r"^\d{10}$")
# Aadhaar optional pattern (12 digits, often grouped) — exercise extension
AADHAAR_RE = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
# Credit card: rough Luhn-free pattern for lab
CC_RE = re.compile(r"\b(?:\d[ -]*?){13,16}\b")


def classify_row(email: str | float, phone: str | float) -> str:
    e = str(email) if pd.notna(email) else ""
    p = str(phone).replace(" ", "") if pd.notna(phone) else ""
    if EMAIL_RE.search(e) or (p and PHONE_RE.match(p)):
        return "Confidential"
    return "Internal"


def scan_dataframe(df: pd.DataFrame) -> dict:
    column_signals: dict[str, list[str]] = {}
    for col in df.columns:
        signals: list[str] = []
        sample = df[col].dropna().astype(str).head(20)
        for val in sample:
            if EMAIL_RE.search(val):
                signals.append("email_pattern")
            if PHONE_RE.match(val.replace(" ", "")):
                signals.append("phone_10digit")
            if AADHAAR_RE.search(val):
                signals.append("aadhaar_like")
            if CC_RE.search(val):
                signals.append("credit_card_like")
        if signals:
            column_signals[col] = sorted(set(signals))
    return column_signals


def main() -> None:
    df = pd.DataFrame(
        {
            "email": ["user@gmail.com", "invalid"],
            "phone": ["9876543210", "123"],
        }
    )
    print("Sample data:\n", df)

    for value in df["email"]:
        m = EMAIL_RE.search(str(value))
        print(f"email match for {value!r} -> {bool(m)}")

    df["classification"] = [classify_row(r.email, r.phone) for r in df.itertuples(index=False)]
    print("\nWith classification:\n", df)

    signals = scan_dataframe(df)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "column_signals": signals,
        "row_level_preview": df.astype(str).to_dict(orient="records"),
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("Wrote:", OUT_PATH)


if __name__ == "__main__":
    main()
