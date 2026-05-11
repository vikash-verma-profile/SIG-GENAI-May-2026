"""
Lab 2: AI-driven data quality — Great Expectations on an in-memory DataFrame.
Natural-language expectation notes are documented; validation uses GX Core Expectations.
"""
from __future__ import annotations

import great_expectations as gx
import pandas as pd

# Human-readable rule notes (pair with generated Expectations below).
EXPECTATION_NOTES = """
Revenue must be non-negative.
customer_id should be unique.
"""


def build_sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "revenue": [1000, 2000, -500],
        }
    )


def validate_with_gx(df: pd.DataFrame) -> None:
    context = gx.get_context()
    data_source = context.data_sources.add_pandas("lab2_pandas")
    data_asset = data_source.add_dataframe_asset(name="lab2_df")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("whole_df")
    batch_parameters = {"dataframe": df}
    batch = batch_definition.get_batch(batch_parameters=batch_parameters)

    exp_revenue = gx.expectations.ExpectColumnValuesToBeBetween(
        column="revenue", min_value=0
    )
    exp_unique = gx.expectations.ExpectColumnValuesToBeUnique(column="customer_id")

    print("Expectation notes:\n", EXPECTATION_NOTES)
    for name, exp in [("revenue >= 0", exp_revenue), ("customer_id unique", exp_unique)]:
        result = batch.validate(exp)
        success = result.success
        print(f"\n{name}: success={success}")
        if hasattr(result, "result") and result.result:
            print("Details:", result.result)


def main() -> None:
    df = build_sample_dataframe()
    print("Dataset:\n", df)
    validate_with_gx(df)


if __name__ == "__main__":
    main()
