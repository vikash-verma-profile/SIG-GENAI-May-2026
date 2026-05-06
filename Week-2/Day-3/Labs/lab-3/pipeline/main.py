"""Retail ETL: optional Ollama-driven cleaning parameters (JSON-only)."""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOG = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "orders.csv"
OUT_DIR = ROOT / "output"

LABS_ROOT = ROOT.parent
if str(LABS_ROOT) not in sys.path:
    sys.path.insert(0, str(LABS_ROOT))


def load_data(file_path: Path) -> pd.DataFrame:
    """Load order data from CSV."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        LOG.error("Failed to load orders: %s", e)
        raise


def clean_data(df: pd.DataFrame, ai_spec: dict | None = None) -> pd.DataFrame:
    """Remove duplicates and fill missing quantity/price."""
    df = df.drop_duplicates().copy()
    if ai_spec is None:
        df["quantity"] = df["quantity"].fillna(1)
        df["price"] = df["price"].fillna(0)
        return df.loc[df["price"] > 0].copy()

    q = float(ai_spec.get("quantity_missing_fill", 1))
    p = float(ai_spec.get("price_missing_fill", 0))
    filt = bool(ai_spec.get("filter_non_positive_price", True))
    df["quantity"] = df["quantity"].fillna(q)
    df["price"] = df["price"].fillna(p)
    if filt:
        return df.loc[df["price"] > 0].copy()
    return df


def transform_data(df: pd.DataFrame):
    """Revenue per category and daily sales counts."""
    df = df.copy()
    df["total"] = df["price"] * df["quantity"]
    revenue = df.groupby("category")["total"].sum().reset_index()
    daily_sales = df.groupby("order_date")["order_id"].count().reset_index()
    daily_sales = daily_sales.rename(columns={"order_id": "order_count"})
    return revenue, daily_sales


def save_data(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def run_pipeline(*, use_ai: bool = False, ai_intent: str | None = None) -> None:
    LOG.info("Pipeline started")
    df = load_data(DATA_PATH)
    spec = None
    if use_ai:
        from genai.dynamic_spec import dataframe_summary, retail_cleaning_spec

        summary = dataframe_summary(df)
        spec = retail_cleaning_spec(summary, ai_intent)
        LOG.info("Ollama-enabled spec: %s", spec)
    df = clean_data(df, ai_spec=spec)
    revenue, daily = transform_data(df)
    save_data(revenue, OUT_DIR / "revenue.csv")
    save_data(daily, OUT_DIR / "daily_sales.csv")
    LOG.info("Pipeline finished")


def _env_truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retail ETL (optional --ai uses Ollama JSON spec).")
    parser.add_argument("--ai", action="store_true")
    parser.add_argument("--intent", default=None)
    args = parser.parse_args()
    use_ai = args.ai or _env_truthy("USE_OLLAMA_PIPELINE")
    run_pipeline(use_ai=use_ai, ai_intent=args.intent)
