"""
Lab 7: Auto-quarantine workflow for invalid emails.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "sales.csv"
QUARANTINE = ROOT / "quarantine"


def email_valid(series: pd.Series) -> pd.Series:
    pattern = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    return series.astype(str).str.match(pattern, na=False)


def main() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    invalid_rows = df.loc[~email_valid(df["email"])].copy()
    invalid_rows.to_csv(QUARANTINE / "invalid.csv", index=False)
    print("Quarantined rows:\n", invalid_rows)
    print("Quarantined rows count:", len(invalid_rows))
    print(f"Written to {QUARANTINE / 'invalid.csv'}")


if __name__ == "__main__":
    main()
