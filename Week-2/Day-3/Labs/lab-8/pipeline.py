"""Logistics pipeline orchestrated with Prefect."""
import logging
from pathlib import Path

import pandas as pd
from prefect import flow, task

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOG = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "shipments.csv"
OUTPUT_PATH = ROOT / "output" / "avg_delivery_by_destination.csv"


def clean_shipments(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["delivery_time"] = df["delivery_time"].fillna(0)
    return df


def avg_delivery_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("destination")["delivery_time"].mean().reset_index()


@task(retries=3, retry_delay_seconds=5)
def ingest() -> pd.DataFrame:
    LOG.info("Ingest started")
    return pd.read_csv(DATA_PATH)


@task
def clean(df: pd.DataFrame) -> pd.DataFrame:
    return clean_shipments(df)


@task
def transform(df: pd.DataFrame) -> pd.DataFrame:
    return avg_delivery_by_destination(df)


@task
def load(df: pd.DataFrame) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    LOG.info("Load complete: %s", OUTPUT_PATH)


@flow(name="logistics-pipeline")
def logistics_pipeline() -> None:
    data = ingest()
    cleaned = clean(data)
    result = transform(cleaned)
    load(result)


if __name__ == "__main__":
    logistics_pipeline()
