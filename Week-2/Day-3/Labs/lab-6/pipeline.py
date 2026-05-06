"""E-commerce schema evolution via union + safe defaults."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"


def load(file: Path) -> pd.DataFrame:
    return pd.read_csv(file)


def merge_schema(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(dfs, ignore_index=True)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "brand" not in out.columns:
        out["brand"] = pd.Series(["Unknown"] * len(out))
    else:
        out["brand"] = out["brand"].fillna("Unknown")
    if "discount" not in out.columns:
        out["discount"] = 0
    else:
        out["discount"] = out["discount"].fillna(0)
    return out


def run_pipeline() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df1 = load(DATA_DIR / "products_day1.csv")
    df2 = load(DATA_DIR / "products_day2.csv")
    df3 = load(DATA_DIR / "products_day3.csv")
    merged = merge_schema([df1, df2, df3])
    final_df = clean(merged)
    final_df.to_csv(OUTPUT_DIR / "final_products.csv", index=False)
    print(final_df.columns.tolist())
    print(final_df.isnull().sum())


if __name__ == "__main__":
    run_pipeline()
