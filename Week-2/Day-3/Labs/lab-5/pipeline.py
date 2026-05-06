"""Telecom incremental ingestion with watermark + CDC merge."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
STATE_PATH = ROOT / "watermark.txt"
OUTPUT_DIR = ROOT / "output"


def load_data(file: Path) -> pd.DataFrame:
    return pd.read_csv(file)


def incremental_load(df: pd.DataFrame, last_time: str) -> pd.DataFrame:
    return df[df["last_updated"] > last_time]


def apply_cdc(old_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.concat([old_df, new_df], ignore_index=True)
    return df.sort_values("last_updated").drop_duplicates("call_id", keep="last")


def aggregate_calls(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    duration_by_user = df.groupby("user_id")["call_duration"].sum().reset_index()
    daily_counts = df.groupby("call_date")["call_id"].count().reset_index()
    daily_counts = daily_counts.rename(columns={"call_id": "call_count"})
    return duration_by_user, daily_counts


def read_watermark(default: str = "2024-01-01") -> str:
    if STATE_PATH.is_file():
        return STATE_PATH.read_text(encoding="utf-8").strip()
    return default


def write_watermark(ts: str) -> None:
    STATE_PATH.write_text(ts, encoding="utf-8")


def run_pipeline() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    last_processed = read_watermark()
    old_df = load_data(DATA_DIR / "cdr_day1.csv")
    new_df = load_data(DATA_DIR / "cdr_day2.csv")
    inc_df = incremental_load(new_df, last_processed)
    final_df = apply_cdc(old_df, inc_df)
    duration_by_user, daily_counts = aggregate_calls(final_df)
    duration_by_user.to_csv(OUTPUT_DIR / "duration_by_user.csv", index=False)
    daily_counts.to_csv(OUTPUT_DIR / "daily_call_count.csv", index=False)
    write_watermark(final_df["last_updated"].max())
    print(duration_by_user)


if __name__ == "__main__":
    run_pipeline()
