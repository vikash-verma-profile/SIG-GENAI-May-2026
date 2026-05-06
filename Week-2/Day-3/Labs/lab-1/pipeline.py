"""Part B: modular healthcare ETL — optional Ollama-driven cleaning parameters (JSON-only)."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data" / "patients.csv"
OUT_DIR = Path(__file__).resolve().parent / "output"

LABS_ROOT = Path(__file__).resolve().parent.parent
if str(LABS_ROOT) not in sys.path:
    sys.path.insert(0, str(LABS_ROOT))


def load_data(file_path: Path) -> pd.DataFrame:
    """Load patient data from CSV file."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}") from e


def clean_data(df: pd.DataFrame, ai_spec: dict | None = None) -> pd.DataFrame:
    """Clean dataset by removing duplicates and handling missing values."""
    df = df.drop_duplicates().copy()
    if ai_spec is None:
        df["age"] = df["age"].fillna(df["age"].mean())
        df["billing_amount"] = df["billing_amount"].fillna(0)
        return df

    strat = ai_spec.get("age_missing_strategy", "mean")
    fill_v = float(ai_spec.get("billing_missing_fill", 0))
    if strat == "median":
        df["age"] = df["age"].fillna(df["age"].median())
    else:
        df["age"] = df["age"].fillna(df["age"].mean())
    df["billing_amount"] = df["billing_amount"].fillna(fill_v)
    return df


def transform_data(df: pd.DataFrame):
    """Generate business metrics: billing per diagnosis and daily patient counts."""
    billing = df.groupby("diagnosis")["billing_amount"].sum().reset_index()
    daily = df.groupby("visit_date")["patient_id"].count().reset_index()
    daily = daily.rename(columns={"patient_id": "patient_count"})
    return billing, daily


def save_data(df: pd.DataFrame, file_path: Path) -> None:
    """Save DataFrame to CSV."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def run_pipeline(*, use_ai: bool = False, ai_intent: str | None = None) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        df = load_data(DATA_PATH)
        spec = None
        if use_ai:
            from genai.dynamic_spec import dataframe_summary, healthcare_cleaning_spec

            summary = dataframe_summary(df)
            spec = healthcare_cleaning_spec(summary, ai_intent)
            print("Ollama-enabled spec:", spec)
        df = clean_data(df, ai_spec=spec)
        billing, daily = transform_data(df)
        save_data(billing, OUT_DIR / "billing.csv")
        save_data(daily, OUT_DIR / "daily.csv")
        print("Pipeline completed successfully")
    except Exception as e:
        print("Pipeline failed:", e)


def _env_truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Healthcare ETL (optional --ai uses Ollama JSON spec).")
    parser.add_argument("--ai", action="store_true", help="Ask Ollama for cleaning parameters (JSON-only).")
    parser.add_argument("--intent", default=None, help="Natural-language intent forwarded to the model.")
    args = parser.parse_args()
    use_ai = args.ai or _env_truthy("USE_OLLAMA_PIPELINE")
    run_pipeline(use_ai=use_ai, ai_intent=args.intent)
