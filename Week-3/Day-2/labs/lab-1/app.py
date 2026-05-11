"""
Lab 1: Autonomous ingestion agent — schema detection, validation, quarantine, processed output.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "sales.csv"
QUARANTINE_DIR = ROOT / "quarantine"
PROCESSED_DIR = ROOT / "processed"


def ensure_dirs() -> None:
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset(csv_path: Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def detect_schema(df: pd.DataFrame) -> pd.Series:
    return df.dtypes


def email_valid(series: pd.Series) -> pd.Series:
    pattern = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    return series.astype(str).str.match(pattern, na=False)


def validate_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split into valid vs invalid (null revenue or invalid email)."""
    bad_revenue = df["revenue"].isna()
    bad_email = ~email_valid(df["email"])
    invalid_mask = bad_revenue | bad_email
    invalid_rows = df.loc[invalid_mask].copy()
    valid_rows = df.loc[~invalid_mask].copy()
    return valid_rows, invalid_rows


def main() -> None:
    ensure_dirs()
    df = load_dataset(DATA)
    print("Head:\n", df.head(), "\n")
    schema = detect_schema(df)
    print("Inferred schema (dtypes):\n", schema, "\n")

    valid, invalid = validate_rows(df)
    print("Invalid rows:\n", invalid, "\n")

    if not invalid.empty:
        invalid.to_csv(QUARANTINE_DIR / "bad_records.csv", index=False)
    valid.to_csv(PROCESSED_DIR / "sales_valid.csv", index=False)

    print(f"Valid rows written: {len(valid)} -> processed/sales_valid.csv")
    print(f"Quarantined rows: {len(invalid)} -> quarantine/bad_records.csv")


if __name__ == "__main__":
    main()
