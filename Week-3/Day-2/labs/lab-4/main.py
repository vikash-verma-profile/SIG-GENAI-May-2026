"""
Lab 4: Generate validation checks from simple profiling heuristics (Great Expectations).
"""
from __future__ import annotations

import json
from pathlib import Path

import great_expectations as gx
import pandas as pd

ROOT = Path(__file__).resolve().parent
SUITE_PATH = ROOT / "expectation_suite_lab4.json"


def build_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "revenue": [100.0, 200.0, 150.0],
            "notes": ["a", "b", "c"],
        }
    )


def profile_columns(df: pd.DataFrame) -> None:
    for col in df.columns:
        print(f"\n--- describe: {col} ---")
        print(df[col].describe(include="all"))


def build_expectations_from_profile(df: pd.DataFrame) -> list:
    """Return a list of dict summaries + GX expectation objects to run."""
    expectations = []
    expectations.append(
        gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id")
    )
    expectations.append(
        gx.expectations.ExpectColumnValuesToBeUnique(column="customer_id")
    )
    for col in df.select_dtypes(include="number").columns:
        stats = df[col].describe()
        min_v = float(stats["min"])
        max_v = float(stats["max"])
        expectations.append(
            gx.expectations.ExpectColumnValuesToBeBetween(
                column=col, min_value=min_v, max_value=max_v
            )
        )
    return expectations


def run_suite(df: pd.DataFrame, expectations: list) -> list[dict]:
    context = gx.get_context()
    ds = context.data_sources.add_pandas("lab4_pandas")
    asset = ds.add_dataframe_asset(name="lab4_df")
    bd = asset.add_batch_definition_whole_dataframe("whole")
    batch = bd.get_batch(batch_parameters={"dataframe": df})
    summaries = []
    for exp in expectations:
        res = batch.validate(exp)
        summaries.append(
            {
                "expectation_type": type(exp).__name__,
                "success": bool(res.success),
            }
        )
    return summaries


def main() -> None:
    df = build_dataframe()
    profile_columns(df)
    exps = build_expectations_from_profile(df)
    summaries = run_suite(df, exps)
    SUITE_PATH.write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    print("\nValidation summaries written to", SUITE_PATH)
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
