import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_COLUMNS = {"order_id", "customer_id", "amount", "region"}


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def extract_orders(json_path: Path) -> pd.DataFrame:
    logger = logging.getLogger("extract")
    logger.info("Reading source JSON from %s", json_path)

    if not json_path.exists():
        raise FileNotFoundError(f"Input file not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as f:
        data: Any = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of order records")

    df = pd.DataFrame(data)
    logger.info("Extracted %d raw records", len(df))
    return df


def validate_orders(df: pd.DataFrame) -> pd.DataFrame:
    logger = logging.getLogger("validate")

    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    valid_df = df.copy()
    valid_df["amount"] = pd.to_numeric(valid_df["amount"], errors="coerce")

    negative_mask = valid_df["amount"] < 0
    negative_count = int(negative_mask.sum())
    if negative_count > 0:
        logger.warning("Removing %d records with negative amounts", negative_count)
        valid_df = valid_df[~negative_mask]

    logger.info("Validation completed with %d records", len(valid_df))
    return valid_df


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    logger = logging.getLogger("transform")
    transformed_df = df.copy()

    null_count = int(transformed_df["amount"].isna().sum())
    if null_count > 0:
        logger.info("Replacing %d null/non-numeric amounts with 0", null_count)

    transformed_df["amount"] = transformed_df["amount"].fillna(0)
    transformed_df["region"] = transformed_df["region"].fillna("UNKNOWN")

    agg_df = (
        transformed_df.groupby("region", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total_revenue"})
        .sort_values(by="total_revenue", ascending=False)
    )
    logger.info("Transformation completed for %d regions", len(agg_df))
    return agg_df


def load_to_csv(df: pd.DataFrame, output_path: Path) -> None:
    logger = logging.getLogger("load")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Loaded %d records to %s", len(df), output_path)


def run_etl(input_json: Path, output_csv: Path) -> None:
    logger = logging.getLogger("pipeline")
    logger.info("ETL job started")

    raw_orders = extract_orders(input_json)
    valid_orders = validate_orders(raw_orders)
    transformed_output = transform_orders(valid_orders)
    load_to_csv(transformed_output, output_csv)

    logger.info("ETL job completed successfully")


if __name__ == "__main__":
    configure_logging()

    try:
        base_dir = Path(__file__).resolve().parent
        input_file = base_dir / "Dataset" / "orders.json"
        output_file = base_dir / "output" / "region_revenue.csv"
        run_etl(input_file, output_file)
    except Exception:
        logging.getLogger("pipeline").exception("ETL job failed")
        raise
